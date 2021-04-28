from types import MappingProxyType
from .base_edit_form import BaseEditForm
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
        if self.feature.id() < 0:
            return  # form open for an invalid feature

        # Cross section definition
        cross_section_def_handler = self.layer_manager.loaded_models[dm.CrossSectionDefinition]
        cross_section_def_feat = cross_section_def_handler.get_feat_by_id(self.feature["cross_section_definition_id"])
        if cross_section_def_feat is not None:
            self.populate_widgets(data_model_cls=dm.CrossSectionDefinition, feature=cross_section_def_feat)

        # Manholes for start and end points
        for name, modifier in (("start", 1), ("end", 2)):
            connection_node_handler = self.layer_manager.loaded_models[dm.ConnectionNode]
            connection_node_id = self.feature[f"connection_node_{name}_id"]
            manhole_feat = connection_node_handler.get_manhole_feat_for_node_id(connection_node_id)
            if manhole_feat is not None:
                self.populate_widgets(
                    data_model_cls=dm.Manhole,
                    feature=manhole_feat,
                    start_end_modifier=modifier,
                )
