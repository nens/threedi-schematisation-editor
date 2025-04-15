# Copyright (C) 2025 by Lutra Consulting
import os
import re
from functools import cached_property
from pathlib import Path
from types import MappingProxyType
from uuid import uuid4

from qgis.core import (Qgis, QgsEditFormConfig, QgsEditorWidgetSetup,
                       QgsExpression, QgsExpressionContextUtils, QgsFeatureRequest, QgsFieldConstraints,
                       QgsProject, QgsRasterLayer, QgsSnappingConfig,
                       QgsTolerance, QgsVectorLayerJoinInfo)
from qgis.PyQt.QtCore import QCoreApplication

import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.enumerators as en
from threedi_schematisation_editor.expressions import (
    cross_section_label, cross_section_max_height, cross_section_max_width)
from threedi_schematisation_editor.styles.style_config import (
    get_style_configurations, styles_location)
from threedi_schematisation_editor.user_layer_forms import LayerEditFormFactory
from threedi_schematisation_editor.user_layer_handlers import MODEL_HANDLERS
from threedi_schematisation_editor.utils import (
    add_layer_to_group, create_tree_group, get_form_ui_path,
    get_qml_style_path, gpkg_layer, hillshade_layer, merge_qml_styles,
    modify_raster_style, remove_group_with_children, remove_layer,
    set_field_default_value, set_initial_layer_configuration,
    validation_errors_summary, ProjectVariableDict)


class LayersManager:
    """Class with methods and attributes used for managing 3Di User Layers."""

    VECTOR_GROUPS = (
        ("Laterals & 0D inflow", dm.MODEL_0D_INFLOW_ELEMENTS),
        ("Structure control", dm.STRUCTURE_CONTROL_ELEMENTS),
        ("1D", dm.MODEL_1D_ELEMENTS),
        ("1D2D", dm.MODEL_1D2D_ELEMENTS),
        ("2D", dm.MODEL_2D_ELEMENTS),
        ("Hydrological processes", dm.HYDROLOGICAL_PROCESSES),
        ("Settings", dm.SETTINGS_ELEMENTS),
    )
    RASTER_GROUPS = (("Rasters", dm.ELEMENTS_WITH_RASTERS),)
    LAYER_JOINS = MappingProxyType({})
    VALUE_RELATIONS = MappingProxyType(
        {
            # parent model: (child model, parent column, child key column, child value column)
            dm.Surface: (dm.SurfaceParameters, "surface_parameters_id", "id", "description"),
            dm.DryWeatherFlow: (dm.DryWeatherFlowDistribution, "dry_weather_flow_distribution_id", "id", "description"),
            dm.Culvert: (dm.Material, "material_id", "id", "description"),
            dm.Pipe: (dm.Material, "material_id", "id", "description"),
            dm.Weir: (dm.Material, "material_id", "id", "description"),
            dm.Orifice: (dm.Material, "material_id", "id", "description"),
        }
    )

    def __init__(self, iface, user_communication, model_gpkg_path):
        self.iface = iface
        self.uc = user_communication
        self.model_gpkg_path = os.path.normpath(model_gpkg_path)
        self.form_factory = LayerEditFormFactory(self)
        self.model_handlers = {}
        self.layer_handlers = {}
        self.spawned_groups = {}
        self.active_form_signals = set()
        self.iface.currentLayerChanged.connect(self.on_active_layer_changed)

    @cached_property
    def snapping_groups(self):
        snap_groups = {
            dm.ConnectionNode: {
                dm.Pipe,
                dm.Weir,
                dm.Orifice,
                dm.Culvert,
                dm.Pump,
                dm.PumpMap,
                dm.Channel,
                dm.SurfaceMap,
                dm.DryWeatherFlowMap,
                dm.Lateral1D,
                dm.BoundaryCondition1D,
                dm.MeasureLocation,
            },
            dm.Channel: {dm.ConnectionNode, dm.CrossSectionLocation, dm.PotentialBreach, dm.Windshielding1D},
            dm.CrossSectionLocation: {dm.Channel},
            dm.PotentialBreach: {dm.Channel},
            dm.Windshielding1D: {dm.Channel},
            dm.MemoryControl: {dm.Pump, dm.Orifice, dm.Weir},
            dm.TableControl: {dm.Pump, dm.Orifice, dm.Weir},
            dm.MeasureMap: {dm.MemoryControl, dm.TableControl, dm.MeasureLocation},
        }
        for model_cls in dm.ALL_MODELS:
            if model_cls.__geometrytype__ == en.GeometryType.NoGeometry:
                continue
            if model_cls not in snap_groups:
                snap_groups[model_cls] = {model_cls, dm.ConnectionNode}
            else:
                snap_groups[model_cls].add(model_cls)
        return snap_groups

    def validate_layers(self, return_raw_errors=False):
        """Validate all layers registered within handlers."""
        fixed_errors, unsolved_errors = [], []
        handlers_count = len(self.model_handlers)
        msg = "Validating layers data..."
        self.uc.progress_bar(msg, 0, handlers_count, 0, clear_msg_bar=True)
        QCoreApplication.processEvents()
        for i, handler in enumerate(self.model_handlers.values(), start=1):
            fixed_validation_errors, unsorted_validation_errors = handler.validate_features()
            fixed_errors += fixed_validation_errors
            unsolved_errors += unsorted_validation_errors
            self.uc.progress_bar(msg, 0, handlers_count, i, clear_msg_bar=True)
            QCoreApplication.processEvents()
        self.uc.clear_message_bar()
        if return_raw_errors:
            return fixed_errors, unsolved_errors
        else:
            fixed_errors_message = validation_errors_summary(fixed_errors) if fixed_errors else ""
            unsolved_errors_message = validation_errors_summary(unsolved_errors) if unsolved_errors else ""
            return fixed_errors_message, unsolved_errors_message

    def on_active_layer_changed(self, layer):
        """Refresh snapping after active layer change."""
        self.reset_snapping()
        try:
            layer_handler = self.layer_handlers[layer.id()]
        except (KeyError, AttributeError):
            return
        self.set_layers_snapping(layer_handler)

    def set_layers_snapping(self, layer_handler):
        """Setting snapping rules."""
        layer_model = layer_handler.MODEL
        if layer_model not in self.snapping_groups:
            return
        snapped_layers = [self.model_handlers[linked_model].layer for linked_model in self.snapping_groups[layer_model]]
        use_topological_editing = layer_model == dm.ConnectionNode
        project = QgsProject.instance()
        project.setTopologicalEditing(use_topological_editing)
        snap_config = project.snappingConfig()
        snap_config.setMode(QgsSnappingConfig.AdvancedConfiguration)
        snap_config.setIntersectionSnapping(True)
        individual_configs = snap_config.individualLayerSettings()
        vertex_segment_snapping_models = {
            dm.CrossSectionLocation,
            dm.PotentialBreach,
            dm.TableControl,
            dm.MemoryControl,
        }
        try:
            snap_type = (
                Qgis.SnappingTypes(Qgis.SnappingType.Vertex | Qgis.SnappingType.Segment)
                if layer_model in vertex_segment_snapping_models
                else Qgis.SnappingType.Vertex
            )
        except AttributeError:
            # Backward compatibility for QGIS versions before introducing `Qgis.SnappingTypes`
            snap_type = (
                QgsSnappingConfig.VertexFlag | QgsSnappingConfig.SegmentFlag
                if layer_model in vertex_segment_snapping_models
                else QgsSnappingConfig.VertexFlag
            )
        for layer in snapped_layers:
            try:
                iconf = individual_configs[layer]
            except KeyError:
                continue
            iconf.setTolerance(10)
            iconf.setTypeFlag(snap_type)
            iconf.setUnits(QgsTolerance.Pixels)
            iconf.setEnabled(True)
            snap_config.setIndividualLayerSettings(layer, iconf)
        if snap_config.enabled() is False:
            snap_config.setEnabled(True)
        project.setSnappingConfig(snap_config)

    @staticmethod
    def reset_snapping():
        """Method used to reset snapping options to the default state."""
        project = QgsProject.instance()
        snap_config = project.snappingConfig()
        snap_config.reset()
        project.setSnappingConfig(snap_config)

    @property
    def common_editing_group(self):
        """Getting a group of models that should be edited simultaneously."""
        linked_models = (
            dm.MODEL_1D_ELEMENTS
            + dm.MODEL_1D2D_ELEMENTS
            + (
                dm.DryWeatherFlow,
                dm.DryWeatherFlowMap,
                dm.Surface,
                dm.SurfaceMap,
            )
            + dm.STRUCTURE_CONTROL_ELEMENTS
        )
        return linked_models

    @property
    def model_name(self):
        """Name of the model."""
        return os.path.basename(self.model_gpkg_path).rsplit(".", 1)[0]

    @cached_property
    def uuid(self) -> str:
        """Unique identifier for the schematisation within the plugin"""
        return str(uuid4())

    @cached_property
    def model_revision(self):
        """3Di model schematisation revision."""
        model_gpkg_path_obj = Path(self.model_gpkg_path)
        try:
            from threedi_mi_utils import LocalSchematisation

            model_files_dir = model_gpkg_path_obj.parents[2]  # 3Di model folder structure candidate
            local_schematisation = LocalSchematisation.initialize_from_location(
                model_files_dir, use_config_for_revisions=False
            )
            if local_schematisation is None or not local_schematisation.revisions:
                raise ValueError("No revisions found.")
            revision_folder = os.path.basename(model_gpkg_path_obj.parents[1])
            if revision_folder == "work in progress":
                revision = local_schematisation.wip_revision
            else:
                revision_number = int(re.findall(r"^revision (\d+)", revision_folder)[0])
                revision = local_schematisation.revisions[revision_number]
        except (ImportError, IndexError, ValueError):
            revision = None
        return revision

    @cached_property
    def detailed_model_name(self):
        """Detailed model name."""
        try:
            if self.model_revision is not None:
                from threedi_mi_utils import WIPRevision

                if isinstance(self.model_revision, WIPRevision):
                    detailed_name = f"{self.model_name} WIP"
                else:
                    detailed_name = f"{self.model_name} #{self.model_revision.number}"
            else:
                detailed_name = self.model_name
        except ImportError:
            detailed_name = self.model_name
        return detailed_name

    @property
    def main_group(self):
        """Main model group."""
        if self.model_revision is not None:
            model_group_name = f"3Di schematisation: {self.detailed_model_name}"
        else:
            model_group_name = f"3Di schematisation: {self.model_gpkg_path}"
        return model_group_name

    @property
    def group_names(self):
        """Names of User Layer groups."""
        names = tuple(group_name for group_name, model_elements in self.VECTOR_GROUPS + self.RASTER_GROUPS)
        return names

    @property
    def data_model_groups(self):
        """Data models to groups mapping."""
        data_model_groups = {}
        for group_name, model_elements in self.VECTOR_GROUPS:
            for model_cls in model_elements:
                data_model_groups[model_cls] = group_name
        return data_model_groups

    @staticmethod
    def register_custom_functions():
        """Register custom expression functions"""
        QgsExpression.registerFunction(cross_section_label)
        QgsExpression.registerFunction(cross_section_max_height)
        QgsExpression.registerFunction(cross_section_max_width)

    @staticmethod
    def unregister_custom_functions():
        """Unregister custom expression functions"""
        QgsExpression.unregisterFunction("cross_section_label")
        QgsExpression.unregisterFunction("diameter_label")
        QgsExpression.unregisterFunction("width_label")
        QgsExpression.unregisterFunction("cross_section_max_height")
        QgsExpression.unregisterFunction("cross_section_max_width")

    @cached_property
    def vector_style_configs(self):
        """Return vector layers style configurations."""
        return get_style_configurations()

    @property
    def nr_editable_layers(self):
        project_variable = ProjectVariableDict(name="nr_editable_layers")
        return project_variable[self.uuid]

    @nr_editable_layers.setter
    def nr_editable_layers(self, value):
        nr_editable_layers = ProjectVariableDict(name="nr_editable_layers")
        nr_editable_layers[self.uuid] = value

    def setup_all_value_relation_widgets(self):
        """Setup all models value relation widgets."""
        for parent_model_cls in self.VALUE_RELATIONS.keys():
            self.setup_value_relation_widgets(parent_model_cls)

    def setup_value_relation_widgets(self, model_cls):
        """Setup value relation widgets for the particular model class."""
        child_model_cls, parent_column, key_column, value_column = self.VALUE_RELATIONS[model_cls]
        parent_layer = self.model_handlers[model_cls].layer
        parent_column_idx = parent_layer.fields().lookupField(parent_column)
        child_layer = self.model_handlers[child_model_cls].layer
        default_ews = parent_layer.editorWidgetSetup(parent_column_idx)
        config = default_ews.config()
        config["Layer"] = child_layer.id()
        config["LayerSource"] = child_layer.source()
        config["Key"] = key_column
        config["Value"] = value_column
        config["AllowNull"] = True
        ews = QgsEditorWidgetSetup("ValueRelation", config)
        parent_layer.setEditorWidgetSetup(parent_column_idx, ews)

    def create_groups(self):
        """Creating all User Layers groups."""
        self.remove_groups()
        main_group = create_tree_group(self.main_group)
        for group_name in self.group_names:
            grp = create_tree_group(group_name, root=main_group)
            grp.setExpanded(False)
            self.spawned_groups[group_name] = grp

    def register_groups(self):
        """Registering all User Layers groups."""
        groups_registered = False
        project = QgsProject.instance()
        root = project.layerTreeRoot()
        main_group = root.findGroup(self.main_group)
        if not main_group:
            return groups_registered
        for group_name in self.group_names:
            grp = main_group.findGroup(group_name)
            if not grp:
                return groups_registered
            self.spawned_groups[group_name] = grp
        groups_registered = True
        return groups_registered

    def remove_groups(self):
        """Removing all User Layers groups."""
        self.remove_loaded_layers()
        remove_group_with_children(self.main_group)
        self.spawned_groups.clear()

    def get_layer_data_model(self, layer):
        """Return data model class for given layer."""
        for model_cls, handler in self.model_handlers.items():
            if handler.layer == layer:
                return model_cls
        return None

    def initialize_data_model_layer(self, model_cls):
        """Initializing single model layer based on data model class."""
        default_style_name = "default"
        layer = gpkg_layer(self.model_gpkg_path, model_cls.__tablename__, model_cls.__layername__)
        QgsExpressionContextUtils.setLayerVariable(layer, 'schematisation_uuid', self.uuid)
        layer_fields = layer.fields()
        fields_indexes = list(range(len(layer_fields)))
        form_ui_path = get_form_ui_path(model_cls.__tablename__)
        qml_main_dir = styles_location()
        style_manager = layer.styleManager()
        try:
            layer_style_config = self.vector_style_configs[model_cls.__tablename__]
            style_names = [
                style_name for style_name in layer_style_config.styles.keys() if style_name != default_style_name
            ]
            style_names.append(default_style_name)  # make sure default is last
            for style_name in style_names:
                style_categories = layer_style_config.styles[style_name]
                style_paths = [qml_main_dir / style_path for style_path in style_categories.values()]
                merged_qml = merge_qml_styles(style_paths)
                layer.loadNamedStyle(str(merged_qml))
                set_initial_layer_configuration(layer, model_cls)
                style_display_name = style_name.replace("_", " ")
                style_manager.addStyleFromLayer(style_display_name)
        except KeyError:
            pass
        all_styles = style_manager.styles()
        default_widgets_setup = [(idx, layer.editorWidgetSetup(idx)) for idx in fields_indexes]
        default_edit_form_config = layer.editFormConfig()
        if form_ui_path:
            default_edit_form_config.setUiForm(form_ui_path)
            try:
                default_edit_form_config.setInitCodeSource(Qgis.AttributeFormPythonInitCodeSource.Dialog)
            except AttributeError:
                try:
                    default_edit_form_config.setInitCodeSource(QgsEditFormConfig.PythonInitCodeSource.Dialog)
                except AttributeError:
                    default_edit_form_config.setInitCodeSource(QgsEditFormConfig.CodeSourceDialog)
            default_edit_form_config.setInitFunction("open_edit_form")
            default_edit_form_config.setInitCode("from threedi_schematisation_editor.utils import open_edit_form")
            set_field_default_value(layer, "id", "")
            if model_cls.__geometrytype__ == en.GeometryType.NoGeometry:
                set_field_default_value(layer, "id", "to_int(if (maximum(id) is null, 1, maximum(id) + 1))")
            else:
                set_field_default_value(layer, "id", "")
            for idx in fields_indexes:
                # We need to remove NotNull constraint for layers with the custom UI forms.
                # It is required to prevent QGIS messing with background validation stylesheet.
                layer.removeFieldConstraint(idx, QgsFieldConstraints.ConstraintNotNull)
        else:
            set_field_default_value(layer, "id", "to_int(if (maximum(id) is null, 1, maximum(id) + 1))")
        if "area" in layer_fields.names():
            set_field_default_value(layer, "area", "$area", apply_on_update=True)
        for style in all_styles:
            style_manager.setCurrentStyle(style)
            layer.setEditFormConfig(default_edit_form_config)
            for field_idx, field_widget_setup in default_widgets_setup:
                layer.setEditorWidgetSetup(field_idx, field_widget_setup)
        style_manager.setCurrentStyle(default_style_name)
        dm_groups = self.data_model_groups
        group_name = dm_groups[model_cls]
        add_layer_to_group(group_name, layer, bottom=True, cached_groups=self.spawned_groups)
        handler_cls = MODEL_HANDLERS[model_cls]
        handler = handler_cls(self, layer)
        handler.connect_handler_signals()
        self.model_handlers[model_cls] = handler
        self.layer_handlers[layer.id()] = handler

    def load_vector_layers(self):
        """Loading all vector layers."""
        msg = "Loading vector layers and styles..."
        layer_count = sum([len(group_models) for _, group_models in self.VECTOR_GROUPS])
        i = 0
        for group_name, group_models in self.VECTOR_GROUPS:
            for model_cls in group_models:
                msg = f"Loading {model_cls.__layername__} and its styles..."
                self.uc.progress_bar(msg, 0, layer_count, i, clear_msg_bar=True)
                QCoreApplication.processEvents()
                self.initialize_data_model_layer(model_cls)
                i += 1

    def register_vector_layers(self):
        """Register all vector layers."""
        layers_registered = False
        project = QgsProject.instance()
        present_layers = project.mapLayers()
        present_layers_sources = {lyr.dataProvider().dataSourceUri(): lyr for lyr in present_layers.values()}
        for group_name, group_models in self.VECTOR_GROUPS:
            for model_cls in group_models:
                layer_uri = f"{self.model_gpkg_path}|layername={model_cls.__tablename__}"
                layer_uri = layer_uri.replace("\\", "/")
                try:
                    layer = present_layers_sources[layer_uri]
                except KeyError:
                    return layers_registered
                handler_cls = MODEL_HANDLERS[model_cls]
                handler = handler_cls(self, layer)
                handler.connect_handler_signals()
                self.model_handlers[model_cls] = handler
                self.layer_handlers[layer.id()] = handler

    def load_raster_layers(self):
        """Loading all available raster layers."""
        gpkg_dir = os.path.dirname(self.model_gpkg_path)
        for group_name, group_models in self.RASTER_GROUPS:
            for model_cls in group_models:
                settings_layer = gpkg_layer(self.model_gpkg_path, model_cls.__tablename__)
                try:
                    feat = next(settings_layer.getFeatures())
                except StopIteration:
                    continue
                for raster_file_field, raster_layer_name in model_cls.RELATED_RASTERS:
                    relative_path = feat[raster_file_field]
                    if not relative_path:
                        continue
                    raster_filepath = os.path.normpath(os.path.join(gpkg_dir, "rasters", relative_path))
                    if not os.path.isfile(raster_filepath):
                        continue
                    rlayer = QgsRasterLayer(raster_filepath, raster_layer_name)
                    qml_path = get_qml_style_path(raster_file_field, "raster")
                    if qml_path is not None:
                        rlayer.loadNamedStyle(qml_path)
                    modify_raster_style(rlayer)
                    if raster_file_field == "dem_file":
                        hillshade_raster_layer = hillshade_layer(raster_filepath)
                        canvas = self.iface.mapCanvas()
                        canvas.setExtent(rlayer.extent())
                        add_layer_to_group(group_name, rlayer, cached_groups=self.spawned_groups)
                        add_layer_to_group(group_name, hillshade_raster_layer, cached_groups=self.spawned_groups)
                    else:
                        add_layer_to_group(group_name, rlayer, bottom=True, cached_groups=self.spawned_groups)

    def load_all_layers(self, from_project=False):
        """Creating/registering groups and loading/registering vector, raster and tabular layers."""
        self.register_custom_functions()
        self.nr_editable_layers = 0
        if not from_project:
            self.create_groups()
            self.load_vector_layers()
            self.load_raster_layers()
            self.add_joins()
        else:
            self.remove_loaded_layers(dry_remove=True)
            self.register_groups()
            self.register_vector_layers()
        self.setup_all_value_relation_widgets()
        self.iface.setActiveLayer(self.model_handlers[dm.ConnectionNode].layer)

    def remove_loaded_layers(self, dry_remove=False):
        """Removing loaded vector layers."""
        for model_cls, layer_handler in list(self.model_handlers.items()):
            try:
                layer_handler.disconnect_handler_signals()
                layer = layer_handler.layer
                if dry_remove is False:
                    remove_layer(layer)
            except RuntimeError:
                continue
        self.model_handlers.clear()
        self.layer_handlers.clear()
        self.spawned_groups.clear()

    def add_joins(self):
        """Setting joins between layers."""
        for parent_model_cls, children_data_models in self.LAYER_JOINS.items():
            try:
                parent_handler = self.model_handlers[parent_model_cls]
                parent_layer = parent_handler.layer
            except KeyError:
                continue
            for child_model_cls, join_specs in children_data_models.items():
                try:
                    child_handler = self.model_handlers[child_model_cls]
                    child_layer = child_handler.layer
                except KeyError:
                    continue
                child_join = QgsVectorLayerJoinInfo()
                child_join.setTargetFieldName(join_specs["target_field_name"])
                child_join.setJoinLayer(child_layer)
                child_join.setJoinFieldName(join_specs["join_field_name"])
                child_join.setUsingMemoryCache(True)
                child_join.setEditable(True)
                child_join.setPrefix(join_specs["prefix"])
                child_join.setJoinFieldNamesSubset(join_specs["join_field_names_subset"])
                parent_layer.addJoin(child_join)

    def get_layer_features(self, model_cls, filter_exp=None):
        """
        Get features from layer defined by the model class.
        If the filter_exp expression is defined, filter the feature list.
        """
        expr = QgsExpression(filter_exp) if filter_exp else None
        req = QgsFeatureRequest(expr) if expr is not None else QgsFeatureRequest()
        return self.model_handlers[model_cls].layer.getFeatures(req)

    def populate_edit_form(self, dialog, layer, feature):
        """Add extra logic to custom edit form of the layer."""
        self.form_factory.set_layer_form_logic(dialog, layer, feature)

    def model_modified(self):
        """Checking if any user layers were modified during work session."""
        modified = any(handler.layer_modified for handler in self.layer_handlers.values())
        return modified

    def stop_model_editing(self):
        """Stop editing session for the all layers within a model."""
        for handler in self.layer_handlers.values():
            handler.on_rollback()
