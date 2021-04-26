from qgis.PyQt.QtCore import NULL

from .base_edit_form import BaseEditForm
import threedi_model_builder.data_models as dm


class PipeEditForm(BaseEditForm):
    """Pipe user layer edit form logic."""
    MODEL = dm.Pipe

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.feature.id() < 0:
            return  # form open for an invalid feature
        cross_section_id = self.feature["cross_section_definition_id"]
        if cross_section_id not in (None, NULL):
            cross_section_feats = self.layer_manager.get_layer_features(dm.CrossSectionDefinition, f'"id" = {cross_section_id}')
            if cross_section_feats.isValid():
                cross_section_feat = next(cross_section_feats)
                if cross_section_feat.isValid():
                    self.populate_widgets(dm.CrossSectionDefinition, cross_section_feat)
