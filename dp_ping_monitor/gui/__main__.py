import logging
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from dp_ping_monitor.config import config
# from dp_ping_monitor.app import init_app, deinit_app
from dp_ping_monitor.gui.main_dialog import MainDialog
from dp_ping_monitor.gui.ui.dp_ping_monitor import qInitResources

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

QCoreApplication.setOrganizationName(config.organization_name)
QCoreApplication.setOrganizationDomain(config.organization_domain)
QCoreApplication.setApplicationName(config.application_name)

app = QApplication(sys.argv)

# call it explicitly because otherwise (if just included)
# IDE tries to optimize imports, so will remove it
qInitResources()
app.setWindowIcon(QIcon(':/icons/app_icon.png'))

mainDlg = MainDialog()
mainDlg.show()

ret_code = app.exec()

sys.exit(ret_code)
