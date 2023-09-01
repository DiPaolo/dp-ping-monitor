import logging
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from dp_ping_monitor.config import config
# from dp_ping_monitor.app import init_app, deinit_app
from dp_ping_monitor.gui.main_dialog import MainDialog

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

QCoreApplication.setOrganizationName(config.organization_name)
QCoreApplication.setOrganizationDomain(config.organization_domain)
QCoreApplication.setApplicationName(config.application_name)

app = QApplication(sys.argv)

# init_app()

mainDlg = MainDialog()
mainDlg.show()

ret_code = app.exec()

# deinit_app()

sys.exit(ret_code)
