from pathlib import Path

from qgis.core import QgsSettings
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QItemSelectionModel, Qt
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel

ui_path = Path(__file__).parent.joinpath("ui")
load_basecls, load_uicls = uic.loadUiType(ui_path.joinpath("load_schematisation.ui"))


class LoadSchematisationDialog(load_basecls, load_uicls):
    """Dialog for loading schematisation."""

    def __init__(self, uc, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.uc = uc
        self.schematisation_model = QStandardItemModel()
        self.schematisation_tv.setModel(self.schematisation_model)
        self.schematisation_list_header = ["Schematisation", "Revision"]
        self.settings = QgsSettings()
        self.working_dir = self.settings.value("threedi/working_dir", "", type=str)
        if self.working_dir:
            self.file_browse_widget.setDefaultRoot(self.working_dir)
        self.selected_schematisation_filepath = None
        self.schematisation_tv.doubleClicked.connect(self.set_schematisation_filepath)
        self.load_pb.clicked.connect(self.set_schematisation_filepath)
        self.cancle_pb.clicked.connect(self.reject)
        self.list_working_dir_schematisations()

    def list_working_dir_schematisations(self):
        """Populate 3Di Working Directory schematisations."""
        try:
            from threedi_mi_utils import (
                WIPRevision,
                list_local_schematisations,
                replace_revision_data,
            )
        except ImportError:
            self.missing_lib_label.setHidden(False)
            return
        self.missing_lib_label.setHidden(True)
        if not self.working_dir:
            return
        self.schematisation_model.clear()
        self.schematisation_model.setHorizontalHeaderLabels(
            self.schematisation_list_header
        )
        local_schematisations = list_local_schematisations(
            self.working_dir, use_config_for_revisions=False
        )
        last_used_schematisation_dir = self.settings.value(
            "threedi/last_schematisation_folder", ""
        )
        last_used_schematisation_row_number = None
        for local_schematisation in local_schematisations.values():
            local_schematisation_name = local_schematisation.name
            wip_revision = local_schematisation.wip_revision
            try:
                wip_revision_db = wip_revision.schematisation_db_filepath
            except (AttributeError, FileNotFoundError):
                wip_revision_db = None
            if wip_revision_db is not None:
                schematisation_name_item = QStandardItem(local_schematisation_name)
                revision_number_str = f"{wip_revision.number} (work in progress)"
                revision_number_item = QStandardItem(revision_number_str)
                revision_number_item.setData(wip_revision_db, Qt.UserRole)
                self.schematisation_model.appendRow(
                    [schematisation_name_item, revision_number_item]
                )
                if wip_revision.schematisation_dir == last_used_schematisation_dir:
                    last_used_schematisation_row_number = (
                        self.schematisation_model.rowCount() - 1
                    )
            for revision_number, revision in local_schematisation.revisions.items():
                try:
                    revision_db = revision.schematisation_db_filepath
                    if revision_db is None:
                        continue
                except FileNotFoundError:
                    continue
                schematisation_name_item = QStandardItem(local_schematisation_name)
                revision_number_item = QStandardItem(str(revision.number))
                revision_number_item.setData(revision_db, Qt.UserRole)
                self.schematisation_model.appendRow(
                    [schematisation_name_item, revision_number_item]
                )
                if revision.schematisation_dir == last_used_schematisation_dir:
                    last_used_schematisation_row_number = (
                        self.schematisation_model.rowCount() - 1
                    )
        for i in range(len(self.schematisation_list_header)):
            self.schematisation_tv.resizeColumnToContents(i)
        if last_used_schematisation_row_number is not None:
            last_used_schematisation_row_idx = self.schematisation_model.index(
                last_used_schematisation_row_number, 0
            )
            self.schematisation_tv.selectionModel().setCurrentIndex(
                last_used_schematisation_row_idx, QItemSelectionModel.ClearAndSelect
            )
            self.schematisation_tv.scrollTo(last_used_schematisation_row_idx)

    def set_schematisation_filepath(self):
        """Set selected schematisation filepath."""
        if self.load_tab.currentIndex() == 0:
            index = self.schematisation_tv.currentIndex()
            if not index.isValid():
                self.uc.show_warn(
                    "Nothing selected. Please select schematisation revision to continue.",
                    parent=self,
                )
                return
            current_row = index.row()
            revision_item = self.schematisation_model.item(current_row, 1)
            revision_db = revision_item.data(Qt.UserRole)
            self.selected_schematisation_filepath = revision_db
        else:
            selected_filepath = self.file_browse_widget.filePath()
            if not selected_filepath:
                self.uc.show_warn(
                    "No file selected. Please select schematisation file to continue.",
                    parent=self,
                )
                return
            self.selected_schematisation_filepath = self.file_browse_widget.filePath()
        self.accept()
