#!/usr/bin/env python3
# encoding: utf-8
# __author__ = 'macan'

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from knoma_converter_ui import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

window.show()
sys.exit(app.exec_())