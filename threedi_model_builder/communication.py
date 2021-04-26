# Copyright (C) 2021 by Lutra Consulting
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QMessageBox, QInputDialog
from qgis.core import Qgis, QgsMessageLog


class UICommunication(object):
    """Class with methods for handling messages using QGIS interface."""

    def __init__(self, iface, context):
        self.iface = iface
        self.context = context
        self.message_bar = self.iface.messageBar()

    def show_info(self, msg, parent=None, context=None):
        """Showing info dialog."""
        if self.iface is not None:
            parent = parent if parent is not None else self.iface.mainWindow()
            context = self.context if context is None else context
            QMessageBox.information(parent, context, msg)
        else:
            print(msg)

    def show_warn(self, msg, parent=None, context=None):
        """Showing warning dialog."""
        if self.iface is not None:
            parent = parent if parent is not None else self.iface.mainWindow()
            context = self.context if context is None else context
            QMessageBox.warning(parent, context, msg)
        else:
            print(msg)

    def show_error(self, msg, parent=None, context=None):
        """Showing error dialog."""
        if self.iface is not None:
            parent = parent if parent is not None else self.iface.mainWindow()
            context = self.context if context is None else context
            QMessageBox.critical(parent, context, msg)
        else:
            print(msg)

    def bar_info(self, msg, dur=5):
        """Showing info message bar."""
        if self.iface is not None:
            self.message_bar.pushMessage(self.context, msg, level=Qgis.Info, duration=dur)
        else:
            print(msg)

    def bar_warn(self, msg, dur=5):
        """Showing warning message bar."""
        if self.iface is not None:
            self.message_bar.pushMessage(self.context, msg, level=Qgis.Warning, duration=dur)
        else:
            print(msg)

    def bar_error(self, msg, dur=5):
        """Showing error message bar."""
        if self.iface is not None:
            self.message_bar.pushMessage(self.context, msg, level=Qgis.Critical, duration=dur)
        else:
            print(msg)

    @staticmethod
    def ask(widget, title, question, box_icon=QMessageBox.Question):
        """Ask for operation confirmation."""
        msg_box = QMessageBox(widget)
        msg_box.setIcon(box_icon)
        msg_box.setWindowTitle(title)
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(question)
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.No)
        res = msg_box.exec_()
        if res == QMessageBox.No:
            return False
        else:
            return True

    def pick_item(self, title, message, parent=None, *items):
        """Getting item from list of items."""
        parent = parent if parent is not None else self.iface.mainWindow()
        item, accept = QInputDialog.getItem(parent, title, message, items, editable=False)
        if accept is False:
            return None
        return item

    def log_msg(self, msg, level=Qgis.Info):
        """Log the message to QGIS log with a given level."""
        QgsMessageLog.logMessage(msg, self.context, level)

    def log_warn(self, msg):
        """Log the warning to QGIS logs."""
        self.log_msg(msg, level=Qgis.Warning)

    def log_info(self, msg):
        """Log the info message to QGIS logs."""
        self.log_msg(msg, level=Qgis.Info)

