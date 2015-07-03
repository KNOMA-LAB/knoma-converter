#!/usr/bin/env python3
# encoding: utf-8
# __author__ = 'macan'

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import os
from papaya_converter_ui import Ui_MainWindow
import subprocess
import re

def selectInThumbFile():
    fileDialog = QtWidgets.QFileDialog()

    dirname = fileDialog.getOpenFileNames(caption='Selectione a imagem para Thumbnail',
                                          filter='Imagens (*.jpg *.png *.gif *.tif)'
                                          )

    if dirname:
        ui.lineEdit_3.setText(';'.join(dirname[0]))


def selectInFile():
    fileDialog = QtWidgets.QFileDialog()

    dirname = fileDialog.getOpenFileNames(caption='Selectione as imagens a converter',
                                          filter='Imagens (*.jpg *.png *.gif *.tif)'
                                          )

    if dirname:
        ui.lineEdit.setText(';'.join(dirname[0]))

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
        quality = ui.spinBox.value()
    elif ui.radioButton_4.isChecked():
        extension = 'jp2'
        quality = 100
    #TODO: CHECK EXISTENCE
    inpath = ui.lineEdit.text()
    outpath = ui.lineEdit_2.text()

    ui.progressBar.setRange(0,100)
    ui.plainTextEdit.clear()
    ui.plainTextEdit.appendPlainText("Iniciando conversão em {}".format(datetime.now()))
    files = inpath.split(';')
    # Let's pick only the images from the directory

    count = 1
    for f in files:

        namecomponents=os.path.basename(f).split('.')
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
            if quality == 100:
                qualitystr = ''
            else:
                qualitystr = "-quality {}".format(quality)

            command = 'convert "{}" {} "{}"'.format(
                os.path.join(inpath, f),
                qualitystr,
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

def makethumb():

    #TODO: CHECK EXISTENCE
    path = ui.lineEdit_3.text()
    ui.plainTextEdit_2.clear()
    ui.plainTextEdit_2.appendPlainText("Criando Thumbnail em {}".format(datetime.now()))

    # Let's pick only the images from the directory

    namecomponents=path.split('.')
    namecomponents[-1] = 'jpg'
    namecomponents[-2] = namecomponents[-2] + '-thumb'
    outf = '.'.join(namecomponents)

    ui.plainTextEdit_2.appendPlainText("Fazendo thumbnail de {} em {}".format(path, outf))

    command = 'convert "{}" -thumbnail 160x160^ -gravity center -extent 160x160 "{}"'.format( path, outf )
    #TODO: change call to not use shell
    output = subprocess.check_output(command, shell=True)
    #subprocess.call(["convert",os.path.join(inpath,f),'-define','tiff:tile-geometry=256x256',
    #                 '-compress', 'jpeg',"'ptif:%s'"% os.path.join(outpath,outf) ])
    ui.plainTextEdit_2.appendPlainText("Conversão concluída em {}".format(datetime.now()))


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

ui = Ui_MainWindow()
ui.setupUi(window)

# ui.lineEdit.setText(os.path.join(os.path.join(os.path.split(os.path.dirname(__file__))),"input"))
#ui.lineEdit_2.setText(os.path.join(os.path.join(os.path.split(os.path.dirname(__file__))),"output"))

ui.pushButton.clicked.connect(selectInFile)
ui.pushButton_2.clicked.connect(selectOutFile)
ui.pushButton_3.clicked.connect(selectInThumbFile)

ui.pushButton_go.clicked.connect(converte)
ui.pushButton_4.clicked.connect(makethumb)

ui.progressBar.setRange(0,100)
ui.progressBar.setValue(0)

ui.actionClose.triggered.connect(QtCore.QCoreApplication.instance().quit)

window.show()
sys.exit(app.exec_())
