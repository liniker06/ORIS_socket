# Form implementation generated from reading ui file 'gui1.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 538)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(610, 559))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.output = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.gridLayout.addWidget(self.output, 0, 0, 1, 1)
        self.input = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.input.setObjectName("input")
        self.gridLayout.addWidget(self.input, 1, 0, 1, 1)
        self.send_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.send_button.setObjectName("send_button")
        self.gridLayout.addWidget(self.send_button, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.create_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.create_button.setObjectName("create_button")
        self.horizontalLayout.addWidget(self.create_button)
        self.join_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.join_button.setObjectName("join_button")
        self.horizontalLayout.addWidget(self.join_button)
        self.ban_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ban_button.setObjectName("ban_button")
        self.horizontalLayout.addWidget(self.ban_button)
        self.exit_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.exit_button.setObjectName("exit_button")
        self.horizontalLayout.addWidget(self.exit_button)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.send_button.setText(_translate("MainWindow", "Send"))
        self.create_button.setText(_translate("MainWindow", "Create"))
        self.join_button.setText(_translate("MainWindow", "Join"))
        self.ban_button.setText(_translate("MainWindow", "Ban"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))
