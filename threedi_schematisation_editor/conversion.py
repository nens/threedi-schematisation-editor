# Copyright (C) 2022 by Lutra Consulting
import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.enumerators as en
from threedi_schematisation_editor.utils import (
    sqlite_layer,
    gpkg_layer,
    layer_to_gpkg,
    vector_layer_factory,
    cast_if_bool,
    ConversionError,
)
from threedi_schematisation_editor.communication import UICommunication
from threedi_schematisation_editor.custom_widgets import ProjectionSelectionDialog
from operator import itemgetter
from collections import OrderedDict, defaultdict
from qgis.core import (
    QgsProject,
    QgsWkbTypes,
    QgsFeature,
    QgsFeatureRequest,
    QgsExpression,
    QgsCoordinateTransform,
    QgsGeometry,
    QgsPointXY,
    QgsVectorFileWriter,
)
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QDialog


class ModelDataConverter:
    """Class with methods Spatialite <==> GeoPackage conversion of the 3Di model layers."""

    SUPPORTED_SCHEMA_VERSION = 214

    def __init__(self, src_sqlite, dst_gpkg, epsg_code=4326, user_communication=None):
        self.src_sqlite = src_sqlite
        self.dst_gpkg = dst_gpkg
        self.epsg_code = epsg_code
        self.missing_source_settings = False
        self.all_models = dm.ALL_MODELS[:]
        self.timeseries_rawdata = OrderedDict()
        self.uc = user_communication if user_communication is not None else UICommunication(context="3Di Model Builder")
        self.conversion_errors = defaultdict(list)

    def report_conversion_errors(self):
        """Report all caught conversion errors."""
        error_message = ""
        errors_per_data_model = list(self.conversion_errors.items())
        errors_per_data_model.sort(key=itemgetter(0))
        for layer_name, errors in errors_per_data_model:
            errors_str = "\n".join(errors)
            error_message += f"{layer_name} conversion errors:\n{errors_str}\n"
        error_message.strip()
        if error_message:
            self.uc.show_error(error_message)

    @staticmethod
    def spatialite_schema_version(sqlite_path):
        """Getting Spatialite 3Di model database schema version."""
        schema_version_table = sqlite_layer(sqlite_path, "schema_version", geom_column=None)
        if not schema_version_table.isValid():
            return None
        try:
            schema_row = next(iter(schema_version_table.getFeatures()))
            spatialite_schema_id = int(schema_row["version_num"])
        except (StopIteration, TypeError):
            spatialite_schema_id = 1
        return spatialite_schema_id

    def set_epsg_from_sqlite(self):
        """Setting EPSG code from SQLITE 3Di model settings table."""
        settings_table = next(iter(dm.GlobalSettings.SQLITE_SOURCES))
        settings_layer = sqlite_layer(self.src_sqlite, settings_table, geom_column=None)
        try:
            settings_feat = next(settings_layer.getFeatures())
            fetched_epsg = settings_feat["epsg_code"]
        except StopIteration:
            self.missing_source_settings = True
            msg = f"'{settings_table}' table is empty. Please pick EPSG code that you want to use first."
            self.uc.show_warn(msg)
            crs_selection_dlg = ProjectionSelectionDialog()
            res = crs_selection_dlg.exec_()
            if res == QDialog.Accepted:
                selected_crs = crs_selection_dlg.projection_selection.crs()
                epsg_str = selected_crs.authid().split(":")[-1]
                if epsg_str.isnumeric():
                    fetched_epsg = int(epsg_str)
                else:
                    fetched_epsg = -1
            else:
                return False
        if fetched_epsg and fetched_epsg != self.epsg_code:
            self.epsg_code = fetched_epsg
        return True

    def set_epsg_from_gpkg(self):
        """Setting EPSG code from GeoPackage 3Di model settings table."""
        settings_table = dm.GlobalSettings.__tablename__
        settings_layer = gpkg_layer(self.dst_gpkg, settings_table)
        try:
            settings_feat = next(settings_layer.getFeatures())
        except StopIteration:
            msg = f"'{dm.GlobalSettings.__layername__}' layer is empty. Please add record with EPSG code first."
            self.uc.show_error(msg)
            return False
        fetched_epsg = settings_feat["epsg_code"]
        if fetched_epsg and fetched_epsg != self.epsg_code:
            self.epsg_code = fetched_epsg
        return True

    def create_empty_user_layers(self, overwrite=True):
        """Creating empty 3Di User Layers structure within GeoPackage."""
        vector_layers = [vector_layer_factory(model_cls, epsg=self.epsg_code) for model_cls in self.all_models]
        overwrite = overwrite
        for vl in vector_layers:
            writer, error_msg = layer_to_gpkg(vl, self.dst_gpkg, overwrite=overwrite)
            if writer != QgsVectorFileWriter.NoError:
                self.uc.show_error(error_msg)
                raise ConversionError((writer, error_msg))
            overwrite = False

    def trim_sqlite_targets(self):
        """Removing all features from Spatialite tables."""
        self.conversion_errors.clear()
        for model_cls in self.all_models:
            for src_table in model_cls.SQLITE_TARGETS or tuple():
                src_layer = sqlite_layer(self.src_sqlite, src_table)
                if not src_layer.isValid():
                    src_layer = sqlite_layer(self.src_sqlite, src_table, geom_column=None)
                fids = [f.id() for f in src_layer.getFeatures()]
                src_layer.startEditing()
                src_layer.deleteFeatures(fids)
                success = src_layer.commitChanges()
                if not success:
                    commit_errors = src_layer.commitErrors()
                    self.conversion_errors[model_cls.__layername__] += commit_errors

    @staticmethod
    def copy_features(src_layer, dst_layer, request=None, **field_mappings):
        """Handling copying of features during Spatialite <==> GeoPackage conversion."""
        src_crs = src_layer.sourceCrs()
        dest_crs = dst_layer.sourceCrs()
        if src_crs != dest_crs:
            context = QgsProject.instance().transformContext()
            transformation = QgsCoordinateTransform(src_crs, dest_crs, context)

            def geometry_transform(geometry):
                geometry.transform(transformation)

        else:

            def geometry_transform(geometry):
                pass

        src_fields = src_layer.fields()
        dst_fields = dst_layer.fields()
        src_field_names = {f.name() for f in src_fields}
        dst_field_names = {f.name() for f in dst_fields}
        skip_geometry = dst_layer.geometryType() == QgsWkbTypes.GeometryType.NullGeometry
        if skip_geometry:

            def transfer_geometry(source_feat, destination_feat):
                pass

        else:

            def transfer_geometry(source_feat, destination_feat):
                src_geom = source_feat.geometry()
                new_geom = QgsGeometry(src_geom)
                geometry_transform(new_geom)
                destination_feat.setGeometry(new_geom)

        field_mappings = {
            dst_fld: src_fld
            for dst_fld, src_fld in field_mappings.items()
            if src_fld in src_field_names and dst_fld in dst_field_names
        }
        new_feats = []
        for src_feat in src_layer.getFeatures() if request is None else src_layer.getFeatures(request):
            dst_feat = QgsFeature(dst_fields)
            transfer_geometry(src_feat, dst_feat)
            for dst_field, src_field in field_mappings.items():
                src_value = src_feat[src_field]
                dst_feat[dst_field] = cast_if_bool(src_value)
            new_feats.append(dst_feat)
        return new_feats

    def extract_timeseries_rawdata(self, src_layer, dst_layer):
        """Extracting Timeseries data from layer features."""
        dst_layer_name = dst_layer.name()
        for src_feat in src_layer.getFeatures():
            self.timeseries_rawdata[dst_layer_name, src_feat["id"]] = src_feat["timeseries"]

    @staticmethod
    def parse_timeseries_row(timeseries_txt, timeseries_id, reference_layer, reference_id, offset=0):
        """Parsing text Timeseries data into structured form."""
        series = []
        for row in timeseries_txt.split("\n"):
            duration_str, value_str = row.split(",")
            duration, value = int(duration_str), float(value_str)
            series.append((timeseries_id, reference_layer, reference_id, offset, duration, value))
        return series

    def process_timeseries_rawdata(self):
        """Writing structured Timeseries into separate table."""
        ts_layer = gpkg_layer(self.dst_gpkg, dm.Timeseries.__tablename__)
        ts_fields = ts_layer.fields()
        ts_field_names = [f.name() for f in ts_fields]
        ts_field_names.remove("fid")
        ts_features = []
        for ts_id, ((reference_layer, reference_id), ts_txt) in enumerate(self.timeseries_rawdata.items(), start=1):
            timeseries = self.parse_timeseries_row(ts_txt, ts_id, reference_layer, reference_id)
            for ts_row in timeseries:
                ts_feat = QgsFeature(ts_fields)
                for field_name, field_value in zip(ts_field_names, ts_row):
                    ts_feat[field_name] = field_value
                ts_features.append(ts_feat)
        ts_layer.startEditing()
        ts_layer.addFeatures(ts_features)
        success = ts_layer.commitChanges()
        if not success:
            commit_errors = ts_layer.commitErrors()
            self.conversion_errors[dm.Timeseries.__layername__] += commit_errors

    def recreate_timeseries_rawdata(self):
        """Reading Timeseries from User Layer table."""
        self.timeseries_rawdata.clear()
        ts_layer = gpkg_layer(self.dst_gpkg, dm.Timeseries.__tablename__)
        grouped_records = defaultdict(list)
        for feat_ts in ts_layer.getFeatures():
            reference_layer = feat_ts["reference_layer"]
            reference_id = feat_ts["reference_id"]
            ts_row = [feat_ts["duration"], feat_ts["value"]]
            grouped_records[reference_layer, reference_id].append(ts_row)
        for key, values in grouped_records.items():
            values.sort(key=itemgetter(0))
            ts_txt = "\n".join(",".join(str(col) for col in row) for row in values)
            self.timeseries_rawdata[key] = ts_txt

    def fill_required_attributes(self, src_layer, new_feats):
        """Filling required attributes during Spatialite <==> GeoPackage conversion."""
        src_layer_name = src_layer.name()
        layers_with_ts = {el.__layername__ for el in dm.ELEMENTS_WITH_TIMESERIES}
        if src_layer_name == dm.Pumpstation.__layername__:
            map_table = dm.PumpstationMap.__tablename__
            map_layer = gpkg_layer(self.dst_gpkg, map_table)
            connections_ids = {
                feat["pumpstation_id"]: feat["connection_node_end_id"] for feat in map_layer.getFeatures()
            }
            for feat in new_feats:
                feat_id = feat["id"]
                try:
                    feat["connection_node_end_id"] = connections_ids[feat_id]
                except KeyError:
                    continue
        elif src_layer_name in layers_with_ts:
            for feat in new_feats:
                feat_id = feat["id"]
                try:
                    feat["timeseries"] = self.timeseries_rawdata[src_layer_name, feat_id]
                except KeyError:
                    continue
        else:
            pass

    def add_surface_map_geometries(self):
        """Adding polyline geometries to the surfaces map layers."""
        connection_node_layer = gpkg_layer(self.dst_gpkg, dm.ConnectionNode.__tablename__)
        impervious_surface_layer = gpkg_layer(self.dst_gpkg, dm.ImperviousSurface.__tablename__)
        surface_layer = gpkg_layer(self.dst_gpkg, dm.Surface.__tablename__)
        connection_node_points = {f["id"]: f.geometry() for f in connection_node_layer.getFeatures()}
        impervious_surface_points = {f["id"]: f.geometry().centroid() for f in impervious_surface_layer.getFeatures()}
        surface_points = {f["id"]: f.geometry().centroid() for f in surface_layer.getFeatures()}
        impervious_surface_map_layer = gpkg_layer(self.dst_gpkg, dm.ImperviousSurfaceMap.__tablename__)
        surface_map_layer = gpkg_layer(self.dst_gpkg, dm.SurfaceMap.__tablename__)
        impervious_surface_map_geoms, surface_map_geoms = {}, {}
        for feat in impervious_surface_map_layer.getFeatures():
            fid, node_id, surface_id = feat.id(), feat["connection_node_id"], feat["impervious_surface_id"]
            try:
                connection_node_geom = connection_node_points[node_id]
            except KeyError:
                missing_node_error = (
                    f"Impervious Surface ({fid}) with an invalid 'connection_node_id' reference. "
                    f"Node ({node_id}) doesn't exist."
                )
                self.conversion_errors[dm.ImperviousSurface.__layername__].append(missing_node_error)
                continue
            connection_node_point = connection_node_geom.asPoint()
            isurface_centroid_geom = impervious_surface_points[surface_id]
            try:
                isurface_point = isurface_centroid_geom.asPoint()
            except ValueError:
                # If surface have no geometry let use point laying 10 meters to the north from connection node
                isurface_point = QgsPointXY(connection_node_point.x(), connection_node_point.y() + 10.0)
            link_geom = QgsGeometry.fromPolylineXY([isurface_point, connection_node_point])
            impervious_surface_map_geoms[fid] = link_geom
        for feat in surface_map_layer.getFeatures():
            fid, node_id, surface_id = feat.id(), feat["connection_node_id"], feat["surface_id"]
            try:
                connection_node_geom = connection_node_points[node_id]
            except KeyError:
                missing_node_error = (
                    f"Surface ({fid}) with an invalid 'connection_node_id' reference. "
                    f"Node ({node_id}) doesn't exist."
                )
                self.conversion_errors[dm.Surface.__layername__].append(missing_node_error)
                continue
            connection_node_point = connection_node_geom.asPoint()
            surface_centroid_geom = surface_points[surface_id]
            try:
                surface_point = surface_centroid_geom.asPoint()
            except ValueError:
                # If surface have no geometry let use point laying 10 meters to the north from connection node
                surface_point = QgsPointXY(connection_node_point.x(), connection_node_point.y() + 10.0)
            link_geom = QgsGeometry.fromPolylineXY([surface_point, connection_node_point])
            surface_map_geoms[fid] = link_geom
        impervious_surface_map_layer.startEditing()
        for fid, link_geom in impervious_surface_map_geoms.items():
            impervious_surface_map_layer.changeGeometry(fid, link_geom)
        success = impervious_surface_map_layer.commitChanges()
        if not success:
            commit_errors = impervious_surface_map_layer.commitErrors()
            self.conversion_errors[dm.ImperviousSurface.__layername__] += commit_errors
        surface_map_layer.startEditing()
        for fid, link_geom in surface_map_geoms.items():
            surface_map_layer.changeGeometry(fid, link_geom)
        success = surface_map_layer.commitChanges()
        if not success:
            commit_errors = surface_map_layer.commitErrors()
            self.conversion_errors[dm.Surface.__layername__] += commit_errors

    def import_model_data(self, annotated_model_csl):
        """Converting Spatialite layer into GeoPackage User Layer based on model data class."""
        dst_table = annotated_model_csl.__tablename__
        dst_layer_name = annotated_model_csl.__layername__
        dst_layer = gpkg_layer(self.dst_gpkg, dst_table, dst_layer_name)
        field_mappings = {k: k for k in annotated_model_csl.__annotations__.keys()}
        if annotated_model_csl.IMPORT_FIELD_MAPPINGS:
            field_mappings.update(annotated_model_csl.IMPORT_FIELD_MAPPINGS)
        for src_table in annotated_model_csl.SQLITE_SOURCES:
            src_layer = sqlite_layer(self.src_sqlite, src_table)
            if not src_layer.isValid():
                src_layer = sqlite_layer(self.src_sqlite, src_table, geom_column=None)
            src_field_names = {f.name() for f in src_layer.fields()}
            layer_with_ts = "timeseries" in src_field_names
            new_feats = self.copy_features(src_layer, dst_layer, **field_mappings)
            # Extra logic for dealing with Linear obstacles
            self.fill_required_attributes(src_layer, new_feats)
            # Extra logic for dealing with Timeseries
            if layer_with_ts:
                self.extract_timeseries_rawdata(src_layer, dst_layer)
            dst_layer.startEditing()
            dst_layer.addFeatures(new_feats)
            success = dst_layer.commitChanges()
            if not success:
                commit_errors = dst_layer.commitErrors()
                self.conversion_errors[dst_layer_name] += commit_errors

    def collect_src_dst_ids(self, annotated_model_csl):
        """Getting unique feature IDs of source and destination layers."""
        src_feat_ids, dst_feat_ids = set(), set()
        src_expr = None
        if annotated_model_csl == dm.Pumpstation:
            src_expr = QgsExpression('"connection_node_start_id" IS NOT NULL')
        elif annotated_model_csl == dm.PumpstationMap:
            src_expr = QgsExpression('"connection_node_start_id" IS NOT NULL AND "connection_node_end_id" IS NOT NULL')
        if src_expr is None:
            src_request = QgsFeatureRequest()
        else:
            src_request = QgsFeatureRequest(src_expr)
        src_request.setFlags(QgsFeatureRequest.NoGeometry)
        dst_request = QgsFeatureRequest()
        dst_request.setFlags(QgsFeatureRequest.NoGeometry)
        for src_table in annotated_model_csl.SQLITE_TARGETS:
            src_target_layer = sqlite_layer(self.src_sqlite, src_table)
            if not src_target_layer.isValid():
                src_target_layer = sqlite_layer(self.src_sqlite, src_table, geom_column=None)
            # Let's assume that ids are unique across multiple sqlite targets
            src_feat_ids |= {src_feat["id"] for src_feat in src_target_layer.getFeatures(src_request)}
        dst_table = annotated_model_csl.__tablename__
        dst_layer = gpkg_layer(self.dst_gpkg, dst_table)
        dst_id_idx = dst_layer.fields().indexFromName("id")
        dst_feat_ids |= set(dst_layer.uniqueValues(dst_id_idx))
        return src_feat_ids, dst_feat_ids

    def import_cross_section_definition_data(self):
        """Importing and splitting cross-section definition data."""
        xs_def_table = next(iter(dm.CrossSectionDefinition.SQLITE_SOURCES))
        xs_def_lyr = sqlite_layer(self.src_sqlite, xs_def_table)
        if not xs_def_lyr.isValid():
            xs_def_lyr = sqlite_layer(self.src_sqlite, xs_def_table, geom_column=None)
        first_model_with_xs_def = next(iter(dm.ELEMENTS_WITH_XS_DEF))
        dst_field_names = [
            field_name
            for field_name in first_model_with_xs_def.__annotations__.keys()
            if field_name.startswith("cross_section_")
        ]
        # Get cross-section definition data and reformat it to fit User Layers structure
        xs_definitions = {}
        for xs_def_feat in xs_def_lyr.getFeatures():
            src_xs_def_id = xs_def_feat["id"]
            src_xs_def_shape = xs_def_feat["shape"]
            src_xs_def_height = xs_def_feat["height"]
            src_xs_def_width = xs_def_feat["width"]
            if src_xs_def_shape in dm.TABLE_SHAPES:
                xs_def_table = "\n".join(
                    f"{h}, {w}" for h, w in zip(src_xs_def_height.split(), src_xs_def_width.split())
                )
                xs_def_height = None
                xs_def_width = None
            else:
                try:
                    xs_def_height = float(src_xs_def_height)
                except (TypeError, ValueError):
                    xs_def_height = None
                try:
                    xs_def_width = float(src_xs_def_width)
                except (TypeError, ValueError):
                    xs_def_width = None
                xs_def_table = None
            xs_def_data = {
                "cross_section_shape": src_xs_def_shape,
                "cross_section_height": xs_def_height,
                "cross_section_width": xs_def_width,
                "cross_section_table": xs_def_table,
            }
            xs_definitions[src_xs_def_id] = xs_def_data
        # Update User Layers cross-section definition data
        request = QgsFeatureRequest()
        request.setFlags(QgsFeatureRequest.NoGeometry)
        for model_cls in dm.ELEMENTS_WITH_XS_DEF:
            # Initialize spatialite and GeoPackage layers for the model class with the cross-section definition data
            table_name = next(iter(model_cls.SQLITE_SOURCES))
            src_xs_def_lyr = sqlite_layer(self.src_sqlite, table_name)
            if not src_xs_def_lyr.isValid():
                src_xs_def_lyr = sqlite_layer(self.src_sqlite, table_name, geom_column=None)
            dst_xs_def_lyr = gpkg_layer(self.dst_gpkg, model_cls.__tablename__)
            # Map field names to field indexes
            dst_layer_fields = dst_xs_def_lyr.fields()
            field_indexes = {fld: dst_layer_fields.lookupField(fld) for fld in dst_field_names}
            # Establish `cross_section_definition_id` field
            src_id_field_name = model_cls.IMPORT_FIELD_MAPPINGS["id"]
            xs_def_id_field_name = None
            for field in src_xs_def_lyr.fields():
                field_name = field.name()
                if "definition_id" in field_name:
                    xs_def_id_field_name = field_name
                    break
            # Map feature `id`s to cross-section definition `id`s based on source spatialite layers
            feat_to_xs_def = {}
            for src_feat in src_xs_def_lyr.getFeatures(request):
                src_feat_id = src_feat[src_id_field_name]
                xs_def_id = src_feat[xs_def_id_field_name]
                feat_to_xs_def[src_feat_id] = xs_def_id
            # Pair cross-section definition data with User Layer features and prepare update dictionary
            xs_def_data_changes = {}
            for dst_feat in dst_xs_def_lyr.getFeatures(request):
                fid = dst_feat.id()
                dst_feat_id = dst_feat["id"]
                xs_def_id = feat_to_xs_def[dst_feat_id]
                xs_def_data = xs_definitions[xs_def_id]
                xs_def_data_changes[fid] = {field_indexes[fld]: xs_def_data[fld] for fld in xs_def_data.keys()}
            # Update User Layers with cross-section definition data
            dst_xs_def_lyr.startEditing()
            for fid, changes in xs_def_data_changes.items():
                dst_xs_def_lyr.changeAttributeValues(fid, changes)
            success = dst_xs_def_lyr.commitChanges()
            if not success:
                commit_errors = dst_xs_def_lyr.commitErrors()
                self.conversion_errors[model_cls.__layername__] += commit_errors

    def import_all_model_data(self):
        """Converting all Spatialite layers into GeoPackage User Layers."""
        self.conversion_errors.clear()
        self.timeseries_rawdata.clear()
        models_to_import = list(self.all_models)
        models_to_import.remove(dm.Timeseries)
        models_to_import.remove(dm.CrossSectionDefinition)
        number_of_steps = len(models_to_import)
        msg = "Loading data from Spatialite..."
        self.uc.progress_bar(msg, 0, number_of_steps, 0, clear_msg_bar=True)
        QCoreApplication.processEvents()
        incomplete_imports = OrderedDict()
        for i, data_model_cls in enumerate(models_to_import):
            msg = f'Loading "{data_model_cls.__layername__}" layer data...'
            self.uc.progress_bar(msg, 0, number_of_steps, i, clear_msg_bar=True)
            QCoreApplication.processEvents()
            self.import_model_data(data_model_cls)
            if data_model_cls == dm.SchemaVersion:
                continue
            sqlite_feat_ids, gpkg_feat_ids = self.collect_src_dst_ids(data_model_cls)
            sqlite_feat_count = len(sqlite_feat_ids)
            gpkg_feat_count = len(gpkg_feat_ids)
            if sqlite_feat_count != gpkg_feat_count:
                missing_ids = list(sorted(sqlite_feat_ids - gpkg_feat_ids))
                missing = len(missing_ids)
                if missing:
                    incomplete_imports[data_model_cls] = (sqlite_feat_count, gpkg_feat_count, missing, missing_ids)
        # Adding geometry between surfaces and connection nodes
        msg = f"Adding links between surfaces and connection nodes..."
        self.uc.progress_bar(msg, 0, number_of_steps, number_of_steps, clear_msg_bar=True)
        QCoreApplication.processEvents()
        self.add_surface_map_geometries()
        msg = f"Importing and splitting cross-section definition data..."
        self.uc.progress_bar(msg, 0, number_of_steps, number_of_steps, clear_msg_bar=True)
        QCoreApplication.processEvents()
        self.import_cross_section_definition_data()
        self.uc.clear_message_bar()
        # TODO: Uncomment line below after finishing forms implementation
        # self.process_timeseries_rawdata()
        if incomplete_imports:
            warn = "Incomplete import:\n"
            for model_cls, (sqlite_fc, gpkg_fc, miss_no, missing_ids) in incomplete_imports.items():
                layer_name = model_cls.__layername__
                warn += f"\n{layer_name}: {gpkg_fc} out of {sqlite_fc} features imported ({miss_no} missing)\n"
                ids_str = ", ".join(str(mid) for mid in missing_ids[:10])
                warn += f"ID's of missing features: {ids_str}"
                if miss_no > 10:
                    warn += " ..."
            warn += "\nPlease run the 3Di schematization checker for more details"
            self.uc.show_warn(warn)
        self.report_conversion_errors()

    def export_model_data(self, annotated_model_csl):
        """Converting GeoPackage User Layer into Spatialite layer based on model data class."""
        src_table = annotated_model_csl.__tablename__
        src_layer_name = annotated_model_csl.__layername__
        src_layer = gpkg_layer(self.dst_gpkg, src_table, src_layer_name)
        field_mappings = {k: k for k in annotated_model_csl.__annotations__.keys()}
        if annotated_model_csl.EXPORT_FIELD_MAPPINGS:
            field_mappings.update(annotated_model_csl.EXPORT_FIELD_MAPPINGS)
        switched_map = {v: k for k, v in field_mappings.items()}
        dst_table = next(iter(annotated_model_csl.SQLITE_TARGETS))
        dst_layer = sqlite_layer(self.src_sqlite, dst_table)
        if not dst_layer.isValid():
            dst_layer = sqlite_layer(self.src_sqlite, dst_table, geom_column=None)
        new_feats = self.copy_features(src_layer, dst_layer, **switched_map)
        self.fill_required_attributes(src_layer, new_feats)
        dst_layer.startEditing()
        dst_layer.addFeatures(new_feats)
        success = dst_layer.commitChanges()
        if not success:
            commit_errors = dst_layer.commitErrors()
            self.conversion_errors[src_layer_name] += commit_errors

    @staticmethod
    def cross_section_definition_code(shape, width, width_values=None, height_values=None):
        """Generate cross-section definition code."""
        if shape in {en.CrossSectionShape.OPEN_RECTANGLE.value, en.CrossSectionShape.CLOSED_RECTANGLE.value} and width:
            code = f"rect_{width:.3f}"
        elif shape == en.CrossSectionShape.CIRCLE.value and width:
            code = f"round_{width:.3f}"
        elif shape == en.CrossSectionShape.EGG.value and width:
            code = f"egg_{width:.3f}_{width * 1.5:.3f}"
        elif shape == en.CrossSectionShape.TABULATED_RECTANGLE.value and width_values and height_values:
            code = f"tab_rect_{float(max(width_values, key=float)):.3f}_{float(max(height_values, key=float)):.3f}"
        elif shape == en.CrossSectionShape.TABULATED_TRAPEZIUM.value and width_values and height_values:
            code = f"tab_trap_{float(max(width_values, key=float)):.3f}_{float(max(height_values, key=float)):.3f}"
        else:
            code = None
        return code

    def export_cross_section_definition_data(self):
        """Exporting and aggregating cross-section definition data."""
        request = QgsFeatureRequest()
        request.setFlags(QgsFeatureRequest.NoGeometry)
        xs_def_data_ids = OrderedDict()
        lyr_feat_to_xs_def_id = {}
        next_xs_def_id = 1
        # Get and aggregate cross-section definition data
        for model_cls in dm.ELEMENTS_WITH_XS_DEF:
            table_name = next(iter(model_cls.SQLITE_TARGETS))
            src_with_xs_def_lyr = gpkg_layer(self.dst_gpkg, model_cls.__tablename__)
            for feat_with_xs_def in src_with_xs_def_lyr.getFeatures(request):
                feat_id = feat_with_xs_def["id"]
                src_xs_def_shape = feat_with_xs_def["cross_section_shape"]
                src_xs_def_height = feat_with_xs_def["cross_section_height"]
                src_xs_def_width = feat_with_xs_def["cross_section_width"]
                src_xs_def_table = feat_with_xs_def["cross_section_table"]
                if src_xs_def_shape in dm.TABLE_SHAPES and src_xs_def_table:
                    parsed_table = [row.split(",") for row in src_xs_def_table.split("\n")]
                    height_values, width_values = list(zip(*parsed_table))
                    xs_def_height = " ".join(hv.strip() for hv in height_values)
                    xs_def_width = " ".join(wv.strip() for wv in width_values)
                    src_xs_def_code = self.cross_section_definition_code(
                        src_xs_def_shape, src_xs_def_width, width_values, height_values
                    )
                else:
                    xs_def_height = str(src_xs_def_height) if src_xs_def_height else None
                    xs_def_width = str(src_xs_def_width) if src_xs_def_width else None
                    src_xs_def_code = self.cross_section_definition_code(src_xs_def_shape, src_xs_def_width)
                xs_def_data = (src_xs_def_code, src_xs_def_shape, xs_def_height, xs_def_width)
                try:
                    xs_def_id = xs_def_data_ids[xs_def_data]
                except KeyError:
                    xs_def_id = next_xs_def_id
                    xs_def_data_ids[xs_def_data] = xs_def_id
                    next_xs_def_id += 1
                lyr_feat_to_xs_def_id[table_name, feat_id] = xs_def_id
        # Inserting CrossSectionDefinition data
        xs_def_table = next(iter(dm.CrossSectionDefinition.SQLITE_TARGETS))
        xs_def_lyr = sqlite_layer(self.src_sqlite, xs_def_table)
        if not xs_def_lyr.isValid():
            xs_def_lyr = sqlite_layer(self.src_sqlite, xs_def_table, geom_column=None)
        xs_def_fields = xs_def_lyr.fields()
        new_xs_def_feats = []
        for (xs_def_code, xs_def_shape, xs_def_height, xs_def_width), xs_def_id in xs_def_data_ids.items():
            new_feat = QgsFeature(xs_def_fields)
            new_feat["id"] = xs_def_id
            new_feat["code"] = xs_def_code
            new_feat["shape"] = xs_def_shape
            new_feat["height"] = xs_def_height
            new_feat["width"] = xs_def_width
            new_xs_def_feats.append(new_feat)
        xs_def_lyr.startEditing()
        xs_def_lyr.addFeatures(new_xs_def_feats)
        success = xs_def_lyr.commitChanges()
        if not success:
            commit_errors = xs_def_lyr.commitErrors()
            self.conversion_errors[dm.CrossSectionDefinition.__layername__] += commit_errors
        # Update `cross_section_definition_id` fields in the layers that refers to the cross-section definition data
        for model_cls in dm.ELEMENTS_WITH_XS_DEF:
            dst_changes = {}
            table_name = next(iter(model_cls.SQLITE_TARGETS))
            dst_with_xs_def_lyr = sqlite_layer(self.src_sqlite, table_name)
            if not dst_with_xs_def_lyr.isValid():
                dst_with_xs_def_lyr = sqlite_layer(self.src_sqlite, table_name, geom_column=None)
            # Establish `cross_section_definition_id` field index
            dst_with_xs_def_lyr_fields = dst_with_xs_def_lyr.fields()
            xs_def_id_field = "definition_id" if model_cls == dm.CrossSectionLocation else "cross_section_definition_id"
            xs_def_id_field_idx = dst_with_xs_def_lyr_fields.lookupField(xs_def_id_field)
            # Create dictionary with `cross_section_definition_id` updates
            for dst_feat in dst_with_xs_def_lyr.getFeatures(request):
                feat_fid = dst_feat.id()
                dst_feat_id = dst_feat["id"]
                xs_def_id = lyr_feat_to_xs_def_id[table_name, dst_feat_id]
                dst_changes[feat_fid] = xs_def_id
            # Update `cross_section_definition_id`field
            dst_with_xs_def_lyr.startEditing()
            for feat_fid, xs_def_id in dst_changes.items():
                dst_with_xs_def_lyr.changeAttributeValue(feat_fid, xs_def_id_field_idx, xs_def_id)
            success = dst_with_xs_def_lyr.commitChanges()
            if not success:
                commit_errors = dst_with_xs_def_lyr.commitErrors()
                self.conversion_errors[model_cls.__layername__] += commit_errors

    def export_all_model_data(self):
        """Converting all GeoPackage User Layers into Spatialite layers."""
        # TODO: Uncomment line below after finishing forms implementation
        # self.recreate_timeseries_rawdata()
        self.conversion_errors.clear()
        models_to_export = list(self.all_models)
        models_to_export.remove(dm.Timeseries)
        models_to_export.remove(dm.PumpstationMap)
        models_to_export.remove(dm.CrossSectionDefinition)
        number_of_steps = len(models_to_export)
        msg = "Saving data into Spatialite..."
        self.uc.progress_bar(msg, 0, number_of_steps, 0, clear_msg_bar=True)
        QCoreApplication.processEvents()
        incomplete_exports = OrderedDict()
        for i, data_model_cls in enumerate(models_to_export):
            msg = f'Saving "{data_model_cls.__layername__}" layer data...'
            self.uc.progress_bar(msg, 0, number_of_steps, i, clear_msg_bar=True)
            QCoreApplication.processEvents()
            self.export_model_data(data_model_cls)
            if data_model_cls == dm.SchemaVersion:
                continue
            sqlite_feat_ids, gpkg_feat_ids = self.collect_src_dst_ids(data_model_cls)
            sqlite_feat_count = len(sqlite_feat_ids)
            gpkg_feat_count = len(gpkg_feat_ids)
            if gpkg_feat_count != sqlite_feat_count:
                missing_ids = list(sorted(gpkg_feat_ids - sqlite_feat_ids))
                missing = len(missing_ids)
                if missing:
                    incomplete_exports[data_model_cls] = (sqlite_feat_count, gpkg_feat_count, missing, missing_ids)
        msg = f"Exporting and aggregating cross-section definition data..."
        self.uc.progress_bar(msg, 0, number_of_steps, number_of_steps, clear_msg_bar=True)
        QCoreApplication.processEvents()
        self.export_cross_section_definition_data()
        self.uc.clear_message_bar()
        if incomplete_exports:
            warn = "Incomplete export:\n"
            for model_cls, (sqlite_fc, gpkg_fc, miss_no, miss_ids) in incomplete_exports.items():
                layer_name = model_cls.__layername__
                warn += f"\n{layer_name}: {sqlite_fc} out of {gpkg_fc} features exported ({miss_no} missing)\n"
                ids_str = ", ".join(str(mid) for mid in miss_ids[:10])
                warn += f"ID's of missing features: {ids_str}"
                if miss_no > 10:
                    warn += " ..."
            self.uc.show_warn(warn)
        self.report_conversion_errors()
