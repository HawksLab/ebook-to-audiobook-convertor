# Form implementation generated from reading ui file '.\ui\progress_screen.ui'

from PyQt6 import QtCore, QtGui, QtWidgets
from app.ui import splash_screen_qrc


class Ui_progressWindow(object):
    def setupUi(self, progressWindow):
        progressWindow.setObjectName("progressWindow")
        progressWindow.resize(540, 120)
        progressWindow.setMinimumSize(QtCore.QSize(540, 120))
        progressWindow.setMaximumSize(QtCore.QSize(540, 120))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/logo.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        progressWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(parent=progressWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        progressWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(progressWindow)
        QtCore.QMetaObject.connectSlotsByName(progressWindow)

    def retranslateUi(self, progressWindow):
        _translate = QtCore.QCoreApplication.translate
        progressWindow.setWindowTitle(_translate("progressWindow", "Converting..."))
        self.label.setText(_translate("progressWindow", "Converting your e-book into audio-book... It may take several minutes depending on your system."))
