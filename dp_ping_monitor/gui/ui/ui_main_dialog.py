# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(677, 465)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.server = QComboBox(Dialog)
        self.server.setObjectName(u"server")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.server.sizePolicy().hasHeightForWidth())
        self.server.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.server)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.start_time = QLabel(Dialog)
        self.start_time.setObjectName(u"start_time")

        self.gridLayout.addWidget(self.start_time, 0, 1, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.duration = QLabel(Dialog)
        self.duration.setObjectName(u"duration")

        self.gridLayout.addWidget(self.duration, 1, 1, 1, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.avg_ping = QLabel(Dialog)
        self.avg_ping.setObjectName(u"avg_ping")

        self.gridLayout.addWidget(self.avg_ping, 2, 1, 1, 1)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.min_ping = QLabel(Dialog)
        self.min_ping.setObjectName(u"min_ping")

        self.gridLayout.addWidget(self.min_ping, 3, 1, 1, 1)

        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.max_ping = QLabel(Dialog)
        self.max_ping.setObjectName(u"max_ping")

        self.gridLayout.addWidget(self.max_ping, 4, 1, 1, 1)


        self.horizontalLayout_4.addLayout(self.gridLayout)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.start_stop = QPushButton(Dialog)
        self.start_stop.setObjectName(u"start_stop")

        self.horizontalLayout_2.addWidget(self.start_stop)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 12, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.program_name_n_version = QLabel(Dialog)
        self.program_name_n_version.setObjectName(u"program_name_n_version")
        self.program_name_n_version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.program_name_n_version)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.copyright = QLabel(Dialog)
        self.copyright.setObjectName(u"copyright")
        self.copyright.setOpenExternalLinks(True)

        self.horizontalLayout_3.addWidget(self.copyright)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Server:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Started at:", None))
        self.start_time.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Duration:", None))
        self.duration.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Average:", None))
        self.avg_ping.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Peak min:", None))
        self.min_ping.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Peak max:", None))
        self.max_ping.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.start_stop.setText(QCoreApplication.translate("Dialog", u"Start", None))
        self.program_name_n_version.setText(QCoreApplication.translate("Dialog", u"<program name & version>", None))
        self.copyright.setText(QCoreApplication.translate("Dialog", u"<copyright>", None))
    # retranslateUi
