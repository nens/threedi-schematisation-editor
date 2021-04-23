# Copyright (C) 2021 by Lutra Consulting
import os
from qgis.core import QgsRasterLayer
import threedi_model_builder.data_models as dm
from threedi_model_builder.user_layer_handlers import MODEL_HANDLERS
from threedi_model_builder.utils import (
    gpkg_layer,
    get_qml_style_path,
    get_tree_group,
    add_layer_to_group,
    remove_group_with_children,
    remove_layer,
)


class LayersManager:
    VECTOR_GROUPS = (
        ("1D", dm.MODEL_1D_ELEMENTS),
        ("2D", dm.MODEL_2D_ELEMENTS),
        ("Inflow", dm.INFLOW_ELEMENTS),
        ("Settings", dm.SETTINGS_ELEMENTS),
    )
    RASTER_GROUPS = (
        ("Model rasters", dm.ELEMENTS_WITH_RASTERS),
    )

    def __init__(self, iface, user_communication, model_gpkg_path):
        self.iface = iface
        self.uc = user_communication
        self.model_gpkg_path = model_gpkg_path
        self.loaded_models = {}
        self.loaded_rasters = {}

    @property
    def group_names(self):
        names = tuple(group_name for group_name, model_elements in self.VECTOR_GROUPS + self.RASTER_GROUPS)
        return names

    @property
    def data_model_groups(self):
        data_model_groups = {}
        for group_name, model_elements in self.VECTOR_GROUPS:
            for model_cls in model_elements:
                data_model_groups[model_cls] = group_name
        return data_model_groups

    def initialize_data_model_layer(self, model_cls):
        layer = gpkg_layer(self.model_gpkg_path, model_cls.__tablename__, model_cls.__layername__)
        qml_path = get_qml_style_path(model_cls.__tablename__)
        if qml_path is not None:
            layer.loadNamedStyle(qml_path)
        dm_groups = self.data_model_groups
        group_name = dm_groups[model_cls]
        add_layer_to_group(group_name, layer, bottom=True)
        handler_cls = MODEL_HANDLERS[model_cls]
        handler = handler_cls(layer, self.uc)
        # TODO: This should be turned on after handler methods implementation
        # handler.connect_handler_signals()
        self.loaded_models[model_cls] = handler

    def load_all_layers(self):
        self.create_groups()
        self.load_vector_layers()
        self.load_raster_layers()

    def load_vector_layers(self):
        for group_name, group_models in self.VECTOR_GROUPS:
            for model_cls in group_models:
                self.initialize_data_model_layer(model_cls)

    def load_raster_layers(self):
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

    def create_groups(self):
        self.remove_groups()
        for group_name in self.group_names:
            get_tree_group(group_name, create=True)

    def remove_groups(self):
        self.remove_loaded_layers()
        for group_name in self.group_names:
            grp = get_tree_group(group_name, create=False)
            if grp:
                remove_group_with_children(group_name)

    def remove_loaded_layers(self):
        for model_cls, layer_handler in list(self.loaded_models.items()):
            # TODO: This should be turned on after handler methods implementation
            # layer_handler.disconnect_handler_signals()
            layer = layer_handler.layer
            remove_layer(layer)
            del self.loaded_models[model_cls]
