# Copyright (C) 2021 by Lutra Consulting
import os
import threedi_model_builder.data_models as dm
from types import MappingProxyType
from qgis.core import QgsExpression, QgsFeatureRequest, QgsRasterLayer, QgsVectorLayerJoinInfo, QgsMapLayer
from threedi_model_builder.user_layer_handlers import MODEL_HANDLERS
from threedi_model_builder.user_layer_forms import LayerEditFormFactory
from threedi_model_builder.utils import (
    gpkg_layer,
    get_form_ui_path,
    get_qml_style_path,
    create_tree_group,
    add_layer_to_group,
    remove_group_with_children,
    remove_layer,
)


class LayersManager:
    """Class with methods and attributes used for managing 3Di User Layers."""

    VECTOR_GROUPS = (
        ("1D", dm.MODEL_1D_ELEMENTS),
        ("2D", dm.MODEL_2D_ELEMENTS),
        ("Inflow", dm.INFLOW_ELEMENTS),
        ("Settings", dm.SETTINGS_ELEMENTS),
    )
    RASTER_GROUPS = (("Model rasters", dm.ELEMENTS_WITH_RASTERS),)

    LAYER_JOINS = MappingProxyType({
        dm.CrossSectionLocation: {
            dm.CrossSectionDefinition: {
                "target_field_name": "cross_section_definition_id",
                "join_field_name": "id",
                "prefix": "cross_section_definition_",
                "join_field_names_subset": ("code", "width", "height", "shape")
            },
        },
    })

    def __init__(self, iface, user_communication, model_gpkg_path):
        self.iface = iface
        self.uc = user_communication
        self.model_gpkg_path = model_gpkg_path
        self.form_factory = LayerEditFormFactory(self)
        self.model_handlers = {}
        self.layer_handlers = {}
        self.active_form_signals = set()

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

    def create_groups(self):
        """Creating all User Layers groups."""
        self.remove_groups()
        main_group = create_tree_group(self.main_group)
        for group_name in self.group_names:
            grp = create_tree_group(group_name, root=main_group)
            grp.setExpanded(False)

    def remove_groups(self):
        """Removing all User Layers groups."""
        self.remove_loaded_layers()
        remove_group_with_children(self.main_group)

    def get_layer_data_model(self, layer):
        """Return data model class for given layer."""
        for model_cls, handler in self.model_handlers.items():
            if handler.layer == layer:
                return model_cls
        return None

    def initialize_data_model_layer(self, model_cls):
        """Initializing single model layer based on data model class."""
        layer = gpkg_layer(self.model_gpkg_path, model_cls.__tablename__, model_cls.__layername__)
        qml_path = get_qml_style_path(model_cls.__tablename__)
        if qml_path is not None:
            layer.loadNamedStyle(qml_path)
        attr_table_config = layer.attributeTableConfig()
        columns = attr_table_config.columns()
        for column in columns:
            if column.name == "fid":
                column.hidden = True
                break
        attr_table_config.setColumns(columns)
        layer.setAttributeTableConfig(attr_table_config)
        form_ui_path = get_form_ui_path(model_cls.__tablename__)
        if form_ui_path:
            form_config = layer.editFormConfig()
            form_config.setUiForm(form_ui_path)
            layer.setEditFormConfig(form_config)
        dm_groups = self.data_model_groups
        group_name = dm_groups[model_cls]
        add_layer_to_group(group_name, layer, bottom=True)
        layer.setFlags(QgsMapLayer.Searchable | QgsMapLayer.Identifiable)
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
                    add_layer_to_group(group_name, rlayer, bottom=True)

    def load_all_layers(self):
        """Creating groups and loading vector, raster and tabular layers."""
        self.create_groups()
        self.load_vector_layers()
        self.load_raster_layers()
        self.add_joins()

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
