#!/usr/bin/env XRP
# -*- coding: utf-8 -*-
"""
Purpose - PyQt5 app to implament proof of concept button for creating a token in the XRP Ledger

qt_issue_v1.py
Zackary E. Scalyer
October 11, 2021  
Developer, Prepared for Flight, LLC
  
input
-------
    currently None

output
--------
    pyqt5 app running python code 
      

Notes
-------
    - This is supper simple/unrealistic implamentation for now. 
"""
# Form implementation generated from reading ui file 'test1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from xrp_poc import xrp_poc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 200, 80, 23))
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoRepeatDelay(299)
        self.pushButton.setAutoRepeatInterval(99)
        self.pushButton.setObjectName("pushButton")
        self.textout = QtWidgets.QPlainTextEdit(self.centralwidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Issue a Token"))
        self.pushButton.clicked.connect(self.clickMethod)
        
    def clickMethod(self):
        issue_print = xrp_poc()
        self.textout.insertPlainText(issue_print)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
