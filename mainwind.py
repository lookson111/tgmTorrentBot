# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwind.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 348)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(230, 310, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 291))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.pathLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.gridLayout.addWidget(self.pathLineEdit, 4, 0, 1, 1)
        self.logTextBrowser = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        self.logTextBrowser.setObjectName("logTextBrowser")
        self.gridLayout.addWidget(self.logTextBrowser, 5, 0, 1, 1)
        self.trayCeckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.trayCeckBox.setObjectName("trayCeckBox")
        self.gridLayout.addWidget(self.trayCeckBox, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.autorunBotcheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.autorunBotcheckBox.setObjectName("autorunBotcheckBox")
        self.gridLayout.addWidget(self.autorunBotcheckBox, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.startBot = QtWidgets.QPushButton(Dialog)
        self.startBot.setGeometry(QtCore.QRect(10, 310, 75, 23))
        self.startBot.setObjectName("startBot")
        self.stopBot = QtWidgets.QPushButton(Dialog)
        self.stopBot.setGeometry(QtCore.QRect(90, 310, 75, 23))
        self.stopBot.setObjectName("stopBot")

        self.retranslateUi(Dialog)
        #self.buttonBox.accepted.connect(Dialog.accept)
        #self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Бот"))
        self.trayCeckBox.setText(_translate("Dialog", "Минимизация в трей"))
        self.label.setText(_translate("Dialog", "Программа телеграм бот"))
        self.autorunBotcheckBox.setText(_translate("Dialog", "Автозапуск бота при старте программы"))
        self.label_2.setText(_translate("Dialog", "Пусть сохранения файлов:"))
        self.startBot.setText(_translate("Dialog", "Start"))
        self.stopBot.setText(_translate("Dialog", "Stop"))