#!/usr/bin/env python3
# encoding: utf-8
# __author__ = 'macan'

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import os
from knoma_converter_ui import Ui_MainWindow
import subprocess
import re

def selectInFile():
    dirname = QtWidgets.QFileDialog.getExistingDirectory()
    if dirname:
        ui.lineEdit.setText(dirname)

def selectOutFile():
    dirname = QtWidgets.QFileDialog.getExistingDirectory()
    if dirname:
        ui.lineEdit_2.setText(dirname)

def converte():
    if ui.radioButton_2.isChecked():
        extension = 'tif'
    elif ui.radioButton_3.isChecked():
        extension = 'jpg'
    elif ui.radioButton.isChecked():
        extension = 'jp2'

    #TODO: CHECK EXISTENCE
    inpath = ui.lineEdit.text()
    outpath = ui.lineEdit_2.text()

    ui.progressBar.setRange(0,100)
    ui.plainTextEdit.clear()
    ui.plainTextEdit.appendPlainText("Iniciando conversão em {}".format(datetime.now()))
    files = os.listdir(inpath)
    # Let's pick only the images from the directory

    files = list(filter(lambda x: x[-4:].lower() in ['ptif', '.tif', '.jpg', '.png', '.bmp', '.gif'], files))

    count = 1
    for f in files:
        namecomponents=f.split('.')
        namecomponents[-1] = extension
        outf = '.'.join(namecomponents)

        ui.plainTextEdit.appendPlainText("Convertendo {} para {}".format(
            os.path.join(inpath,f),
            os.path.join(outpath,outf)
        ))
        if extension == 'tif':
            # convert infile -define tiff:tile-geometry=256x256 -compress jpeg 'ptif:o.tif'
            command = 'convert "{}" -define tiff:tile-geometry=256x256 -compress jpeg "ptif:{}"'.format(
                os.path.join(inpath, f), os.path.join(outpath, outf)
            )

        elif extension == 'jp2':
            # convert infile -define tiff:tile-geometry=256x256 -compress jpeg 'ptif:o.tif'
            command = 'convert "{}" "{}"'.format(
                os.path.join(inpath, f),
                os.path.join(outpath, outf)
            )
        elif extension == 'jpg':
            command = 'convert "{}" "{}"'.format(
                os.path.join(inpath, f),
                os.path.join(outpath, outf)
            )
        #TODO: change call to not use shell
        output = subprocess.check_output(command, shell=True)
        #subprocess.call(["convert",os.path.join(inpath,f),'-define','tiff:tile-geometry=256x256',
        #                 '-compress', 'jpeg',"'ptif:%s'"% os.path.join(outpath,outf) ])
        ui.progressBar.setValue(int(count*100/len(files)))

        count += 1
    ui.plainTextEdit.appendPlainText("Conversão concluída em {}".format(datetime.now()))
    #ui.label_message.setText("Concluído")

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

ui = Ui_MainWindow()
ui.setupUi(window)

# ui.lineEdit.setText(os.path.join(os.path.join(os.path.split(os.path.dirname(__file__))),"input"))
#ui.lineEdit_2.setText(os.path.join(os.path.join(os.path.split(os.path.dirname(__file__))),"output"))

ui.pushButton.clicked.connect(selectInFile)
ui.pushButton_2.clicked.connect(selectOutFile)
ui.pushButton_go.clicked.connect(converte)

ui.progressBar.setRange(0,100)
ui.progressBar.setValue(0)

window.show()
sys.exit(app.exec_())
