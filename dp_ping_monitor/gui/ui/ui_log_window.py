# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHeaderView,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_LogWindow(object):
    def setupUi(self, LogWindow):
        if not LogWindow.objectName():
            LogWindow.setObjectName(u"LogWindow")
        LogWindow.resize(661, 734)
        self.centralwidget = QWidget(LogWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.close = QPushButton(self.centralwidget)
        self.close.setObjectName(u"close")

        self.gridLayout.addWidget(self.close, 1, 3, 1, 1)

        self.clear = QPushButton(self.centralwidget)
        self.clear.setObjectName(u"clear")

        self.gridLayout.addWidget(self.clear, 1, 1, 1, 1)

        self.log_list = QTableWidget(self.centralwidget)
        if (self.log_list.columnCount() < 3):
            self.log_list.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.log_list.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.log_list.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.log_list.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.log_list.setObjectName(u"log_list")
        self.log_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.log_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.log_list.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.log_list, 0, 0, 1, 4)

        self.horizontalSpacer = QSpacerItem(442, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        LogWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LogWindow)

        QMetaObject.connectSlotsByName(LogWindow)
    # setupUi

    def retranslateUi(self, LogWindow):
        LogWindow.setWindowTitle(QCoreApplication.translate("LogWindow", u"Log Window", None))
        self.close.setText(QCoreApplication.translate("LogWindow", u"Close", None))
        self.clear.setText(QCoreApplication.translate("LogWindow", u"Clear", None))
        ___qtablewidgetitem = self.log_list.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("LogWindow", u"Time", None));
        ___qtablewidgetitem1 = self.log_list.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("LogWindow", u"Severity", None));
        ___qtablewidgetitem2 = self.log_list.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("LogWindow", u"Message", None));
    # retranslateUi

