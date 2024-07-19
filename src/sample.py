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
    def __init__(self, MainWindow, model) -> None:
        super().__init__()
        self.setupUI(MainWindow)
        if self.RescueMap.mouseDoubleClickEvent == Qt.LeftButton:
            print('Right mouse double click')

    # def keyPressEvent(self, key) -> None:
    #     print(key)

    # @QtCore.pyqtSlot(float, float)
    # def onMapMoved(self, latitude, longitude):
    #     print("Moved to ", latitude, longitude)

    # def onMapRClick(self, latitude, longitude):
    #     print("RClick on ", latitude, longitude)

    # def onMapLClick(self, latitude, longitude):
    #     print("LClick on ", latitude, longitude)

    # def onMapDClick(self, latitude, longitude):
    #     print("DClick on ", latitude, longitude)
    # def


def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App(MainWindow=MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
