from types import MappingProxyType
from threedi_model_builder.forms.base_edit_form import BaseEditForm
from threedi_model_builder.utils import find_linestring_nodes
import threedi_model_builder.data_models as dm


class PipeEditForm(BaseEditForm):
    """Pipe user layer edit form logic."""

    MODEL = dm.Pipe
    FOREIGN_MODEL_FIELDS = MappingProxyType(
        {
            "connection_node_1_id": dm.ConnectionNode,
            "connection_node_1_initial_waterlevel": dm.ConnectionNode,
            "connection_node_1_storage_area": dm.ConnectionNode,
            "connection_node_1_code": dm.ConnectionNode,
            "connection_node_2_id": dm.ConnectionNode,
            "connection_node_2_initial_waterlevel": dm.ConnectionNode,
            "connection_node_2_storage_area": dm.ConnectionNode,
            "connection_node_2_code": dm.ConnectionNode,
            "manhole_1_id": dm.Manhole,
            "manhole_1_code": dm.Manhole,
            "manhole_1_display_name": dm.Manhole,
            "manhole_1_calculation_type": dm.Manhole,
            "manhole_1_shape": dm.Manhole,
            "manhole_1_width": dm.Manhole,
            "manhole_1_length": dm.Manhole,
            "manhole_1_bottom_level": dm.Manhole,
            "manhole_1_surface_level": dm.Manhole,
            "manhole_1_drain_level": dm.Manhole,
            "manhole_1_manhole_indicator": dm.Manhole,
            "manhole_1_zoom_category": dm.Manhole,
            "manhole_2_id": dm.Manhole,
            "manhole_2_code": dm.Manhole,
            "manhole_2_display_name": dm.Manhole,
            "manhole_2_calculation_type": dm.Manhole,
            "manhole_2_shape": dm.Manhole,
            "manhole_2_width": dm.Manhole,
            "manhole_2_length": dm.Manhole,
            "manhole_2_bottom_level": dm.Manhole,
            "manhole_2_surface_level": dm.Manhole,
            "manhole_2_drain_level": dm.Manhole,
            "manhole_2_manhole_indicator": dm.Manhole,
            "manhole_2_zoom_category": dm.Manhole,
            "cross_section_definition_shape": dm.CrossSectionDefinition,
            "cross_section_definition_width": dm.CrossSectionDefinition,
            "cross_section_definition_height": dm.CrossSectionDefinition,
            "cross_section_definition_code": dm.CrossSectionDefinition,
        }
    )

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        # Cross section definition
        self.populate_cross_section_definition()
        # Manholes for start and end points
        if self.new_feature is True:
            self.populate_manholes_on_creation()
        else:
            self.populate_manholes_on_edit()

    def populate_cross_section_definition(self):
        cross_section_def_handler = self.layer_manager.loaded_models[dm.CrossSectionDefinition]
        cross_section_def_feat = cross_section_def_handler.get_feat_by_id(self.feature["cross_section_definition_id"])
        if cross_section_def_feat is not None:
            self.populate_widgets(data_model_cls=dm.CrossSectionDefinition, feature=cross_section_def_feat)

    def populate_manholes_on_edit(self):
        connection_node_handler = self.layer_manager.loaded_models[dm.ConnectionNode]
        for name, modifier in (("start", 1), ("end", 2)):
            connection_node_id = self.feature[f"connection_node_{name}_id"]
            if connection_node_id:
                connection_node_feat = connection_node_handler.get_feat_for_node_id(connection_node_id)
                manhole_feat = connection_node_handler.get_manhole_feat_for_node_id(connection_node_id)
                if manhole_feat is not None:
                    self.populate_widgets(
                        data_model_cls=dm.ConnectionNode,
                        feature=connection_node_feat,
                        start_end_modifier=modifier,
                    )
                    self.populate_widgets(
                        data_model_cls=dm.Manhole,
                        feature=manhole_feat,
                        start_end_modifier=modifier,
                    )

    def populate_manholes_on_creation(self):
        connection_node_handler = self.layer_manager.loaded_models[dm.ConnectionNode]
        manhole_handler = self.layer_manager.loaded_models[dm.Manhole]
        linestring = self.feature.geometry().asPolyline()
        start_manhole_feat, end_manhole_feat = find_linestring_nodes(linestring, manhole_handler.layer)
        for name, modifier, manhole_feat in (("start", 1, start_manhole_feat), ("end", 2, end_manhole_feat)):
            if manhole_feat is None:
                continue
            connection_node_id = manhole_feat["connection_node_id"]
            connection_node_feat = connection_node_handler.get_feat_for_node_id(connection_node_id)
            self.feature[f"connection_node_{name}_id"] = connection_node_id
            self.populate_widgets(
                data_model_cls=dm.ConnectionNode,
                feature=connection_node_feat,
                start_end_modifier=modifier,
            )
            self.populate_widgets(
                data_model_cls=dm.Manhole,
                feature=manhole_feat,
                start_end_modifier=modifier,
                )
        self.populate_widgets()
