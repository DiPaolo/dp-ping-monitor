from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QMainWindow

from dp_ping_monitor.gui import logger
from dp_ping_monitor.gui import settings
from dp_ping_monitor.gui.settings import SettingsKey
from dp_ping_monitor.gui.ui.ui_log_window import Ui_LogWindow


class LogWindow(QMainWindow):
    visibility_changed = Signal(bool)

    def __init__(self, parent: QWidget = None):
        super(LogWindow, self).__init__(parent,
                                        flags=Qt.WindowType.WindowCloseButtonHint)

        self.ui = Ui_LogWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        # self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)

        # restore position and state
        # self.setWindowState(
        #     settings.get_settings_byte_array_value(SettingsKey.LOG_WINDOW_STATE, QtCore.Qt.WindowNoState))
        self.restoreGeometry(settings.get_settings_byte_array_value(SettingsKey.LOG_WINDOW_GEOMETRY))

        # log; setup it before setting it as a target for logger
        header = self.ui.log_list.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)

        logger.set_log_widget(self.ui.log_list)

        self.ui.clear.clicked.connect(lambda: self.ui.log_list.clear())
        self.ui.close.clicked.connect(lambda: self.setHidden(True))

    def showEvent(self, event):
        self.visibility_changed.emit(True)

    def hideEvent(self, event):
        self.visibility_changed.emit(False)

    def closeEvent(self, event):
        logger.info('Closing log window...')

        # save window position and size
        settings.set_settings_byte_array_value(SettingsKey.LOG_WINDOW_GEOMETRY, self.saveGeometry())
        # settings.set_settings_byte_array_value(SettingsKey.LOG_WINDOW_STATE, self.windowState())
