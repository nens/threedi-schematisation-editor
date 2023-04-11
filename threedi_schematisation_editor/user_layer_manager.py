# Copyright (C) 2023 by Lutra Consulting
import os
from types import MappingProxyType

from qgis.core import (
    Qgis,
    QgsExpression,
    QgsFeatureRequest,
    QgsProject,
    QgsRasterLayer,
    QgsSnappingConfig,
    QgsTolerance,
    QgsVectorLayerJoinInfo,
)
from qgis.PyQt.QtCore import QCoreApplication

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.expressions import (
    cross_section_label,
    cross_section_max_height,
    cross_section_max_width,
)
from threedi_schematisation_editor.user_layer_forms import LayerEditFormFactory
from threedi_schematisation_editor.user_layer_handlers import MODEL_HANDLERS
from threedi_schematisation_editor.utils import (
    add_layer_to_group,
    create_tree_group,
    get_form_ui_path,
    get_multiple_qml_style_paths,
    get_qml_style_path,
    gpkg_layer,
    hillshade_layer,
    modify_raster_style,
    remove_group_with_children,
    remove_layer,
    set_field_default_value,
    set_initial_layer_configuration,
    validation_errors_summary,
)


class LayersManager:
    """Class with methods and attributes used for managing 3Di User Layers."""

    VECTOR_GROUPS = (
        ("1D", dm.MODEL_1D_ELEMENTS),
        ("1D2D", dm.MODEL_1D2D_ELEMENTS),
        ("2D", dm.MODEL_2D_ELEMENTS),
        ("Inflow", dm.INFLOW_ELEMENTS),
        ("Settings", dm.SETTINGS_ELEMENTS),
    )
    RASTER_GROUPS = (("Model rasters", dm.ELEMENTS_WITH_RASTERS),)

    LAYER_JOINS = MappingProxyType({})

    TOPOLOGICAL_EDITING_GROUPS = MappingProxyType(
        {
            dm.ConnectionNode: (
                dm.Manhole,
                dm.Pipe,
                dm.Weir,
                dm.Orifice,
                dm.Culvert,
                dm.Pumpstation,
                dm.PumpstationMap,
                dm.Channel,
                dm.SurfaceMap,
                dm.ImperviousSurfaceMap,
                dm.Lateral1D,
                dm.BoundaryCondition1D,
            ),
            dm.Manhole: (
                dm.ConnectionNode,
                dm.Pipe,
                dm.Weir,
                dm.Orifice,
                dm.Culvert,
                dm.Pumpstation,
                dm.PumpstationMap,
                dm.Channel,
                dm.SurfaceMap,
                dm.ImperviousSurfaceMap,
                dm.Lateral1D,
                dm.BoundaryCondition1D,
            ),
            dm.Channel: (
                dm.ConnectionNode,
                dm.CrossSectionLocation,
                dm.PotentialBreach,
            ),
            dm.CrossSectionLocation: (dm.Channel,),
            dm.PotentialBreach: (dm.Channel,),
        }
    )

    def __init__(self, iface, user_communication, model_gpkg_path):
        self.iface = iface
        self.uc = user_communication
        self.model_gpkg_path = model_gpkg_path
        self.form_factory = LayerEditFormFactory(self)
        self.model_handlers = {}
        self.layer_handlers = {}
        self.spawned_groups = {}
        self.active_form_signals = set()
        self.iface.currentLayerChanged.connect(self.on_active_layer_changed)

    def validate_layers(self, return_raw_errors=False):
        """Validate all layers registered within handlers."""
        fixed_errors, unsolved_errors = [], []
        handlers_count = len(self.model_handlers)
        msg = "Validating data before the export..."
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
        active_layer = layer_handler.layer
        layer_model = layer_handler.MODEL
        snapped_layers = [active_layer]
        if layer_model in self.TOPOLOGICAL_EDITING_GROUPS:
            snapped_layers += [
                self.model_handlers[linked_model].layer for linked_model in self.TOPOLOGICAL_EDITING_GROUPS[layer_model]
            ]
            use_topological_editing = True if layer_model != dm.Channel else False
        else:
            if layer_model != dm.ConnectionNode:
                connection_node_layer = self.model_handlers[dm.ConnectionNode].layer
                snapped_layers.append(connection_node_layer)
            use_topological_editing = False
        project = QgsProject.instance()
        project.setTopologicalEditing(use_topological_editing)
        snap_config = project.snappingConfig()
        snap_config.setMode(QgsSnappingConfig.AdvancedConfiguration)
        snap_config.setIntersectionSnapping(True)
        individual_configs = snap_config.individualLayerSettings()
        try:
            snap_type = (
                Qgis.SnappingTypes(Qgis.SnappingType.Vertex | Qgis.SnappingType.Segment)
                if layer_model == dm.PotentialBreach
                else Qgis.SnappingType.Vertex
            )
        except AttributeError:
            # Backward compatibility for QGIS versions before introducing `Qgis.SnappingTypes`
            snap_type = (
                QgsSnappingConfig.VertexFlag | QgsSnappingConfig.SegmentFlag
                if layer_model == dm.PotentialBreach
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
                dm.ImperviousSurface,
                dm.ImperviousSurfaceMap,
                dm.Surface,
                dm.SurfaceMap,
            )
        )
        return linked_models

    @property
    def main_group(self):
        """Main model group."""
        model_file_dir = os.path.basename(os.path.dirname(self.model_gpkg_path))
        model_name = os.path.basename(self.model_gpkg_path).rsplit(".", 1)[0]
        model_group_name = f"3Di model: {model_file_dir}/{model_name}"
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
        fields_indexes = list(range(len(layer.fields())))
        form_ui_path = get_form_ui_path(model_cls.__tablename__)
        qml_paths = get_multiple_qml_style_paths(model_cls.__tablename__, "vector")
        qml_names = [os.path.basename(qml_path).split(".")[0] for qml_path in qml_paths]
        try:
            default_idx = qml_names.index(default_style_name)
            qml_paths.append(qml_paths.pop(default_idx))
            qml_names.append(qml_names.pop(default_idx))
        except ValueError:
            # There is no default.qml style defined for the model layer
            pass
        style_manager = layer.styleManager()
        for style_name, qml_path in zip(qml_names, qml_paths):
            layer.loadNamedStyle(qml_path)
            set_initial_layer_configuration(layer, model_cls)
            style_manager.addStyleFromLayer(style_name)
        all_styles = style_manager.styles()
        default_widgets_setup = [(idx, layer.editorWidgetSetup(idx)) for idx in fields_indexes]
        default_edit_form_config = layer.editFormConfig()
        if form_ui_path:
            default_edit_form_config.setUiForm(form_ui_path)
        else:
            if model_cls != dm.SchemaVersion:
                id_increment_expression = "if (maximum(id) is null, 1, maximum(id) + 1)"
                set_field_default_value(layer, "id", id_increment_expression)
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
        for group_name, group_models in self.VECTOR_GROUPS:
            for model_cls in group_models:
                self.initialize_data_model_layer(model_cls)

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
                    raster_filepath = os.path.normpath(os.path.join(gpkg_dir, relative_path))
                    if not os.path.isfile(raster_filepath):
                        continue
                    rlayer = QgsRasterLayer(raster_filepath, raster_layer_name)
                    qml_path = get_qml_style_path(raster_file_field, "raster")
                    if qml_path is not None:
                        rlayer.loadNamedStyle(qml_path)
                    modify_raster_style(rlayer)
                    add_layer_to_group(group_name, rlayer, bottom=True, cached_groups=self.spawned_groups)
                    if raster_file_field == "dem_file":
                        hillshade_raster_layer = hillshade_layer(raster_filepath)
                        add_layer_to_group(group_name, hillshade_raster_layer, cached_groups=self.spawned_groups)

    def load_all_layers(self, from_project=False):
        """Creating/registering groups and loading/registering vector, raster and tabular layers."""
        self.register_custom_functions()
        if not from_project:
            self.create_groups()
            self.load_vector_layers()
            self.load_raster_layers()
            self.add_joins()
        else:
            self.remove_loaded_layers(dry_remove=True)
            self.register_groups()
            self.register_vector_layers()

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
