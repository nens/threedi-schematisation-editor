from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTabWidget,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from threedi_schematisation_editor.vector_data_importer.dialogs.utils import create_font


class WizardPage(QWidget):
    def __init__(self, parent=None, next_button=True, previous_button=True, stop_button=True, stop_name="Cancel"):
        super().__init__(parent)
        font = create_font(self, 10)
        self.setFont(font)
        self.setup_ui(next_button, previous_button, stop_button, stop_name)

    def setup_ui(self, next_button: bool, previous_button: bool, stop_button: bool, stop_name: str = "Cancel"):
        # Create navigation buttons
        button_layout = QHBoxLayout(self)
        if previous_button:
            previous_button = QPushButton("Previous")
            button_layout.addWidget(previous_button)
        if next_button:
            next_button = QPushButton("Next")
            button_layout.addWidget(next_button)
        if stop_button:
            stop_button = QPushButton(stop_name)
            stop_button.clicked.connect(self.close)
            button_layout.addWidget(stop_button)


class BaseWizard(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        font = create_font(self, 10)
        self.setFont(font)
        self.pages = [WizardPage(parent=self, next_button=True, previous_button=False, stop_button=True, stop_name="Cancel"),
                      WizardPage(parent=self, next_button=False, previous_button=True, stop_button=True, stop_name="Stop")]
        self.current_index = 0
        self.setup_ui(next_button, previous_button, stop_button, stop_name)

    def setup_ui(self):
        # Setup window
        self.setWindowTitle("Import {}s")
        self.resize(1000, 750)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.addLayout(self.pages[self.current_index], self.gridLayout.rowCount(), 0, 1, -1)

    def next_page(self):
        if self.current_index < len(self.pages) - 1:
            self.current_index += 1
            self.pages[self.current_index].show()


    def setup_ui(self, next_button: bool, previous_button: bool, stop_button: bool, stop_name: str = "Cancel"):
        # Setup window
        self.setWindowTitle("Import {}s")
        self.resize(1000, 750)
        self.gridLayout = QGridLayout(self)
        # Create navigation buttons
        button_layout = QHBoxLayout()
        if previous_button:
            previous_button = QPushButton("Previous")
            button_layout.addWidget(previous_button)
        if next_button:
            next_button = QPushButton("Next")
            button_layout.addWidget(next_button)
        if stop_button:
            stop_button = QPushButton(stop_name)
            stop_button.clicked.connect(self.close)
            button_layout.addWidget(stop_button)
        self.gridLayout.addLayout(button_layout, self.gridLayout.rowCount(), 0, 1, -1)

