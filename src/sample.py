# !/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import os
import sys
from pathlib import Path

import pandas as pd
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

from UI.interface_uav import *


class App(Ui_MainWindow,  QtWidgets.QWidget):
    def __init__(self, MainWindow, model=None) -> None:
        super().__init__()
        self.setupUi(MainWindow)


def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App(MainWindow=MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
