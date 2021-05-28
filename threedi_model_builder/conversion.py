import threedi_model_builder.data_models as dm
import threedi_model_builder.enumerators as en
from threedi_model_builder.utils import (
    sqlite_layer,
    gpkg_layer,
    layer_to_gpkg,
    vector_layer_factory,
    cast_if_bool,
)
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
)


class ModelDataConverter:
    """Class with methods Spatialite <==> GeoPackage conversion of the 3Di model layers."""

    def __init__(self, src_sqlite, dst_gpkg, use_source_epsg=True):
        self.src_sqlite = src_sqlite
        self.dst_gpkg = dst_gpkg
        self.epsg_code = 4326
        self.all_models = dm.ALL_MODELS[:]
        self.timeseries_rawdata = OrderedDict()
        if use_source_epsg is True:
            self.set_source_epsg()

    def set_source_epsg(self):
        """Setting source EPSG code from 3Di model settings table."""
        settings_table = next(iter(dm.GlobalSettings.SQLITE_SOURCES))
        settings_layer = sqlite_layer(self.src_sqlite, settings_table, geom_column=None)
        settings_feat = next(settings_layer.getFeatures())
        epsg_from_settings = settings_feat["epsg_code"]
        if epsg_from_settings and epsg_from_settings != self.epsg_code:
            self.epsg_code = epsg_from_settings

    def create_empty_user_layers(self, overwrite=True):
        """Creating empty 3Di User Layers structure within GeoPackage."""
        vector_layers = [vector_layer_factory(model_cls, epsg=self.epsg_code) for model_cls in self.all_models]
        overwrite = overwrite
        write_results = {}
        for vl in vector_layers:
            writer = layer_to_gpkg(vl, self.dst_gpkg, overwrite=overwrite)
            write_results[vl.id()] = writer
            overwrite = False

    def trim_sqlite_targets(self):
        """Removing all features from Spatialite tables."""
        for model_cls in self.all_models:
            for src_table in model_cls.SQLITE_TARGETS or tuple():
                src_layer = sqlite_layer(self.src_sqlite, src_table)
                if not src_layer.isValid():
                    src_layer = sqlite_layer(self.src_sqlite, src_table, geom_column=None)
                fids = [f.id() for f in src_layer.getFeatures()]
                src_layer_dp = src_layer.dataProvider()
                src_layer_dp.deleteFeatures(fids)

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
        """Parsing text Timeseries data into structurized form."""
        series = []
        for row in timeseries_txt.split("\n"):
            duration_str, value_str = row.split(",")
            duration, value = int(duration_str), float(value_str)
            series.append((timeseries_id, reference_layer, reference_id, offset, duration, value))
        return series

    def process_timeseries_rawdata(self):
        """Writing structurized Timeseries into separate table."""
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
        ts_layer.commitChanges()

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
        if src_layer_name in dm.LinearObstacle.SQLITE_SOURCES:
            obstacle_type = en.ObstacleType.LEVEE.value if src_layer_name == "v2_levee" else en.ObstacleType.OTHER.value
            for feat in new_feats:
                feat["type"] = obstacle_type
        elif src_layer_name == dm.Pumpstation.__layername__:
            map_table = dm.PumpstationMap.__tablename__
            map_layer = gpkg_layer(self.dst_gpkg, map_table)
            connections_ids = {feat["pumpstation_id"]: feat["connection_node_end_id"] for feat in
                               map_layer.getFeatures()}
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
        connection_node_points = {f["id"]: f.geometry().asPoint() for f in connection_node_layer.getFeatures()}
        impervious_surface_points = {f["id"]: f.geometry().centroid().asPoint() for f in
                                     impervious_surface_layer.getFeatures()}
        surface_points = {f["id"]: f.geometry().centroid().asPoint() for f in surface_layer.getFeatures()}
        impervious_surface_map_layer = gpkg_layer(self.dst_gpkg, dm.ImperviousSurfaceMap.__tablename__)
        surface_map_layer = gpkg_layer(self.dst_gpkg, dm.SurfaceMap.__tablename__)
        impervious_surface_map_geoms, surface_map_geoms = {}, {}
        for feat in impervious_surface_map_layer.getFeatures():
            fid, node_id, surface_id = feat.id(), feat["connection_node_id"], feat["impervious_surface_id"]
            link_geom = QgsGeometry.fromPolylineXY(
                [impervious_surface_points[surface_id], connection_node_points[node_id]])
            impervious_surface_map_geoms[fid] = link_geom
        for feat in surface_map_layer.getFeatures():
            fid, node_id, surface_id = feat.id(), feat["connection_node_id"], feat["surface_id"]
            link_geom = QgsGeometry.fromPolylineXY(
                [surface_points[surface_id], connection_node_points[node_id]])
            surface_map_geoms[fid] = link_geom
        impervious_surface_map_layer.startEditing()
        for fid, link_geom in impervious_surface_map_geoms.items():
            impervious_surface_map_layer.changeGeometry(fid, link_geom)
        impervious_surface_map_layer.commitChanges()
        surface_map_layer.startEditing()
        for fid, link_geom in surface_map_geoms.items():
            surface_map_layer.changeGeometry(fid, link_geom)
        surface_map_layer.commitChanges()

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
            dst_layer.commitChanges()

    def import_all_model_data(self):
        """Converting all Spatialite layers into GeoPackage User Layers."""
        self.timeseries_rawdata.clear()
        for data_model_cls in self.all_models:
            if data_model_cls == dm.Timeseries:
                continue
            print(f"Processing data for {data_model_cls.__layername__}...")
            self.import_model_data(data_model_cls)
        # Adding geometry between surfaces and connection nodes
        print(f"Adding links between surfaces and connection nodes...")
        self.add_surface_map_geometries()
        # TODO: Uncomment line below after finishing forms implementation
        # self.process_timeseries_rawdata()

    def export_model_data(self, annotated_model_csl):
        """Converting GeoPackage User Layer into Spatialite layer based on model data class."""
        src_table = annotated_model_csl.__tablename__
        src_layer_name = annotated_model_csl.__layername__
        src_layer = gpkg_layer(self.dst_gpkg, src_table, src_layer_name)
        field_mappings = {k: k for k in annotated_model_csl.__annotations__.keys()}
        if annotated_model_csl.EXPORT_FIELD_MAPPINGS:
            field_mappings.update(annotated_model_csl.EXPORT_FIELD_MAPPINGS)
        switched_map = {v: k for k, v in field_mappings.items()}
        if annotated_model_csl == dm.LinearObstacle:
            dst_obstacle_table, dst_levee_table = annotated_model_csl.SQLITE_TARGETS
            # Set expression requests to split Obstacles and Levees
            obstacle_expr = QgsExpression(f'"type" = {en.ObstacleType.OTHER.value}')
            obstacle_request = QgsFeatureRequest(obstacle_expr)
            levee_expr = QgsExpression(f'"type" = {en.ObstacleType.LEVEE.value}')
            levee_request = QgsFeatureRequest(levee_expr)
            dst_obstacle_layer = sqlite_layer(self.src_sqlite, dst_obstacle_table)
            dst_levee_layer = sqlite_layer(self.src_sqlite, dst_levee_table)
            # Copy only obstacle features
            new_obstacle_feats = self.copy_features(src_layer, dst_obstacle_layer, obstacle_request, **switched_map)
            dst_obstacle_layer.startEditing()
            dst_obstacle_layer.addFeatures(new_obstacle_feats)
            dst_obstacle_layer.commitChanges()
            # Copy only levee features
            new_levee_feats = self.copy_features(src_layer, dst_levee_layer, levee_request, **switched_map)
            dst_levee_layer.startEditing()
            dst_levee_layer.addFeatures(new_levee_feats)
            dst_levee_layer.commitChanges()
        else:
            dst_table = next(iter(annotated_model_csl.SQLITE_TARGETS))
            dst_layer = sqlite_layer(self.src_sqlite, dst_table)
            if not dst_layer.isValid():
                dst_layer = sqlite_layer(self.src_sqlite, dst_table, geom_column=None)
            new_feats = self.copy_features(src_layer, dst_layer, **switched_map)
            self.fill_required_attributes(src_layer, new_feats)
            dst_layer.startEditing()
            dst_layer.addFeatures(new_feats)
            dst_layer.commitChanges()

    def export_all_model_data(self):
        """Converting all GeoPackage User Layers into Spatialite layers."""
        # TODO: Uncomment line below after finishing forms implementation
        # self.recreate_timeseries_rawdata()
        for data_model_cls in self.all_models:
            if data_model_cls == dm.Timeseries or data_model_cls == dm.PumpstationMap:
                continue
            print(f"Processing data for {data_model_cls.__layername__}...")
            self.export_model_data(data_model_cls)
