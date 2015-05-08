#!/usr/bin/env python3
# encoding: utf-8
# __author__ = 'macan'

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import os
from knoma_converter_ui import Ui_MainWindow


def selectInFile():
    dirname = QtWidgets.QFileDialog.getExistingDirectory()
    if dirname:
        ui.lineEdit.setText(dirname)

def selectOutFile():
    dirname = QtWidgets.QFileDialog.getExistingDirectory()
    if dirname:
        ui.lineEdit_2.setText(dirname)

def converte():
    ui.progressBar.setRange(0,100)
    ui.label_message.setText("Convertendo")
    files = os.listdir(ui.lineEdit.text())
    count = 1
    for f in files:
        print(f,count/len(files))
        ui.progressBar.setValue(int(count*100/len(files)))
        ui.label_message.setText(f)
        count += 1
    ui.label_message.setText("Concluído")

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

ui = Ui_MainWindow()
ui.setupUi(window)

ui.label_message.setText("Inativo")
ui.lineEdit.setText(os.path.join(os.path.dirname(__file__),"input"))
ui.lineEdit_2.setText(os.path.join(os.path.dirname(__file__),"output"))

ui.pushButton.clicked.connect(selectInFile)
ui.pushButton_2.clicked.connect(selectOutFile)
ui.pushButton_go.clicked.connect(converte)

ui.progressBar.setRange(0,100)
ui.progressBar.setValue(0)

window.show()
sys.exit(app.exec_())