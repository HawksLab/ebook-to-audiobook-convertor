# Form implementation generated from reading ui file 'ui\splash_screen.ui'

from PyQt6 import QtCore, QtGui, QtWidgets
from app.ui import splash_screen_qrc


class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName("SplashScreen")
        SplashScreen.resize(620, 360)
        SplashScreen.setMaximumSize(QtCore.QSize(620, 600))
        SplashScreen.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/logo.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        SplashScreen.setWindowIcon(icon)
        SplashScreen.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(parent=SplashScreen)
        self.centralwidget.setMaximumSize(QtCore.QSize(620, 600))
        self.centralwidget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(620, 360))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/background/Hawks Lab.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.loadingStatus = QtWidgets.QLabel(parent=self.centralwidget)
        self.loadingStatus.setText("Loading...")
        self.loadingStatus.setStyleSheet("color: white;")
        self.loadingStatus.setContentsMargins(10, 0, 0, 10)
        self.verticalLayout.addWidget(self.loadingStatus)
        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)
        QtCore.QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen):
        _translate = QtCore.QCoreApplication.translate
        SplashScreen.setWindowTitle(_translate("SplashScreen", "abook reader"))
