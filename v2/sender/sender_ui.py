# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sender.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 360)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_1 = QtWidgets.QWidget(self.centralwidget)
        self.widget_1.setGeometry(QtCore.QRect(0, 0, 480, 360))
        self.widget_1.setObjectName("widget_1")
        self.infoLabel_1 = QtWidgets.QLabel(self.widget_1)
        self.infoLabel_1.setGeometry(QtCore.QRect(110, 10, 241, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.infoLabel_1.setFont(font)
        self.infoLabel_1.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel_1.setObjectName("infoLabel_1")
        self.inputText = QtWidgets.QTextEdit(self.widget_1)
        self.inputText.setGeometry(QtCore.QRect(70, 80, 321, 71))
        self.inputText.setObjectName("inputText")
        self.sendButton = QtWidgets.QPushButton(self.widget_1)
        self.sendButton.setGeometry(QtCore.QRect(120, 170, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sendButton.setFont(font)
        self.sendButton.setDefault(False)
        self.sendButton.setObjectName("sendButton")
        self.exitButton = QtWidgets.QPushButton(self.widget_1)
        self.exitButton.setGeometry(QtCore.QRect(120, 270, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.exitButton.setFont(font)
        self.exitButton.setDefault(False)
        self.exitButton.setObjectName("exitButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.infoLabel_1.setText(_translate("MainWindow", "请输入想要传输的数据"))
        self.sendButton.setText(_translate("MainWindow", "开始传输数据"))
        self.exitButton.setText(_translate("MainWindow", "退出程序"))