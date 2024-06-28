# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'interfaceFFmUWd.ui'
##
# Created by: Qt User Interface Compiler version 5.15.3
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# import icons_rc

icons_dir = "../icons/"


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1653, 830)
        MainWindow.setMinimumSize(QSize(97, 35))
        MainWindow.setMaximumSize(QSize(1692, 16777215))
        MainWindow.setStyleSheet(u"*{\n"
                                 "	border: none;\n"
                                 "}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: rgb(24, 24, 36);")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.slide_menu_container = QFrame(self.centralwidget)
        self.slide_menu_container.setObjectName(u"slide_menu_container")
        self.slide_menu_container.setMinimumSize(QSize(0, 0))
        self.slide_menu_container.setMaximumSize(QSize(0, 16777215))
        self.slide_menu_container.setStyleSheet(
            u"background-color: rgb(9, 5, 13);")
        self.slide_menu_container.setFrameShape(QFrame.StyledPanel)
        self.slide_menu_container.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.slide_menu_container)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.slide_menu = QFrame(self.slide_menu_container)
        self.slide_menu.setObjectName(u"slide_menu")
        self.slide_menu.setMinimumSize(QSize(196, 0))
        self.slide_menu.setFrameShape(QFrame.StyledPanel)
        self.slide_menu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.slide_menu)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.slide_menu)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_2 = QLabel(self.frame_7)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
                                   "color: rgb(255, 0, 0);")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_2)

        self.verticalLayout_5.addWidget(self.frame_7, 0, Qt.AlignTop)

        self.frame_8 = QFrame(self.slide_menu)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.btn_home = QPushButton(self.frame_8)
        self.btn_home.setObjectName(u"btn_home")
        self.btn_home.setGeometry(QRect(10, 70, 178, 40))
        self.btn_home.setMinimumSize(QSize(0, 40))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        font1.setWeight(75)
        self.btn_home.setFont(font1)
        self.btn_home.setStyleSheet(u"background:rgb(118, 118, 118);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "\n"
                                    "")
        icon = QIcon()
        icon.addFile(f"{icons_dir}/home.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_home.setIcon(icon)
        self.btn_home.setIconSize(QSize(24, 24))
        self.btn_connect = QPushButton(self.frame_8)
        self.btn_connect.setObjectName(u"btn_connect")
        self.btn_connect.setGeometry(QRect(10, 150, 178, 40))
        self.btn_connect.setMinimumSize(QSize(0, 40))
        self.btn_connect.setFont(font1)
        self.btn_connect.setStyleSheet(u"background:rgb(118, 118, 118);\n"
                                       "color: rgb(0, 0, 0);\n"
                                       "")
        icon1 = QIcon()
        icon1.addFile(f"{icons_dir}/link.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_connect.setIcon(icon1)
        self.btn_connect.setIconSize(QSize(24, 24))
        self.btn_map = QPushButton(self.frame_8)
        self.btn_map.setObjectName(u"btn_map")
        self.btn_map.setGeometry(QRect(10, 230, 178, 40))
        self.btn_map.setMinimumSize(QSize(0, 40))
        self.btn_map.setFont(font1)
        self.btn_map.setStyleSheet(u"background:rgb(118, 118, 118);\n"
                                   "color: rgb(0, 0, 0);\n"
                                   "")
        icon2 = QIcon()
        icon2.addFile(f"{icons_dir}/map.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_map.setIcon(icon2)
        self.btn_map.setIconSize(QSize(24, 24))
        self.btn_parameter = QPushButton(self.frame_8)
        self.btn_parameter.setObjectName(u"btn_parameter")
        self.btn_parameter.setGeometry(QRect(10, 390, 178, 40))
        self.btn_parameter.setMinimumSize(QSize(0, 40))
        self.btn_parameter.setFont(font1)
        self.btn_parameter.setStyleSheet(u"background:rgb(118, 118, 118);\n"
                                         "color: rgb(0, 0, 0);\n"
                                         "")
        icon3 = QIcon()
        icon3.addFile(f"{icons_dir}/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_parameter.setIcon(icon3)
        self.btn_parameter.setIconSize(QSize(24, 24))
        self.btn_algorithm = QPushButton(self.frame_8)
        self.btn_algorithm.setObjectName(u"btn_algorithm")
        self.btn_algorithm.setGeometry(QRect(10, 310, 178, 40))
        self.btn_algorithm.setMinimumSize(QSize(0, 40))
        self.btn_algorithm.setFont(font1)
        self.btn_algorithm.setStyleSheet(u"background:rgb(118, 118, 118);\n"
                                         "color: rgb(0, 0, 0);\n"
                                         "")
        icon4 = QIcon()
        icon4.addFile(f"{icons_dir}/tool.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_algorithm.setIcon(icon4)
        self.btn_algorithm.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.slide_menu)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.exit_button = QPushButton(self.frame_9)
        self.exit_button.setObjectName(u"exit_button")
        icon5 = QIcon()
        icon5.addFile(f"{icons_dir}/external-link.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exit_button.setIcon(icon5)
        self.exit_button.setIconSize(QSize(16, 16))

        self.horizontalLayout_9.addWidget(
            self.exit_button, 0, Qt.AlignLeft | Qt.AlignBottom)

        self.verticalLayout_5.addWidget(self.frame_9, 0, Qt.AlignBottom)

        self.verticalLayout_2.addWidget(self.slide_menu)

        self.horizontalLayout.addWidget(self.slide_menu_container)

        self.main_body = QFrame(self.centralwidget)
        self.main_body.setObjectName(u"main_body")
        self.main_body.setFrameShape(QFrame.StyledPanel)
        self.main_body.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.main_body)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.main_body)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setStyleSheet(u"background-color: rgb(9, 5, 13);")
        self.header_frame.setFrameShape(QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.header_frame)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.frame_6 = QFrame(self.header_frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.open_close_side_bar_btn = QPushButton(self.frame_6)
        self.open_close_side_bar_btn.setObjectName(u"open_close_side_bar_btn")
        self.open_close_side_bar_btn.setStyleSheet(u"color: rgb(255, 0, 0);")
        icon6 = QIcon()
        icon6.addFile(f"{icons_dir}/align-justify.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.open_close_side_bar_btn.setIcon(icon6)
        self.open_close_side_bar_btn.setIconSize(QSize(32, 32))

        self.horizontalLayout_7.addWidget(self.open_close_side_bar_btn)

        self.horizontalLayout_2.addWidget(
            self.frame_6, 0, Qt.AlignLeft | Qt.AlignTop)

        self.frame_3 = QFrame(self.header_frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_2.addWidget(
            self.frame_3, 0, Qt.AlignLeft | Qt.AlignTop)

        self.label = QLabel(self.header_frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 40))
        self.label.setMaximumSize(QSize(16777215, 40))
        font2 = QFont()
        font2.setFamily(u"Times New Roman")
        font2.setPointSize(18)
        font2.setBold(True)
        font2.setItalic(True)
        font2.setWeight(75)
        self.label.setFont(font2)
        self.label.setStyleSheet(u"color: rgb(255, 0, 0);\n"
                                 "background-color: rgb(0, 0, 0);")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.frame_2 = QFrame(self.header_frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_2.addWidget(
            self.frame_2, 0, Qt.AlignHCenter | Qt.AlignTop)

        self.frame = QFrame(self.header_frame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.minimize_window_button = QPushButton(self.frame)
        self.minimize_window_button.setObjectName(u"minimize_window_button")
        icon7 = QIcon()
        icon7.addFile(f"{icons_dir}/arrow-down-left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_window_button.setIcon(icon7)

        self.horizontalLayout_4.addWidget(self.minimize_window_button)

        self.restore_window_button = QPushButton(self.frame)
        self.restore_window_button.setObjectName(u"restore_window_button")
        icon8 = QIcon()
        icon8.addFile(f"{icons_dir}/maximize-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.restore_window_button.setIcon(icon8)

        self.horizontalLayout_4.addWidget(self.restore_window_button)

        self.close_window_button = QPushButton(self.frame)
        self.close_window_button.setObjectName(u"close_window_button")
        icon9 = QIcon()
        icon9.addFile(f"{icons_dir}/x.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.close_window_button.setIcon(icon9)

        self.horizontalLayout_4.addWidget(self.close_window_button)

        self.horizontalLayout_2.addWidget(
            self.frame, 0, Qt.AlignRight | Qt.AlignTop)

        self.verticalLayout.addWidget(self.header_frame, 0, Qt.AlignTop)

        self.main_body_contents = QFrame(self.main_body)
        self.main_body_contents.setObjectName(u"main_body_contents")
        sizePolicy.setHeightForWidth(
            self.main_body_contents.sizePolicy().hasHeightForWidth())
        self.main_body_contents.setSizePolicy(sizePolicy)
        self.main_body_contents.setFrameShape(QFrame.StyledPanel)
        self.main_body_contents.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.main_body_contents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.stackedWidget = QStackedWidget(self.main_body_contents)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.page_algorithm = QWidget()
        self.page_algorithm.setObjectName(u"page_algorithm")
        self.horizontalLayout_65 = QHBoxLayout(self.page_algorithm)
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.frame_114 = QFrame(self.page_algorithm)
        self.frame_114.setObjectName(u"frame_114")
        self.frame_114.setFrameShape(QFrame.StyledPanel)
        self.frame_114.setFrameShadow(QFrame.Raised)
        self.verticalLayout_42 = QVBoxLayout(self.frame_114)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.frame_116 = QFrame(self.frame_114)
        self.frame_116.setObjectName(u"frame_116")
        self.frame_116.setMinimumSize(QSize(0, 30))
        self.frame_116.setMaximumSize(QSize(16777215, 40))
        self.frame_116.setStyleSheet(u"background-color: rgb(85, 255, 0);")
        self.frame_116.setFrameShape(QFrame.StyledPanel)
        self.frame_116.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_66 = QHBoxLayout(self.frame_116)
        self.horizontalLayout_66.setSpacing(0)
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.horizontalLayout_66.setContentsMargins(0, 0, 0, 0)
        self.label_76 = QLabel(self.frame_116)
        self.label_76.setObjectName(u"label_76")
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(True)
        font3.setItalic(True)
        font3.setWeight(75)
        self.label_76.setFont(font3)
        self.label_76.setStyleSheet(u"color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(0, 0, 0);")
        self.label_76.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_66.addWidget(self.label_76)

        self.label_82 = QLabel(self.frame_116)
        self.label_82.setObjectName(u"label_82")
        self.label_82.setFont(font3)
        self.label_82.setStyleSheet(u"color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(0, 0, 0);")
        self.label_82.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_66.addWidget(self.label_82)

        self.frame_120 = QFrame(self.frame_116)
        self.frame_120.setObjectName(u"frame_120")
        self.frame_120.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_120.setFrameShape(QFrame.StyledPanel)
        self.frame_120.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_66.addWidget(self.frame_120)

        self.verticalLayout_42.addWidget(self.frame_116)

        self.frame_117 = QFrame(self.frame_114)
        self.frame_117.setObjectName(u"frame_117")
        self.frame_117.setMinimumSize(QSize(0, 50))
        self.frame_117.setMaximumSize(QSize(16777215, 50))
        self.frame_117.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_117.setFrameShape(QFrame.StyledPanel)
        self.frame_117.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_67 = QHBoxLayout(self.frame_117)
        self.horizontalLayout_67.setSpacing(0)
        self.horizontalLayout_67.setObjectName(u"horizontalLayout_67")
        self.horizontalLayout_67.setContentsMargins(0, 0, 0, 0)
        self.frame_122 = QFrame(self.frame_117)
        self.frame_122.setObjectName(u"frame_122")
        self.frame_122.setMaximumSize(QSize(30, 16777215))
        self.frame_122.setFrameShape(QFrame.StyledPanel)
        self.frame_122.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_67.addWidget(self.frame_122)

        self.latitude_algorithm = QPlainTextEdit(self.frame_117)
        self.latitude_algorithm.setObjectName(u"latitude_algorithm")
        self.latitude_algorithm.setMinimumSize(QSize(200, 30))
        self.latitude_algorithm.setMaximumSize(QSize(200, 30))
        self.latitude_algorithm.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "border-width: 2px;\n"
                                              "border-radius: 10px;")

        self.horizontalLayout_67.addWidget(self.latitude_algorithm)

        self.frame_123 = QFrame(self.frame_117)
        self.frame_123.setObjectName(u"frame_123")
        self.frame_123.setMinimumSize(QSize(55, 0))
        self.frame_123.setMaximumSize(QSize(55, 16777215))
        self.frame_123.setFrameShape(QFrame.StyledPanel)
        self.frame_123.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_67.addWidget(self.frame_123)

        self.longtitude_algorithm = QPlainTextEdit(self.frame_117)
        self.longtitude_algorithm.setObjectName(u"longtitude_algorithm")
        self.longtitude_algorithm.setMinimumSize(QSize(200, 30))
        self.longtitude_algorithm.setMaximumSize(QSize(200, 30))
        self.longtitude_algorithm.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                                "color: rgb(0, 0, 0);\n"
                                                "border-width: 2px;\n"
                                                "border-radius: 10px;")

        self.horizontalLayout_67.addWidget(self.longtitude_algorithm)

        self.frame_124 = QFrame(self.frame_117)
        self.frame_124.setObjectName(u"frame_124")
        self.frame_124.setMinimumSize(QSize(55, 0))
        self.frame_124.setMaximumSize(QSize(55, 16777215))
        self.frame_124.setFrameShape(QFrame.StyledPanel)
        self.frame_124.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_67.addWidget(self.frame_124)

        self.pushButton = QPushButton(self.frame_117)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(200, 30))
        self.pushButton.setMaximumSize(QSize(200, 30))
        self.pushButton.setFont(font1)
        self.pushButton.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "border-width: 2px;\n"
                                      "border-radius: 10px;")

        self.horizontalLayout_67.addWidget(self.pushButton)

        self.frame_125 = QFrame(self.frame_117)
        self.frame_125.setObjectName(u"frame_125")
        self.frame_125.setMinimumSize(QSize(35, 0))
        self.frame_125.setMaximumSize(QSize(50, 16777215))
        self.frame_125.setFrameShape(QFrame.StyledPanel)
        self.frame_125.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_67.addWidget(self.frame_125)

        self.verticalLayout_42.addWidget(self.frame_117)

        self.frame_118 = QFrame(self.frame_114)
        self.frame_118.setObjectName(u"frame_118")
        self.frame_118.setMaximumSize(QSize(16777215, 300))
        self.frame_118.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.frame_118.setFrameShape(QFrame.StyledPanel)
        self.frame_118.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_68 = QHBoxLayout(self.frame_118)
        self.horizontalLayout_68.setSpacing(0)
        self.horizontalLayout_68.setObjectName(u"horizontalLayout_68")
        self.horizontalLayout_68.setContentsMargins(0, 0, 0, 0)
        self.frame_128 = QFrame(self.frame_118)
        self.frame_128.setObjectName(u"frame_128")
        self.frame_128.setMaximumSize(QSize(10, 16777215))
        self.frame_128.setFrameShape(QFrame.StyledPanel)
        self.frame_128.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_68.addWidget(self.frame_128)

        self.frame_126 = QFrame(self.frame_118)
        self.frame_126.setObjectName(u"frame_126")
        self.frame_126.setMaximumSize(QSize(455, 16777215))
        self.frame_126.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")
        self.frame_126.setFrameShape(QFrame.StyledPanel)
        self.frame_126.setFrameShadow(QFrame.Raised)
        self.verticalLayout_43 = QVBoxLayout(self.frame_126)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.scr_algorithm = QPlainTextEdit(self.frame_126)
        self.scr_algorithm.setObjectName(u"scr_algorithm")
        self.scr_algorithm.setMaximumSize(QSize(455, 300))
        self.scr_algorithm.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
                                         "color: rgb(255, 255, 255);")

        self.verticalLayout_43.addWidget(self.scr_algorithm)

        self.horizontalLayout_68.addWidget(self.frame_126)

        self.frame_129 = QFrame(self.frame_118)
        self.frame_129.setObjectName(u"frame_129")
        self.frame_129.setMaximumSize(QSize(40, 16777215))
        self.frame_129.setFrameShape(QFrame.StyledPanel)
        self.frame_129.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_68.addWidget(self.frame_129)

        self.frame_127 = QFrame(self.frame_118)
        self.frame_127.setObjectName(u"frame_127")
        self.frame_127.setMaximumSize(QSize(200, 16777215))
        self.frame_127.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.frame_127.setFrameShape(QFrame.StyledPanel)
        self.frame_127.setFrameShadow(QFrame.Raised)
        self.verticalLayout_44 = QVBoxLayout(self.frame_127)
        self.verticalLayout_44.setSpacing(0)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.verticalLayout_44.setContentsMargins(0, 0, 0, 0)
        self.fly_1_uav = QPushButton(self.frame_127)
        self.fly_1_uav.setObjectName(u"fly_1_uav")
        self.fly_1_uav.setMinimumSize(QSize(200, 30))
        self.fly_1_uav.setMaximumSize(QSize(200, 30))
        self.fly_1_uav.setFont(font1)
        self.fly_1_uav.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.verticalLayout_44.addWidget(self.fly_1_uav)

        self.fly_2_uav = QPushButton(self.frame_127)
        self.fly_2_uav.setObjectName(u"fly_2_uav")
        self.fly_2_uav.setMinimumSize(QSize(200, 30))
        self.fly_2_uav.setMaximumSize(QSize(200, 30))
        self.fly_2_uav.setFont(font1)
        self.fly_2_uav.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.verticalLayout_44.addWidget(self.fly_2_uav)

        self.fly_3_UAV = QPushButton(self.frame_127)
        self.fly_3_UAV.setObjectName(u"fly_3_UAV")
        self.fly_3_UAV.setMinimumSize(QSize(200, 30))
        self.fly_3_UAV.setMaximumSize(QSize(200, 30))
        self.fly_3_UAV.setFont(font1)
        self.fly_3_UAV.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.verticalLayout_44.addWidget(self.fly_3_UAV)

        self.fly_4_UAV = QPushButton(self.frame_127)
        self.fly_4_UAV.setObjectName(u"fly_4_UAV")
        self.fly_4_UAV.setMinimumSize(QSize(200, 30))
        self.fly_4_UAV.setMaximumSize(QSize(200, 30))
        self.fly_4_UAV.setFont(font1)
        self.fly_4_UAV.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.verticalLayout_44.addWidget(self.fly_4_UAV)

        self.horizontalLayout_68.addWidget(self.frame_127)

        self.frame_130 = QFrame(self.frame_118)
        self.frame_130.setObjectName(u"frame_130")
        self.frame_130.setMaximumSize(QSize(20, 16777215))
        self.frame_130.setFrameShape(QFrame.StyledPanel)
        self.frame_130.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_68.addWidget(self.frame_130)

        self.verticalLayout_42.addWidget(self.frame_118)

        self.frame_119 = QFrame(self.frame_114)
        self.frame_119.setObjectName(u"frame_119")
        self.frame_119.setStyleSheet(u"background-color: rgb(118, 118, 118);")
        self.frame_119.setFrameShape(QFrame.StyledPanel)
        self.frame_119.setFrameShadow(QFrame.Raised)

        self.verticalLayout_42.addWidget(self.frame_119)

        self.horizontalLayout_65.addWidget(self.frame_114)

        self.frame_115 = QFrame(self.page_algorithm)
        self.frame_115.setObjectName(u"frame_115")
        self.frame_115.setMinimumSize(QSize(822, 0))
        self.frame_115.setMaximumSize(QSize(822, 16777215))
        self.frame_115.setFrameShape(QFrame.StyledPanel)
        self.frame_115.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_65.addWidget(self.frame_115)

        self.stackedWidget.addWidget(self.page_algorithm)
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.verticalLayout_6 = QVBoxLayout(self.page_home)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_29 = QFrame(self.page_home)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMinimumSize(QSize(0, 40))
        self.frame_29.setMaximumSize(QSize(16777215, 40))
        self.frame_29.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_29.setFrameShape(QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.frame_30 = QFrame(self.frame_29)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_30.setFrameShape(QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_30)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_24 = QLabel(self.frame_30)
        self.label_24.setObjectName(u"label_24")
        font4 = QFont()
        font4.setPointSize(18)
        font4.setBold(True)
        font4.setItalic(True)
        font4.setWeight(75)
        self.label_24.setFont(font4)
        self.label_24.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_24.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_15.addWidget(self.label_24)

        self.horizontalLayout_14.addWidget(self.frame_30)

        self.frame_31 = QFrame(self.frame_29)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_31.setFrameShape(QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_31)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_30 = QLabel(self.frame_31)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font4)
        self.label_30.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_30.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_16.addWidget(self.label_30)

        self.horizontalLayout_14.addWidget(self.frame_31)

        self.frame_32 = QFrame(self.frame_29)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_32.setFrameShape(QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_31 = QLabel(self.frame_32)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font4)
        self.label_31.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_31.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_17.addWidget(self.label_31)

        self.horizontalLayout_14.addWidget(self.frame_32)

        self.frame_33 = QFrame(self.frame_29)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_33.setFrameShape(QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_32 = QLabel(self.frame_33)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font4)
        self.label_32.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_32.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_18.addWidget(self.label_32)

        self.horizontalLayout_14.addWidget(self.frame_33)

        self.frame_34 = QFrame(self.frame_29)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_34.setFrameShape(QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_34)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_33 = QLabel(self.frame_34)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font4)
        self.label_33.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_33.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_19.addWidget(self.label_33)

        self.horizontalLayout_14.addWidget(self.frame_34)

        self.frame_35 = QFrame(self.frame_29)
        self.frame_35.setObjectName(u"frame_35")
        self.frame_35.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_35.setFrameShape(QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_35)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_34 = QLabel(self.frame_35)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font4)
        self.label_34.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_34.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_20.addWidget(self.label_34)

        self.horizontalLayout_14.addWidget(self.frame_35)

        self.verticalLayout_6.addWidget(self.frame_29)

        self.frame_13 = QFrame(self.page_home)
        self.frame_13.setObjectName(u"frame_13")
        sizePolicy.setHeightForWidth(
            self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy)
        self.frame_13.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.frame_17 = QFrame(self.frame_13)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_17)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_3 = QLabel(self.frame_17)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(240, 170))
        self.label_3.setMaximumSize(QSize(240, 180))
        font5 = QFont()
        font5.setPointSize(10)
        self.label_3.setFont(font5)
        self.label_3.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_3)

        self.horizontalLayout_12.addWidget(self.frame_17)

        self.frame_18 = QFrame(self.frame_13)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_18)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_7 = QLabel(self.frame_18)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(240, 170))
        self.label_7.setMaximumSize(QSize(240, 180))
        self.label_7.setFont(font5)
        self.label_7.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_7)

        self.horizontalLayout_12.addWidget(self.frame_18)

        self.frame_19 = QFrame(self.frame_13)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_19)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_8 = QLabel(self.frame_19)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(240, 170))
        self.label_8.setMaximumSize(QSize(240, 180))
        self.label_8.setFont(font5)
        self.label_8.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.label_8)

        self.horizontalLayout_12.addWidget(self.frame_19)

        self.frame_20 = QFrame(self.frame_13)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_20)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_9 = QLabel(self.frame_20)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(240, 170))
        self.label_9.setMaximumSize(QSize(240, 180))
        self.label_9.setFont(font5)
        self.label_9.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_9.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.label_9)

        self.horizontalLayout_12.addWidget(self.frame_20)

        self.frame_21 = QFrame(self.frame_13)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_21)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_10 = QLabel(self.frame_21)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(240, 170))
        self.label_10.setMaximumSize(QSize(240, 180))
        self.label_10.setFont(font5)
        self.label_10.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_10.setAlignment(Qt.AlignCenter)

        self.verticalLayout_13.addWidget(self.label_10)

        self.horizontalLayout_12.addWidget(self.frame_21)

        self.frame_22 = QFrame(self.frame_13)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_22)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_18 = QLabel(self.frame_22)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(240, 170))
        self.label_18.setMaximumSize(QSize(240, 180))
        self.label_18.setFont(font5)
        self.label_18.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_18.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.label_18)

        self.horizontalLayout_12.addWidget(self.frame_22)

        self.verticalLayout_6.addWidget(self.frame_13)

        self.frame_14 = QFrame(self.page_home)
        self.frame_14.setObjectName(u"frame_14")
        sizePolicy.setHeightForWidth(
            self.frame_14.sizePolicy().hasHeightForWidth())
        self.frame_14.setSizePolicy(sizePolicy)
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.frame_23 = QFrame(self.frame_14)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_35 = QLabel(self.frame_23)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setMinimumSize(QSize(240, 170))
        self.label_35.setMaximumSize(QSize(240, 180))
        self.label_35.setFont(font5)
        self.label_35.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_35.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_22.addWidget(self.label_35)

        self.horizontalLayout_13.addWidget(self.frame_23)

        self.frame_24 = QFrame(self.frame_14)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_36 = QLabel(self.frame_24)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(240, 170))
        self.label_36.setMaximumSize(QSize(240, 180))
        self.label_36.setFont(font5)
        self.label_36.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_36.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_23.addWidget(self.label_36)

        self.horizontalLayout_13.addWidget(self.frame_24)

        self.frame_25 = QFrame(self.frame_14)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_25.setFrameShape(QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_37 = QLabel(self.frame_25)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setMinimumSize(QSize(240, 170))
        self.label_37.setMaximumSize(QSize(240, 180))
        self.label_37.setFont(font5)
        self.label_37.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_37.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_24.addWidget(self.label_37)

        self.horizontalLayout_13.addWidget(self.frame_25)

        self.frame_26 = QFrame(self.frame_14)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_26.setFrameShape(QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.label_38 = QLabel(self.frame_26)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setMinimumSize(QSize(240, 170))
        self.label_38.setMaximumSize(QSize(240, 180))
        self.label_38.setFont(font5)
        self.label_38.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_38.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_25.addWidget(self.label_38)

        self.horizontalLayout_13.addWidget(self.frame_26)

        self.frame_27 = QFrame(self.frame_14)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_27.setFrameShape(QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_39 = QLabel(self.frame_27)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setMinimumSize(QSize(240, 170))
        self.label_39.setMaximumSize(QSize(240, 180))
        self.label_39.setFont(font5)
        self.label_39.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_39.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_26.addWidget(self.label_39)

        self.horizontalLayout_13.addWidget(self.frame_27)

        self.frame_28 = QFrame(self.frame_14)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_28.setFrameShape(QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_28)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_40 = QLabel(self.frame_28)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMinimumSize(QSize(240, 170))
        self.label_40.setMaximumSize(QSize(240, 180))
        self.label_40.setFont(font5)
        self.label_40.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_40.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_27.addWidget(self.label_40)

        self.horizontalLayout_13.addWidget(self.frame_28)

        self.verticalLayout_6.addWidget(self.frame_14)

        self.frame_15 = QFrame(self.page_home)
        self.frame_15.setObjectName(u"frame_15")
        sizePolicy.setHeightForWidth(
            self.frame_15.sizePolicy().hasHeightForWidth())
        self.frame_15.setSizePolicy(sizePolicy)
        self.frame_15.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.plainTextEdit = QPlainTextEdit(self.frame_15)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        self.horizontalLayout_21.addWidget(self.plainTextEdit)

        self.verticalLayout_6.addWidget(self.frame_15)

        self.frame_16 = QFrame(self.page_home)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 50))
        self.frame_16.setMaximumSize(QSize(16777215, 50))
        self.frame_16.setStyleSheet(u"background-color: rgb(255, 85, 127);")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.frame_12 = QFrame(self.frame_16)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_29.setSpacing(0)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(0, 0, 9, 0)
        self.pushButton_3 = QPushButton(self.frame_12)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(0, 30))
        self.pushButton_3.setMaximumSize(QSize(16777215, 30))
        font6 = QFont()
        font6.setPointSize(12)
        font6.setBold(True)
        font6.setWeight(75)
        self.pushButton_3.setFont(font6)
        self.pushButton_3.setStyleSheet(u"background:rgb(118, 118, 118);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-width: 2px;\n"
                                        "border-radius: 10px;\n"
                                        "")

        self.horizontalLayout_29.addWidget(self.pushButton_3)

        self.horizontalLayout_28.addWidget(self.frame_12)

        self.frame_36 = QFrame(self.frame_16)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_36.setFrameShape(QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.frame_36)
        self.horizontalLayout_30.setSpacing(0)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(0, 0, 9, 0)
        self.pushButton_4 = QPushButton(self.frame_36)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(0, 30))
        self.pushButton_4.setMaximumSize(QSize(16777215, 30))
        self.pushButton_4.setFont(font6)
        self.pushButton_4.setStyleSheet(u"background:rgb(118, 118, 118);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-width: 2px;\n"
                                        "border-radius: 10px;")

        self.horizontalLayout_30.addWidget(self.pushButton_4)

        self.horizontalLayout_28.addWidget(self.frame_36)

        self.frame_37 = QFrame(self.frame_16)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_37.setFrameShape(QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_31 = QHBoxLayout(self.frame_37)
        self.horizontalLayout_31.setSpacing(0)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(0, 0, 0, 0)
        self.pushButton_5 = QPushButton(self.frame_37)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(0, 30))
        self.pushButton_5.setMaximumSize(QSize(16777215, 30))
        self.pushButton_5.setFont(font6)
        self.pushButton_5.setStyleSheet(u"background:rgb(118, 118, 118);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-width: 2px;\n"
                                        "border-radius: 10px;")

        self.horizontalLayout_31.addWidget(self.pushButton_5)

        self.horizontalLayout_28.addWidget(self.frame_37)

        self.verticalLayout_6.addWidget(self.frame_16)

        self.stackedWidget.addWidget(self.page_home)
        self.page_parameter = QWidget()
        self.page_parameter.setObjectName(u"page_parameter")
        self.verticalLayout_23 = QVBoxLayout(self.page_parameter)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.frame_67 = QFrame(self.page_parameter)
        self.frame_67.setObjectName(u"frame_67")
        self.frame_67.setMinimumSize(QSize(0, 35))
        self.frame_67.setMaximumSize(QSize(16777215, 35))
        self.frame_67.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.frame_67.setFrameShape(QFrame.StyledPanel)
        self.frame_67.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_57 = QHBoxLayout(self.frame_67)
        self.horizontalLayout_57.setSpacing(0)
        self.horizontalLayout_57.setObjectName(u"horizontalLayout_57")
        self.horizontalLayout_57.setContentsMargins(0, 0, 0, 0)
        self.label_41 = QLabel(self.frame_67)
        self.label_41.setObjectName(u"label_41")
        font7 = QFont()
        font7.setPointSize(13)
        font7.setBold(True)
        font7.setItalic(True)
        font7.setWeight(75)
        self.label_41.setFont(font7)
        self.label_41.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_41.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_57.addWidget(self.label_41)

        self.label_47 = QLabel(self.frame_67)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFont(font7)
        self.label_47.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_47.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_57.addWidget(self.label_47)

        self.label_48 = QLabel(self.frame_67)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font7)
        self.label_48.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_48.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_57.addWidget(self.label_48)

        self.label_49 = QLabel(self.frame_67)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFont(font7)
        self.label_49.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_49.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_57.addWidget(self.label_49)

        self.label_50 = QLabel(self.frame_67)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font7)
        self.label_50.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_50.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_57.addWidget(self.label_50)

        self.label_51 = QLabel(self.frame_67)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setFont(font7)
        self.label_51.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_51.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_57.addWidget(self.label_51)

        self.verticalLayout_23.addWidget(self.frame_67)

        self.frame_71 = QFrame(self.page_parameter)
        self.frame_71.setObjectName(u"frame_71")
        self.frame_71.setStyleSheet(u"background-color: rgb(85, 255, 127);")
        self.frame_71.setFrameShape(QFrame.StyledPanel)
        self.frame_71.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_58 = QHBoxLayout(self.frame_71)
        self.horizontalLayout_58.setSpacing(0)
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.horizontalLayout_58.setContentsMargins(0, 0, 0, 0)
        self.frame_72 = QFrame(self.frame_71)
        self.frame_72.setObjectName(u"frame_72")
        self.frame_72.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                    "border-width: 2px;\n"
                                    "border-radius: 10px;")
        self.frame_72.setFrameShape(QFrame.StyledPanel)
        self.frame_72.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_59 = QHBoxLayout(self.frame_72)
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.frame_78 = QFrame(self.frame_72)
        self.frame_78.setObjectName(u"frame_78")
        self.frame_78.setMinimumSize(QSize(150, 0))
        self.frame_78.setMaximumSize(QSize(150, 16777215))
        self.frame_78.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_78.setFrameShape(QFrame.StyledPanel)
        self.frame_78.setFrameShadow(QFrame.Raised)
        self.verticalLayout_24 = QVBoxLayout(self.frame_78)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_52 = QLabel(self.frame_78)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setMinimumSize(QSize(0, 30))
        self.label_52.setMaximumSize(QSize(16777215, 30))
        self.label_52.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_52.setAlignment(Qt.AlignCenter)

        self.verticalLayout_24.addWidget(self.label_52)

        self.label_53 = QLabel(self.frame_78)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setMinimumSize(QSize(0, 30))
        self.label_53.setMaximumSize(QSize(16777215, 30))
        self.label_53.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_53.setAlignment(Qt.AlignCenter)

        self.verticalLayout_24.addWidget(self.label_53)

        self.label_54 = QLabel(self.frame_78)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setMinimumSize(QSize(0, 30))
        self.label_54.setMaximumSize(QSize(16777215, 30))
        self.label_54.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_54.setAlignment(Qt.AlignCenter)

        self.verticalLayout_24.addWidget(self.label_54)

        self.label_55 = QLabel(self.frame_78)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setMinimumSize(QSize(0, 30))
        self.label_55.setMaximumSize(QSize(16777215, 30))
        self.label_55.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_55.setAlignment(Qt.AlignCenter)

        self.verticalLayout_24.addWidget(self.label_55)

        self.frame_96 = QFrame(self.frame_78)
        self.frame_96.setObjectName(u"frame_96")
        self.frame_96.setFrameShape(QFrame.StyledPanel)
        self.frame_96.setFrameShadow(QFrame.Raised)

        self.verticalLayout_24.addWidget(self.frame_96)

        self.horizontalLayout_59.addWidget(self.frame_78)

        self.frame_79 = QFrame(self.frame_72)
        self.frame_79.setObjectName(u"frame_79")
        self.frame_79.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_79.setFrameShape(QFrame.StyledPanel)
        self.frame_79.setFrameShadow(QFrame.Raised)
        self.verticalLayout_30 = QVBoxLayout(self.frame_79)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.plainTextEdit_2 = QPlainTextEdit(self.frame_79)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        self.plainTextEdit_2.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_2.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_2.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_30.addWidget(self.plainTextEdit_2)

        self.plainTextEdit_3 = QPlainTextEdit(self.frame_79)
        self.plainTextEdit_3.setObjectName(u"plainTextEdit_3")
        self.plainTextEdit_3.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_3.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_3.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_30.addWidget(self.plainTextEdit_3)

        self.plainTextEdit_4 = QPlainTextEdit(self.frame_79)
        self.plainTextEdit_4.setObjectName(u"plainTextEdit_4")
        self.plainTextEdit_4.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_4.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_4.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_30.addWidget(self.plainTextEdit_4)

        self.plainTextEdit_5 = QPlainTextEdit(self.frame_79)
        self.plainTextEdit_5.setObjectName(u"plainTextEdit_5")
        self.plainTextEdit_5.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_5.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_5.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_30.addWidget(self.plainTextEdit_5)

        self.frame_97 = QFrame(self.frame_79)
        self.frame_97.setObjectName(u"frame_97")
        self.frame_97.setFrameShape(QFrame.StyledPanel)
        self.frame_97.setFrameShadow(QFrame.Raised)

        self.verticalLayout_30.addWidget(self.frame_97)

        self.horizontalLayout_59.addWidget(self.frame_79)

        self.frame_80 = QFrame(self.frame_72)
        self.frame_80.setObjectName(u"frame_80")
        self.frame_80.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_80.setFrameShape(QFrame.StyledPanel)
        self.frame_80.setFrameShadow(QFrame.Raised)
        self.verticalLayout_36 = QVBoxLayout(self.frame_80)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.plainTextEdit_28 = QPlainTextEdit(self.frame_80)
        self.plainTextEdit_28.setObjectName(u"plainTextEdit_28")
        self.plainTextEdit_28.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_28.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_28.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_36.addWidget(self.plainTextEdit_28)

        self.plainTextEdit_26 = QPlainTextEdit(self.frame_80)
        self.plainTextEdit_26.setObjectName(u"plainTextEdit_26")
        self.plainTextEdit_26.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_26.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_26.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_36.addWidget(self.plainTextEdit_26)

        self.plainTextEdit_27 = QPlainTextEdit(self.frame_80)
        self.plainTextEdit_27.setObjectName(u"plainTextEdit_27")
        self.plainTextEdit_27.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_27.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_27.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_36.addWidget(self.plainTextEdit_27)

        self.plainTextEdit_29 = QPlainTextEdit(self.frame_80)
        self.plainTextEdit_29.setObjectName(u"plainTextEdit_29")
        self.plainTextEdit_29.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_29.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_29.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_36.addWidget(self.plainTextEdit_29)

        self.frame_98 = QFrame(self.frame_80)
        self.frame_98.setObjectName(u"frame_98")
        self.frame_98.setFrameShape(QFrame.StyledPanel)
        self.frame_98.setFrameShadow(QFrame.Raised)

        self.verticalLayout_36.addWidget(self.frame_98)

        self.horizontalLayout_59.addWidget(self.frame_80)

        self.horizontalLayout_58.addWidget(self.frame_72)

        self.frame_73 = QFrame(self.frame_71)
        self.frame_73.setObjectName(u"frame_73")
        self.frame_73.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                    "border-width: 2px;\n"
                                    "border-radius: 10px;")
        self.frame_73.setFrameShape(QFrame.StyledPanel)
        self.frame_73.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_60 = QHBoxLayout(self.frame_73)
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.frame_81 = QFrame(self.frame_73)
        self.frame_81.setObjectName(u"frame_81")
        self.frame_81.setMinimumSize(QSize(150, 0))
        self.frame_81.setMaximumSize(QSize(150, 16777215))
        self.frame_81.setStyleSheet(u"\n"
                                    "background-color: rgb(0, 0, 0);")
        self.frame_81.setFrameShape(QFrame.StyledPanel)
        self.frame_81.setFrameShadow(QFrame.Raised)
        self.verticalLayout_25 = QVBoxLayout(self.frame_81)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.label_56 = QLabel(self.frame_81)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setMinimumSize(QSize(0, 30))
        self.label_56.setMaximumSize(QSize(16777215, 30))
        self.label_56.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_56.setAlignment(Qt.AlignCenter)

        self.verticalLayout_25.addWidget(self.label_56)

        self.label_57 = QLabel(self.frame_81)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setMinimumSize(QSize(0, 30))
        self.label_57.setMaximumSize(QSize(16777215, 30))
        self.label_57.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_57.setAlignment(Qt.AlignCenter)

        self.verticalLayout_25.addWidget(self.label_57)

        self.label_58 = QLabel(self.frame_81)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setMinimumSize(QSize(0, 30))
        self.label_58.setMaximumSize(QSize(16777215, 30))
        self.label_58.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_58.setAlignment(Qt.AlignCenter)

        self.verticalLayout_25.addWidget(self.label_58)

        self.label_59 = QLabel(self.frame_81)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setMinimumSize(QSize(0, 30))
        self.label_59.setMaximumSize(QSize(16777215, 30))
        self.label_59.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_59.setAlignment(Qt.AlignCenter)

        self.verticalLayout_25.addWidget(self.label_59)

        self.frame_99 = QFrame(self.frame_81)
        self.frame_99.setObjectName(u"frame_99")
        self.frame_99.setFrameShape(QFrame.StyledPanel)
        self.frame_99.setFrameShadow(QFrame.Raised)

        self.verticalLayout_25.addWidget(self.frame_99)

        self.horizontalLayout_60.addWidget(self.frame_81)

        self.frame_83 = QFrame(self.frame_73)
        self.frame_83.setObjectName(u"frame_83")
        self.frame_83.setStyleSheet(u"\n"
                                    "background-color: rgb(0, 0, 0);")
        self.frame_83.setFrameShape(QFrame.StyledPanel)
        self.frame_83.setFrameShadow(QFrame.Raised)
        self.verticalLayout_31 = QVBoxLayout(self.frame_83)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.plainTextEdit_6 = QPlainTextEdit(self.frame_83)
        self.plainTextEdit_6.setObjectName(u"plainTextEdit_6")
        self.plainTextEdit_6.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_6.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_6.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_31.addWidget(self.plainTextEdit_6)

        self.plainTextEdit_7 = QPlainTextEdit(self.frame_83)
        self.plainTextEdit_7.setObjectName(u"plainTextEdit_7")
        self.plainTextEdit_7.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_7.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_7.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_31.addWidget(self.plainTextEdit_7)

        self.plainTextEdit_8 = QPlainTextEdit(self.frame_83)
        self.plainTextEdit_8.setObjectName(u"plainTextEdit_8")
        self.plainTextEdit_8.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_8.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_8.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_31.addWidget(self.plainTextEdit_8)

        self.plainTextEdit_9 = QPlainTextEdit(self.frame_83)
        self.plainTextEdit_9.setObjectName(u"plainTextEdit_9")
        self.plainTextEdit_9.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_9.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_9.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_31.addWidget(self.plainTextEdit_9)

        self.frame_100 = QFrame(self.frame_83)
        self.frame_100.setObjectName(u"frame_100")
        self.frame_100.setFrameShape(QFrame.StyledPanel)
        self.frame_100.setFrameShadow(QFrame.Raised)

        self.verticalLayout_31.addWidget(self.frame_100)

        self.horizontalLayout_60.addWidget(self.frame_83)

        self.frame_82 = QFrame(self.frame_73)
        self.frame_82.setObjectName(u"frame_82")
        self.frame_82.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_82.setFrameShape(QFrame.StyledPanel)
        self.frame_82.setFrameShadow(QFrame.Raised)
        self.verticalLayout_37 = QVBoxLayout(self.frame_82)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.plainTextEdit_33 = QPlainTextEdit(self.frame_82)
        self.plainTextEdit_33.setObjectName(u"plainTextEdit_33")
        self.plainTextEdit_33.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_33.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_33.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_37.addWidget(self.plainTextEdit_33)

        self.plainTextEdit_30 = QPlainTextEdit(self.frame_82)
        self.plainTextEdit_30.setObjectName(u"plainTextEdit_30")
        self.plainTextEdit_30.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_30.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_30.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_37.addWidget(self.plainTextEdit_30)

        self.plainTextEdit_31 = QPlainTextEdit(self.frame_82)
        self.plainTextEdit_31.setObjectName(u"plainTextEdit_31")
        self.plainTextEdit_31.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_31.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_31.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_37.addWidget(self.plainTextEdit_31)

        self.plainTextEdit_32 = QPlainTextEdit(self.frame_82)
        self.plainTextEdit_32.setObjectName(u"plainTextEdit_32")
        self.plainTextEdit_32.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_32.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_32.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_37.addWidget(self.plainTextEdit_32)

        self.frame_101 = QFrame(self.frame_82)
        self.frame_101.setObjectName(u"frame_101")
        self.frame_101.setFrameShape(QFrame.StyledPanel)
        self.frame_101.setFrameShadow(QFrame.Raised)

        self.verticalLayout_37.addWidget(self.frame_101)

        self.horizontalLayout_60.addWidget(self.frame_82)

        self.horizontalLayout_58.addWidget(self.frame_73)

        self.frame_74 = QFrame(self.frame_71)
        self.frame_74.setObjectName(u"frame_74")
        self.frame_74.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                    "border-width: 2px;\n"
                                    "border-radius: 10px;")
        self.frame_74.setFrameShape(QFrame.StyledPanel)
        self.frame_74.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_61 = QHBoxLayout(self.frame_74)
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.frame_84 = QFrame(self.frame_74)
        self.frame_84.setObjectName(u"frame_84")
        self.frame_84.setMinimumSize(QSize(150, 0))
        self.frame_84.setMaximumSize(QSize(150, 16777215))
        self.frame_84.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_84.setFrameShape(QFrame.StyledPanel)
        self.frame_84.setFrameShadow(QFrame.Raised)
        self.verticalLayout_26 = QVBoxLayout(self.frame_84)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.label_60 = QLabel(self.frame_84)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setMinimumSize(QSize(0, 30))
        self.label_60.setMaximumSize(QSize(16777215, 30))
        self.label_60.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_60.setAlignment(Qt.AlignCenter)

        self.verticalLayout_26.addWidget(self.label_60)

        self.label_61 = QLabel(self.frame_84)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setMinimumSize(QSize(0, 30))
        self.label_61.setMaximumSize(QSize(16777215, 30))
        self.label_61.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_61.setAlignment(Qt.AlignCenter)

        self.verticalLayout_26.addWidget(self.label_61)

        self.label_62 = QLabel(self.frame_84)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setMinimumSize(QSize(0, 30))
        self.label_62.setMaximumSize(QSize(16777215, 30))
        self.label_62.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_62.setAlignment(Qt.AlignCenter)

        self.verticalLayout_26.addWidget(self.label_62)

        self.label_63 = QLabel(self.frame_84)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setMinimumSize(QSize(0, 30))
        self.label_63.setMaximumSize(QSize(16777215, 30))
        self.label_63.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_63.setAlignment(Qt.AlignCenter)

        self.verticalLayout_26.addWidget(self.label_63)

        self.frame_102 = QFrame(self.frame_84)
        self.frame_102.setObjectName(u"frame_102")
        self.frame_102.setFrameShape(QFrame.StyledPanel)
        self.frame_102.setFrameShadow(QFrame.Raised)

        self.verticalLayout_26.addWidget(self.frame_102)

        self.horizontalLayout_61.addWidget(self.frame_84)

        self.frame_85 = QFrame(self.frame_74)
        self.frame_85.setObjectName(u"frame_85")
        self.frame_85.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_85.setFrameShape(QFrame.StyledPanel)
        self.frame_85.setFrameShadow(QFrame.Raised)
        self.verticalLayout_32 = QVBoxLayout(self.frame_85)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.plainTextEdit_11 = QPlainTextEdit(self.frame_85)
        self.plainTextEdit_11.setObjectName(u"plainTextEdit_11")
        self.plainTextEdit_11.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_11.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_11.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_32.addWidget(self.plainTextEdit_11)

        self.plainTextEdit_10 = QPlainTextEdit(self.frame_85)
        self.plainTextEdit_10.setObjectName(u"plainTextEdit_10")
        self.plainTextEdit_10.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_10.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_10.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_32.addWidget(self.plainTextEdit_10)

        self.plainTextEdit_12 = QPlainTextEdit(self.frame_85)
        self.plainTextEdit_12.setObjectName(u"plainTextEdit_12")
        self.plainTextEdit_12.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_12.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_12.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_32.addWidget(self.plainTextEdit_12)

        self.plainTextEdit_13 = QPlainTextEdit(self.frame_85)
        self.plainTextEdit_13.setObjectName(u"plainTextEdit_13")
        self.plainTextEdit_13.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_13.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_13.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_32.addWidget(self.plainTextEdit_13)

        self.frame_103 = QFrame(self.frame_85)
        self.frame_103.setObjectName(u"frame_103")
        self.frame_103.setFrameShape(QFrame.StyledPanel)
        self.frame_103.setFrameShadow(QFrame.Raised)

        self.verticalLayout_32.addWidget(self.frame_103)

        self.horizontalLayout_61.addWidget(self.frame_85)

        self.frame_86 = QFrame(self.frame_74)
        self.frame_86.setObjectName(u"frame_86")
        self.frame_86.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_86.setFrameShape(QFrame.StyledPanel)
        self.frame_86.setFrameShadow(QFrame.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.frame_86)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.plainTextEdit_37 = QPlainTextEdit(self.frame_86)
        self.plainTextEdit_37.setObjectName(u"plainTextEdit_37")
        self.plainTextEdit_37.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_37.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_37.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_38.addWidget(self.plainTextEdit_37)

        self.plainTextEdit_36 = QPlainTextEdit(self.frame_86)
        self.plainTextEdit_36.setObjectName(u"plainTextEdit_36")
        self.plainTextEdit_36.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_36.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_36.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_38.addWidget(self.plainTextEdit_36)

        self.plainTextEdit_34 = QPlainTextEdit(self.frame_86)
        self.plainTextEdit_34.setObjectName(u"plainTextEdit_34")
        self.plainTextEdit_34.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_34.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_34.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_38.addWidget(self.plainTextEdit_34)

        self.plainTextEdit_35 = QPlainTextEdit(self.frame_86)
        self.plainTextEdit_35.setObjectName(u"plainTextEdit_35")
        self.plainTextEdit_35.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_35.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_35.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_38.addWidget(self.plainTextEdit_35)

        self.frame_104 = QFrame(self.frame_86)
        self.frame_104.setObjectName(u"frame_104")
        self.frame_104.setFrameShape(QFrame.StyledPanel)
        self.frame_104.setFrameShadow(QFrame.Raised)

        self.verticalLayout_38.addWidget(self.frame_104)

        self.horizontalLayout_61.addWidget(self.frame_86)

        self.horizontalLayout_58.addWidget(self.frame_74)

        self.frame_75 = QFrame(self.frame_71)
        self.frame_75.setObjectName(u"frame_75")
        self.frame_75.setStyleSheet(u"background-color: rgb(118, 118, 118);border-width: 2px;\n"
                                    "border-radius: 10px;")
        self.frame_75.setFrameShape(QFrame.StyledPanel)
        self.frame_75.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_62 = QHBoxLayout(self.frame_75)
        self.horizontalLayout_62.setObjectName(u"horizontalLayout_62")
        self.frame_89 = QFrame(self.frame_75)
        self.frame_89.setObjectName(u"frame_89")
        self.frame_89.setMinimumSize(QSize(150, 0))
        self.frame_89.setMaximumSize(QSize(150, 16777215))
        self.frame_89.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_89.setFrameShape(QFrame.StyledPanel)
        self.frame_89.setFrameShadow(QFrame.Raised)
        self.verticalLayout_27 = QVBoxLayout(self.frame_89)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.label_64 = QLabel(self.frame_89)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setMinimumSize(QSize(0, 30))
        self.label_64.setMaximumSize(QSize(16777215, 30))
        self.label_64.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_64.setAlignment(Qt.AlignCenter)

        self.verticalLayout_27.addWidget(self.label_64)

        self.label_65 = QLabel(self.frame_89)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setMinimumSize(QSize(0, 30))
        self.label_65.setMaximumSize(QSize(16777215, 30))
        self.label_65.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_65.setAlignment(Qt.AlignCenter)

        self.verticalLayout_27.addWidget(self.label_65)

        self.label_66 = QLabel(self.frame_89)
        self.label_66.setObjectName(u"label_66")
        self.label_66.setMinimumSize(QSize(0, 30))
        self.label_66.setMaximumSize(QSize(16777215, 30))
        self.label_66.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_66.setAlignment(Qt.AlignCenter)

        self.verticalLayout_27.addWidget(self.label_66)

        self.label_67 = QLabel(self.frame_89)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setMinimumSize(QSize(0, 30))
        self.label_67.setMaximumSize(QSize(16777215, 30))
        self.label_67.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_67.setAlignment(Qt.AlignCenter)

        self.verticalLayout_27.addWidget(self.label_67)

        self.frame_105 = QFrame(self.frame_89)
        self.frame_105.setObjectName(u"frame_105")
        self.frame_105.setFrameShape(QFrame.StyledPanel)
        self.frame_105.setFrameShadow(QFrame.Raised)

        self.verticalLayout_27.addWidget(self.frame_105)

        self.horizontalLayout_62.addWidget(self.frame_89)

        self.frame_87 = QFrame(self.frame_75)
        self.frame_87.setObjectName(u"frame_87")
        self.frame_87.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_87.setFrameShape(QFrame.StyledPanel)
        self.frame_87.setFrameShadow(QFrame.Raised)
        self.verticalLayout_33 = QVBoxLayout(self.frame_87)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.plainTextEdit_16 = QPlainTextEdit(self.frame_87)
        self.plainTextEdit_16.setObjectName(u"plainTextEdit_16")
        self.plainTextEdit_16.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_16.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_16.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_33.addWidget(self.plainTextEdit_16)

        self.plainTextEdit_14 = QPlainTextEdit(self.frame_87)
        self.plainTextEdit_14.setObjectName(u"plainTextEdit_14")
        self.plainTextEdit_14.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_14.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_14.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_33.addWidget(self.plainTextEdit_14)

        self.plainTextEdit_15 = QPlainTextEdit(self.frame_87)
        self.plainTextEdit_15.setObjectName(u"plainTextEdit_15")
        self.plainTextEdit_15.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_15.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_15.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_33.addWidget(self.plainTextEdit_15)

        self.plainTextEdit_17 = QPlainTextEdit(self.frame_87)
        self.plainTextEdit_17.setObjectName(u"plainTextEdit_17")
        self.plainTextEdit_17.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_17.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_17.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_33.addWidget(self.plainTextEdit_17)

        self.frame_106 = QFrame(self.frame_87)
        self.frame_106.setObjectName(u"frame_106")
        self.frame_106.setFrameShape(QFrame.StyledPanel)
        self.frame_106.setFrameShadow(QFrame.Raised)

        self.verticalLayout_33.addWidget(self.frame_106)

        self.horizontalLayout_62.addWidget(self.frame_87)

        self.frame_88 = QFrame(self.frame_75)
        self.frame_88.setObjectName(u"frame_88")
        self.frame_88.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_88.setFrameShape(QFrame.StyledPanel)
        self.frame_88.setFrameShadow(QFrame.Raised)
        self.verticalLayout_39 = QVBoxLayout(self.frame_88)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.plainTextEdit_41 = QPlainTextEdit(self.frame_88)
        self.plainTextEdit_41.setObjectName(u"plainTextEdit_41")
        self.plainTextEdit_41.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_41.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_41.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_39.addWidget(self.plainTextEdit_41)

        self.plainTextEdit_40 = QPlainTextEdit(self.frame_88)
        self.plainTextEdit_40.setObjectName(u"plainTextEdit_40")
        self.plainTextEdit_40.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_40.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_40.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_39.addWidget(self.plainTextEdit_40)

        self.plainTextEdit_39 = QPlainTextEdit(self.frame_88)
        self.plainTextEdit_39.setObjectName(u"plainTextEdit_39")
        self.plainTextEdit_39.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_39.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_39.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_39.addWidget(self.plainTextEdit_39)

        self.plainTextEdit_38 = QPlainTextEdit(self.frame_88)
        self.plainTextEdit_38.setObjectName(u"plainTextEdit_38")
        self.plainTextEdit_38.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_38.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_38.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_39.addWidget(self.plainTextEdit_38)

        self.frame_107 = QFrame(self.frame_88)
        self.frame_107.setObjectName(u"frame_107")
        self.frame_107.setFrameShape(QFrame.StyledPanel)
        self.frame_107.setFrameShadow(QFrame.Raised)

        self.verticalLayout_39.addWidget(self.frame_107)

        self.horizontalLayout_62.addWidget(self.frame_88)

        self.horizontalLayout_58.addWidget(self.frame_75)

        self.frame_76 = QFrame(self.frame_71)
        self.frame_76.setObjectName(u"frame_76")
        self.frame_76.setStyleSheet(u"border-width: 2px;\n"
                                    "border-radius: 10px;background-color: rgb(118, 118, 118);")
        self.frame_76.setFrameShape(QFrame.StyledPanel)
        self.frame_76.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_63 = QHBoxLayout(self.frame_76)
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.frame_90 = QFrame(self.frame_76)
        self.frame_90.setObjectName(u"frame_90")
        self.frame_90.setMinimumSize(QSize(150, 0))
        self.frame_90.setMaximumSize(QSize(150, 16777215))
        self.frame_90.setStyleSheet(u"border-width: 2px;\n"
                                    "border-radius: 10px;background-color: rgb(0, 0, 0);")
        self.frame_90.setFrameShape(QFrame.StyledPanel)
        self.frame_90.setFrameShadow(QFrame.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.frame_90)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.label_68 = QLabel(self.frame_90)
        self.label_68.setObjectName(u"label_68")
        self.label_68.setMinimumSize(QSize(0, 30))
        self.label_68.setMaximumSize(QSize(16777215, 30))
        self.label_68.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_68.setAlignment(Qt.AlignCenter)

        self.verticalLayout_28.addWidget(self.label_68)

        self.label_69 = QLabel(self.frame_90)
        self.label_69.setObjectName(u"label_69")
        self.label_69.setMinimumSize(QSize(0, 30))
        self.label_69.setMaximumSize(QSize(16777215, 30))
        self.label_69.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_69.setAlignment(Qt.AlignCenter)

        self.verticalLayout_28.addWidget(self.label_69)

        self.label_70 = QLabel(self.frame_90)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setMinimumSize(QSize(0, 30))
        self.label_70.setMaximumSize(QSize(16777215, 30))
        self.label_70.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_70.setAlignment(Qt.AlignCenter)

        self.verticalLayout_28.addWidget(self.label_70)

        self.label_71 = QLabel(self.frame_90)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setMinimumSize(QSize(0, 30))
        self.label_71.setMaximumSize(QSize(16777215, 30))
        self.label_71.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_71.setAlignment(Qt.AlignCenter)

        self.verticalLayout_28.addWidget(self.label_71)

        self.frame_108 = QFrame(self.frame_90)
        self.frame_108.setObjectName(u"frame_108")
        self.frame_108.setFrameShape(QFrame.StyledPanel)
        self.frame_108.setFrameShadow(QFrame.Raised)

        self.verticalLayout_28.addWidget(self.frame_108)

        self.horizontalLayout_63.addWidget(self.frame_90)

        self.frame_91 = QFrame(self.frame_76)
        self.frame_91.setObjectName(u"frame_91")
        self.frame_91.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_91.setFrameShape(QFrame.StyledPanel)
        self.frame_91.setFrameShadow(QFrame.Raised)
        self.verticalLayout_34 = QVBoxLayout(self.frame_91)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.plainTextEdit_20 = QPlainTextEdit(self.frame_91)
        self.plainTextEdit_20.setObjectName(u"plainTextEdit_20")
        self.plainTextEdit_20.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_20.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_20.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_34.addWidget(self.plainTextEdit_20)

        self.plainTextEdit_18 = QPlainTextEdit(self.frame_91)
        self.plainTextEdit_18.setObjectName(u"plainTextEdit_18")
        self.plainTextEdit_18.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_18.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_18.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_34.addWidget(self.plainTextEdit_18)

        self.plainTextEdit_19 = QPlainTextEdit(self.frame_91)
        self.plainTextEdit_19.setObjectName(u"plainTextEdit_19")
        self.plainTextEdit_19.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_19.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_19.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_34.addWidget(self.plainTextEdit_19)

        self.plainTextEdit_21 = QPlainTextEdit(self.frame_91)
        self.plainTextEdit_21.setObjectName(u"plainTextEdit_21")
        self.plainTextEdit_21.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_21.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_21.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_34.addWidget(self.plainTextEdit_21)

        self.frame_109 = QFrame(self.frame_91)
        self.frame_109.setObjectName(u"frame_109")
        self.frame_109.setFrameShape(QFrame.StyledPanel)
        self.frame_109.setFrameShadow(QFrame.Raised)

        self.verticalLayout_34.addWidget(self.frame_109)

        self.horizontalLayout_63.addWidget(self.frame_91)

        self.frame_92 = QFrame(self.frame_76)
        self.frame_92.setObjectName(u"frame_92")
        self.frame_92.setMinimumSize(QSize(0, 30))
        self.frame_92.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_92.setFrameShape(QFrame.StyledPanel)
        self.frame_92.setFrameShadow(QFrame.Raised)
        self.verticalLayout_40 = QVBoxLayout(self.frame_92)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.plainTextEdit_44 = QPlainTextEdit(self.frame_92)
        self.plainTextEdit_44.setObjectName(u"plainTextEdit_44")
        self.plainTextEdit_44.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_44.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_44.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_40.addWidget(self.plainTextEdit_44)

        self.plainTextEdit_42 = QPlainTextEdit(self.frame_92)
        self.plainTextEdit_42.setObjectName(u"plainTextEdit_42")
        self.plainTextEdit_42.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_42.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_42.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_40.addWidget(self.plainTextEdit_42)

        self.plainTextEdit_43 = QPlainTextEdit(self.frame_92)
        self.plainTextEdit_43.setObjectName(u"plainTextEdit_43")
        self.plainTextEdit_43.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_43.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_43.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_40.addWidget(self.plainTextEdit_43)

        self.plainTextEdit_45 = QPlainTextEdit(self.frame_92)
        self.plainTextEdit_45.setObjectName(u"plainTextEdit_45")
        self.plainTextEdit_45.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_45.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_45.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_40.addWidget(self.plainTextEdit_45)

        self.frame_110 = QFrame(self.frame_92)
        self.frame_110.setObjectName(u"frame_110")
        self.frame_110.setFrameShape(QFrame.StyledPanel)
        self.frame_110.setFrameShadow(QFrame.Raised)

        self.verticalLayout_40.addWidget(self.frame_110)

        self.horizontalLayout_63.addWidget(self.frame_92)

        self.horizontalLayout_58.addWidget(self.frame_76)

        self.frame_77 = QFrame(self.frame_71)
        self.frame_77.setObjectName(u"frame_77")
        self.frame_77.setStyleSheet(u"border-width: 2px;\n"
                                    "border-radius: 10px;background-color: rgb(118, 118, 118);")
        self.frame_77.setFrameShape(QFrame.StyledPanel)
        self.frame_77.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_64 = QHBoxLayout(self.frame_77)
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.frame_93 = QFrame(self.frame_77)
        self.frame_93.setObjectName(u"frame_93")
        self.frame_93.setMinimumSize(QSize(150, 0))
        self.frame_93.setMaximumSize(QSize(150, 16777215))
        self.frame_93.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_93.setFrameShape(QFrame.StyledPanel)
        self.frame_93.setFrameShadow(QFrame.Raised)
        self.verticalLayout_29 = QVBoxLayout(self.frame_93)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.label_72 = QLabel(self.frame_93)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setMinimumSize(QSize(0, 30))
        self.label_72.setMaximumSize(QSize(16777215, 30))
        self.label_72.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_72.setAlignment(Qt.AlignCenter)

        self.verticalLayout_29.addWidget(self.label_72)

        self.label_73 = QLabel(self.frame_93)
        self.label_73.setObjectName(u"label_73")
        self.label_73.setMinimumSize(QSize(0, 30))
        self.label_73.setMaximumSize(QSize(16777215, 30))
        self.label_73.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_73.setAlignment(Qt.AlignCenter)

        self.verticalLayout_29.addWidget(self.label_73)

        self.label_74 = QLabel(self.frame_93)
        self.label_74.setObjectName(u"label_74")
        self.label_74.setMinimumSize(QSize(0, 30))
        self.label_74.setMaximumSize(QSize(16777215, 30))
        self.label_74.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_74.setAlignment(Qt.AlignCenter)

        self.verticalLayout_29.addWidget(self.label_74)

        self.label_75 = QLabel(self.frame_93)
        self.label_75.setObjectName(u"label_75")
        self.label_75.setMinimumSize(QSize(0, 30))
        self.label_75.setMaximumSize(QSize(16777215, 30))
        self.label_75.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_75.setAlignment(Qt.AlignCenter)

        self.verticalLayout_29.addWidget(self.label_75)

        self.frame_111 = QFrame(self.frame_93)
        self.frame_111.setObjectName(u"frame_111")
        self.frame_111.setFrameShape(QFrame.StyledPanel)
        self.frame_111.setFrameShadow(QFrame.Raised)

        self.verticalLayout_29.addWidget(self.frame_111)

        self.horizontalLayout_64.addWidget(self.frame_93)

        self.frame_95 = QFrame(self.frame_77)
        self.frame_95.setObjectName(u"frame_95")
        self.frame_95.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_95.setFrameShape(QFrame.StyledPanel)
        self.frame_95.setFrameShadow(QFrame.Raised)
        self.verticalLayout_35 = QVBoxLayout(self.frame_95)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.plainTextEdit_25 = QPlainTextEdit(self.frame_95)
        self.plainTextEdit_25.setObjectName(u"plainTextEdit_25")
        self.plainTextEdit_25.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_25.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_25.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_35.addWidget(self.plainTextEdit_25)

        self.plainTextEdit_22 = QPlainTextEdit(self.frame_95)
        self.plainTextEdit_22.setObjectName(u"plainTextEdit_22")
        self.plainTextEdit_22.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_22.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_22.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_35.addWidget(self.plainTextEdit_22)

        self.plainTextEdit_23 = QPlainTextEdit(self.frame_95)
        self.plainTextEdit_23.setObjectName(u"plainTextEdit_23")
        self.plainTextEdit_23.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_23.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_23.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_35.addWidget(self.plainTextEdit_23)

        self.plainTextEdit_24 = QPlainTextEdit(self.frame_95)
        self.plainTextEdit_24.setObjectName(u"plainTextEdit_24")
        self.plainTextEdit_24.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_24.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_24.setStyleSheet(
            u"background-color: rgb(170, 170, 255);")

        self.verticalLayout_35.addWidget(self.plainTextEdit_24)

        self.frame_112 = QFrame(self.frame_95)
        self.frame_112.setObjectName(u"frame_112")
        self.frame_112.setFrameShape(QFrame.StyledPanel)
        self.frame_112.setFrameShadow(QFrame.Raised)

        self.verticalLayout_35.addWidget(self.frame_112)

        self.horizontalLayout_64.addWidget(self.frame_95)

        self.frame_94 = QFrame(self.frame_77)
        self.frame_94.setObjectName(u"frame_94")
        self.frame_94.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_94.setFrameShape(QFrame.StyledPanel)
        self.frame_94.setFrameShadow(QFrame.Raised)
        self.verticalLayout_41 = QVBoxLayout(self.frame_94)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.plainTextEdit_48 = QPlainTextEdit(self.frame_94)
        self.plainTextEdit_48.setObjectName(u"plainTextEdit_48")
        self.plainTextEdit_48.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_48.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_48.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_41.addWidget(self.plainTextEdit_48)

        self.plainTextEdit_46 = QPlainTextEdit(self.frame_94)
        self.plainTextEdit_46.setObjectName(u"plainTextEdit_46")
        self.plainTextEdit_46.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_46.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_46.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_41.addWidget(self.plainTextEdit_46)

        self.plainTextEdit_47 = QPlainTextEdit(self.frame_94)
        self.plainTextEdit_47.setObjectName(u"plainTextEdit_47")
        self.plainTextEdit_47.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_47.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_47.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_41.addWidget(self.plainTextEdit_47)

        self.plainTextEdit_49 = QPlainTextEdit(self.frame_94)
        self.plainTextEdit_49.setObjectName(u"plainTextEdit_49")
        self.plainTextEdit_49.setMinimumSize(QSize(30, 30))
        self.plainTextEdit_49.setMaximumSize(QSize(30, 30))
        self.plainTextEdit_49.setStyleSheet(
            u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_41.addWidget(self.plainTextEdit_49)

        self.frame_113 = QFrame(self.frame_94)
        self.frame_113.setObjectName(u"frame_113")
        self.frame_113.setFrameShape(QFrame.StyledPanel)
        self.frame_113.setFrameShadow(QFrame.Raised)

        self.verticalLayout_41.addWidget(self.frame_113)

        self.horizontalLayout_64.addWidget(self.frame_94)

        self.horizontalLayout_58.addWidget(self.frame_77)

        self.verticalLayout_23.addWidget(self.frame_71)

        self.stackedWidget.addWidget(self.page_parameter)
        self.page_map = QWidget()
        self.page_map.setObjectName(u"page_map")
        self.verticalLayout_15 = QVBoxLayout(self.page_map)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.frame_38 = QFrame(self.page_map)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setMinimumSize(QSize(0, 60))
        self.frame_38.setMaximumSize(QSize(16777215, 60))
        self.frame_38.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_38.setFrameShape(QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.frame_38)
        self.horizontalLayout_32.setSpacing(0)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.frame_38)
        self.label_11.setObjectName(u"label_11")
        font8 = QFont()
        font8.setPointSize(20)
        font8.setBold(True)
        font8.setItalic(True)
        font8.setWeight(75)
        self.label_11.setFont(font8)
        self.label_11.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_32.addWidget(self.label_11)

        self.label_45 = QLabel(self.frame_38)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font8)
        self.label_45.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_45.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_32.addWidget(self.label_45)

        self.label_80 = QLabel(self.frame_38)
        self.label_80.setObjectName(u"label_80")
        self.label_80.setFont(font8)
        self.label_80.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_80.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_32.addWidget(self.label_80)

        self.label_83 = QLabel(self.frame_38)
        self.label_83.setObjectName(u"label_83")
        self.label_83.setFont(font8)
        self.label_83.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_83.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_32.addWidget(self.label_83)

        self.label_84 = QLabel(self.frame_38)
        self.label_84.setObjectName(u"label_84")
        self.label_84.setFont(font8)
        self.label_84.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_84.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_32.addWidget(self.label_84)

        self.label_85 = QLabel(self.frame_38)
        self.label_85.setObjectName(u"label_85")
        self.label_85.setFont(font8)
        self.label_85.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_85.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_32.addWidget(self.label_85)

        self.verticalLayout_15.addWidget(self.frame_38)

        self.frame_39 = QFrame(self.page_map)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setMinimumSize(QSize(0, 23))
        self.frame_39.setMaximumSize(QSize(16777215, 23))
        self.frame_39.setStyleSheet(u"background-color: rgb(255, 170, 127);")
        self.frame_39.setFrameShape(QFrame.StyledPanel)
        self.frame_39.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_35 = QHBoxLayout(self.frame_39)
        self.horizontalLayout_35.setSpacing(0)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.frame_49 = QFrame(self.frame_39)
        self.frame_49.setObjectName(u"frame_49")
        self.frame_49.setMinimumSize(QSize(269, 23))
        self.frame_49.setMaximumSize(QSize(269, 23))
        self.frame_49.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_49.setFrameShape(QFrame.StyledPanel)
        self.frame_49.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_33 = QHBoxLayout(self.frame_49)
        self.horizontalLayout_33.setSpacing(0)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.file_1 = QPushButton(self.frame_49)
        self.file_1.setObjectName(u"file_1")
        self.file_1.setMinimumSize(QSize(28, 23))
        self.file_1.setMaximumSize(QSize(28, 25))
        self.file_1.setFont(font7)
        self.file_1.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        icon10 = QIcon()
        icon10.addFile(f"{icons_dir}/file.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.file_1.setIcon(icon10)
        self.file_1.setIconSize(QSize(24, 24))

        self.horizontalLayout_33.addWidget(self.file_1)

        self.link_uav1 = QPlainTextEdit(self.frame_49)
        self.link_uav1.setObjectName(u"link_uav1")
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        brush1 = QBrush(QColor(0, 0, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Active, QPalette.HighlightedText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush1)
        self.link_uav1.setPalette(palette)
        self.link_uav1.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;\n"
                                     "")

        self.horizontalLayout_33.addWidget(self.link_uav1)

        self.horizontalLayout_35.addWidget(self.frame_49)

        self.frame_50 = QFrame(self.frame_39)
        self.frame_50.setObjectName(u"frame_50")
        self.frame_50.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_50.setFrameShape(QFrame.StyledPanel)
        self.frame_50.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_46 = QHBoxLayout(self.frame_50)
        self.horizontalLayout_46.setSpacing(0)
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.horizontalLayout_46.setContentsMargins(0, 0, 9, 0)
        self.file_2 = QPushButton(self.frame_50)
        self.file_2.setObjectName(u"file_2")
        self.file_2.setMinimumSize(QSize(28, 23))
        self.file_2.setMaximumSize(QSize(28, 23))
        self.file_2.setFont(font7)
        self.file_2.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.file_2.setIcon(icon10)
        self.file_2.setIconSize(QSize(24, 24))

        self.horizontalLayout_46.addWidget(self.file_2)

        self.link_uav2 = QPlainTextEdit(self.frame_50)
        self.link_uav2.setObjectName(u"link_uav2")
        self.link_uav2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_46.addWidget(self.link_uav2)

        self.horizontalLayout_35.addWidget(self.frame_50)

        self.frame_51 = QFrame(self.frame_39)
        self.frame_51.setObjectName(u"frame_51")
        self.frame_51.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_51.setFrameShape(QFrame.StyledPanel)
        self.frame_51.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_45 = QHBoxLayout(self.frame_51)
        self.horizontalLayout_45.setSpacing(0)
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.horizontalLayout_45.setContentsMargins(0, 0, 9, 0)
        self.file_3 = QPushButton(self.frame_51)
        self.file_3.setObjectName(u"file_3")
        self.file_3.setMinimumSize(QSize(28, 23))
        self.file_3.setMaximumSize(QSize(28, 23))
        self.file_3.setFont(font7)
        self.file_3.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.file_3.setIcon(icon10)
        self.file_3.setIconSize(QSize(24, 24))

        self.horizontalLayout_45.addWidget(self.file_3)

        self.link_uav3 = QPlainTextEdit(self.frame_51)
        self.link_uav3.setObjectName(u"link_uav3")
        self.link_uav3.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_45.addWidget(self.link_uav3)

        self.horizontalLayout_35.addWidget(self.frame_51)

        self.frame_52 = QFrame(self.frame_39)
        self.frame_52.setObjectName(u"frame_52")
        self.frame_52.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_52.setFrameShape(QFrame.StyledPanel)
        self.frame_52.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_44 = QHBoxLayout(self.frame_52)
        self.horizontalLayout_44.setSpacing(0)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.horizontalLayout_44.setContentsMargins(0, 0, 9, 0)
        self.file_4 = QPushButton(self.frame_52)
        self.file_4.setObjectName(u"file_4")
        self.file_4.setMinimumSize(QSize(28, 23))
        self.file_4.setMaximumSize(QSize(28, 23))
        self.file_4.setFont(font7)
        self.file_4.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.file_4.setIcon(icon10)
        self.file_4.setIconSize(QSize(24, 24))

        self.horizontalLayout_44.addWidget(self.file_4)

        self.link_uav4 = QPlainTextEdit(self.frame_52)
        self.link_uav4.setObjectName(u"link_uav4")
        self.link_uav4.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_44.addWidget(self.link_uav4)

        self.horizontalLayout_35.addWidget(self.frame_52)

        self.frame_53 = QFrame(self.frame_39)
        self.frame_53.setObjectName(u"frame_53")
        self.frame_53.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_53.setFrameShape(QFrame.StyledPanel)
        self.frame_53.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_43 = QHBoxLayout(self.frame_53)
        self.horizontalLayout_43.setSpacing(0)
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(0, 0, 9, 0)
        self.file_5 = QPushButton(self.frame_53)
        self.file_5.setObjectName(u"file_5")
        self.file_5.setMinimumSize(QSize(28, 23))
        self.file_5.setMaximumSize(QSize(28, 23))
        self.file_5.setFont(font7)
        self.file_5.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.file_5.setIcon(icon10)
        self.file_5.setIconSize(QSize(24, 24))

        self.horizontalLayout_43.addWidget(self.file_5)

        self.link_uav5 = QPlainTextEdit(self.frame_53)
        self.link_uav5.setObjectName(u"link_uav5")
        self.link_uav5.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_43.addWidget(self.link_uav5)

        self.horizontalLayout_35.addWidget(self.frame_53)

        self.frame_54 = QFrame(self.frame_39)
        self.frame_54.setObjectName(u"frame_54")
        self.frame_54.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_54.setFrameShape(QFrame.StyledPanel)
        self.frame_54.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_42 = QHBoxLayout(self.frame_54)
        self.horizontalLayout_42.setSpacing(0)
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.horizontalLayout_42.setContentsMargins(0, 0, 9, 0)
        self.file_6 = QPushButton(self.frame_54)
        self.file_6.setObjectName(u"file_6")
        self.file_6.setMinimumSize(QSize(28, 23))
        self.file_6.setMaximumSize(QSize(28, 23))
        self.file_6.setFont(font7)
        self.file_6.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.file_6.setIcon(icon10)
        self.file_6.setIconSize(QSize(24, 24))

        self.horizontalLayout_42.addWidget(self.file_6)

        self.link_uav6 = QPlainTextEdit(self.frame_54)
        self.link_uav6.setObjectName(u"link_uav6")
        self.link_uav6.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_42.addWidget(self.link_uav6)

        self.horizontalLayout_35.addWidget(self.frame_54)

        self.verticalLayout_15.addWidget(self.frame_39)

        self.frame_40 = QFrame(self.page_map)
        self.frame_40.setObjectName(u"frame_40")
        sizePolicy.setHeightForWidth(
            self.frame_40.sizePolicy().hasHeightForWidth())
        self.frame_40.setSizePolicy(sizePolicy)
        self.frame_40.setMinimumSize(QSize(0, 130))
        self.frame_40.setMaximumSize(QSize(16777215, 200))
        self.frame_40.setStyleSheet(u"background-color: rgb(85, 255, 127);")
        self.frame_40.setFrameShape(QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_34 = QHBoxLayout(self.frame_40)
        self.horizontalLayout_34.setSpacing(0)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.frame_55 = QFrame(self.frame_40)
        self.frame_55.setObjectName(u"frame_55")
        self.frame_55.setStyleSheet(u"background-color: rgb(118, 118, 118);")
        self.frame_55.setFrameShape(QFrame.StyledPanel)
        self.frame_55.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_85 = QHBoxLayout(self.frame_55)
        self.horizontalLayout_85.setObjectName(u"horizontalLayout_85")
        self.frame_148 = QFrame(self.frame_55)
        self.frame_148.setObjectName(u"frame_148")
        self.frame_148.setMinimumSize(QSize(25, 0))
        self.frame_148.setMaximumSize(QSize(25, 16777215))
        self.frame_148.setStyleSheet(u"background-color: rgb(83, 83, 83);")
        self.frame_148.setFrameShape(QFrame.StyledPanel)
        self.frame_148.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_148)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.Load_MS_1 = QPushButton(self.frame_148)
        self.Load_MS_1.setObjectName(u"Load_MS_1")
        self.Load_MS_1.setMinimumSize(QSize(0, 30))
        self.Load_MS_1.setMaximumSize(QSize(16777215, 30))
        self.Load_MS_1.setFont(font7)
        self.Load_MS_1.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")
        icon11 = QIcon()
        icon11.addFile(f"{icons_dir}/upload.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Load_MS_1.setIcon(icon11)
        self.Load_MS_1.setIconSize(QSize(24, 24))

        self.verticalLayout_16.addWidget(self.Load_MS_1)

        self.mission_uav1 = QPushButton(self.frame_148)
        self.mission_uav1.setObjectName(u"mission_uav1")
        self.mission_uav1.setMinimumSize(QSize(0, 30))
        self.mission_uav1.setMaximumSize(QSize(16777215, 30))
        self.mission_uav1.setFont(font7)
        self.mission_uav1.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-width: 2px;\n"
                                        "border-radius: 10px;")
        icon12 = QIcon()
        icon12.addFile(f"{icons_dir}/play.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.mission_uav1.setIcon(icon12)
        self.mission_uav1.setIconSize(QSize(24, 24))

        self.verticalLayout_16.addWidget(self.mission_uav1)

        self.pause_1 = QPushButton(self.frame_148)
        self.pause_1.setObjectName(u"pause_1")
        self.pause_1.setMinimumSize(QSize(0, 30))
        self.pause_1.setMaximumSize(QSize(16777215, 30))
        self.pause_1.setFont(font7)
        self.pause_1.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-width: 2px;\n"
                                   "border-radius: 10px;")
        icon13 = QIcon()
        icon13.addFile(f"{icons_dir}/pause.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pause_1.setIcon(icon13)
        self.pause_1.setIconSize(QSize(24, 24))

        self.verticalLayout_16.addWidget(self.pause_1)

        self.horizontalLayout_85.addWidget(self.frame_148)

        self.file_uav1 = QPlainTextEdit(self.frame_55)
        self.file_uav1.setObjectName(u"file_uav1")
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
# endif
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
# endif
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
# endif
        self.file_uav1.setPalette(palette1)
        self.file_uav1.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_85.addWidget(self.file_uav1)

        self.horizontalLayout_34.addWidget(self.frame_55)

        self.frame_56 = QFrame(self.frame_40)
        self.frame_56.setObjectName(u"frame_56")
        self.frame_56.setStyleSheet(u"background-color: rgb(118, 118, 118);")
        self.frame_56.setFrameShape(QFrame.StyledPanel)
        self.frame_56.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_90 = QHBoxLayout(self.frame_56)
        self.horizontalLayout_90.setObjectName(u"horizontalLayout_90")
        self.frame_149 = QFrame(self.frame_56)
        self.frame_149.setObjectName(u"frame_149")
        self.frame_149.setMinimumSize(QSize(25, 0))
        self.frame_149.setMaximumSize(QSize(25, 16777215))
        self.frame_149.setStyleSheet(u"background-color: rgb(83, 83, 83);")
        self.frame_149.setFrameShape(QFrame.StyledPanel)
        self.frame_149.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_149)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.Load_MS_2 = QPushButton(self.frame_149)
        self.Load_MS_2.setObjectName(u"Load_MS_2")
        self.Load_MS_2.setMinimumSize(QSize(0, 30))
        self.Load_MS_2.setMaximumSize(QSize(16777215, 30))
        self.Load_MS_2.setFont(font7)
        self.Load_MS_2.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")
        self.Load_MS_2.setIcon(icon11)
        self.Load_MS_2.setIconSize(QSize(24, 24))

        self.verticalLayout_17.addWidget(self.Load_MS_2)

        self.mission_uav2 = QPushButton(self.frame_149)
        self.mission_uav2.setObjectName(u"mission_uav2")
        self.mission_uav2.setMinimumSize(QSize(0, 30))
        self.mission_uav2.setMaximumSize(QSize(16777215, 30))
        self.mission_uav2.setFont(font7)
        self.mission_uav2.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-width: 2px;\n"
                                        "border-radius: 10px;")
        self.mission_uav2.setIcon(icon12)
        self.mission_uav2.setIconSize(QSize(24, 24))

        self.verticalLayout_17.addWidget(self.mission_uav2)

        self.pause_2 = QPushButton(self.frame_149)
        self.pause_2.setObjectName(u"pause_2")
        self.pause_2.setMinimumSize(QSize(0, 30))
        self.pause_2.setMaximumSize(QSize(16777215, 30))
        self.pause_2.setFont(font7)
        self.pause_2.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-width: 2px;\n"
                                   "border-radius: 10px;")
        self.pause_2.setIcon(icon13)
        self.pause_2.setIconSize(QSize(24, 24))

        self.verticalLayout_17.addWidget(self.pause_2)

        self.horizontalLayout_90.addWidget(self.frame_149)

        self.file_uav2 = QPlainTextEdit(self.frame_56)
        self.file_uav2.setObjectName(u"file_uav2")
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette2.setBrush(QPalette.Active, QPalette.Text, brush)
        palette2.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
# endif
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
# endif
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
# endif
        self.file_uav2.setPalette(palette2)
        self.file_uav2.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_90.addWidget(self.file_uav2)

        self.horizontalLayout_34.addWidget(self.frame_56)

        self.frame_57 = QFrame(self.frame_40)
        self.frame_57.setObjectName(u"frame_57")
        self.frame_57.setStyleSheet(u"background-color: rgb(118, 118, 118);")
        self.frame_57.setFrameShape(QFrame.StyledPanel)
        self.frame_57.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_89 = QHBoxLayout(self.frame_57)
        self.horizontalLayout_89.setObjectName(u"horizontalLayout_89")
        self.frame_150 = QFrame(self.frame_57)
        self.frame_150.setObjectName(u"frame_150")
        self.frame_150.setMinimumSize(QSize(25, 0))
        self.frame_150.setMaximumSize(QSize(25, 16777215))
        self.frame_150.setStyleSheet(u"background-color: rgb(83, 83, 83);")
        self.frame_150.setFrameShape(QFrame.StyledPanel)
        self.frame_150.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_150)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.Load_MS_3 = QPushButton(self.frame_150)
        self.Load_MS_3.setObjectName(u"Load_MS_3")
        self.Load_MS_3.setMinimumSize(QSize(0, 30))
        self.Load_MS_3.setMaximumSize(QSize(16777215, 30))
        font9 = QFont()
        font9.setPointSize(13)
        font9.setBold(True)
        font9.setItalic(True)
        font9.setUnderline(False)
        font9.setWeight(75)
        self.Load_MS_3.setFont(font9)
        self.Load_MS_3.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")
        self.Load_MS_3.setIcon(icon11)
        self.Load_MS_3.setIconSize(QSize(24, 24))

        self.verticalLayout_18.addWidget(self.Load_MS_3)

        self.mission_uav3 = QPushButton(self.frame_150)
        self.mission_uav3.setObjectName(u"mission_uav3")
        self.mission_uav3.setMinimumSize(QSize(0, 30))
        self.mission_uav3.setMaximumSize(QSize(16777215, 30))
        self.mission_uav3.setFont(font7)
        self.mission_uav3.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-width: 2px;\n"
                                        "border-radius: 10px;")
        self.mission_uav3.setIcon(icon12)
        self.mission_uav3.setIconSize(QSize(24, 24))

        self.verticalLayout_18.addWidget(self.mission_uav3)

        self.pause_3 = QPushButton(self.frame_150)
        self.pause_3.setObjectName(u"pause_3")
        self.pause_3.setMinimumSize(QSize(0, 30))
        self.pause_3.setMaximumSize(QSize(16777215, 30))
        self.pause_3.setFont(font7)
        self.pause_3.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-width: 2px;\n"
                                   "border-radius: 10px;")
        self.pause_3.setIcon(icon13)
        self.pause_3.setIconSize(QSize(24, 24))

        self.verticalLayout_18.addWidget(self.pause_3)

        self.horizontalLayout_89.addWidget(self.frame_150)

        self.file_uav3 = QPlainTextEdit(self.frame_57)
        self.file_uav3.setObjectName(u"file_uav3")
        palette3 = QPalette()
        palette3.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette3.setBrush(QPalette.Active, QPalette.Text, brush)
        palette3.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Active, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
# endif
        palette3.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette3.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
# endif
        palette3.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette3.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
# endif
        self.file_uav3.setPalette(palette3)
        self.file_uav3.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_89.addWidget(self.file_uav3)

        self.horizontalLayout_34.addWidget(self.frame_57)

        self.frame_58 = QFrame(self.frame_40)
        self.frame_58.setObjectName(u"frame_58")
        self.frame_58.setStyleSheet(u"background-color: rgb(118, 118, 118);")
        self.frame_58.setFrameShape(QFrame.StyledPanel)
        self.frame_58.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_88 = QHBoxLayout(self.frame_58)
        self.horizontalLayout_88.setObjectName(u"horizontalLayout_88")
        self.frame_151 = QFrame(self.frame_58)
        self.frame_151.setObjectName(u"frame_151")
        self.frame_151.setMinimumSize(QSize(25, 0))
        self.frame_151.setMaximumSize(QSize(25, 16777215))
        self.frame_151.setStyleSheet(u"background-color: rgb(83, 83, 83);")
        self.frame_151.setFrameShape(QFrame.StyledPanel)
        self.frame_151.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.frame_151)
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.Load_MS_4 = QPushButton(self.frame_151)
        self.Load_MS_4.setObjectName(u"Load_MS_4")
        self.Load_MS_4.setMinimumSize(QSize(0, 30))
        self.Load_MS_4.setMaximumSize(QSize(16777215, 30))
        self.Load_MS_4.setFont(font7)
        self.Load_MS_4.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")
        self.Load_MS_4.setIcon(icon11)
        self.Load_MS_4.setIconSize(QSize(24, 24))

        self.verticalLayout_19.addWidget(self.Load_MS_4)

        self.mission_uav4 = QPushButton(self.frame_151)
        self.mission_uav4.setObjectName(u"mission_uav4")
        self.mission_uav4.setMinimumSize(QSize(0, 30))
        self.mission_uav4.setMaximumSize(QSize(16777215, 30))
        self.mission_uav4.setFont(font7)
        self.mission_uav4.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-width: 2px;\n"
                                        "border-radius: 10px;")
        self.mission_uav4.setIcon(icon12)
        self.mission_uav4.setIconSize(QSize(24, 24))

        self.verticalLayout_19.addWidget(self.mission_uav4)

        self.pause_4 = QPushButton(self.frame_151)
        self.pause_4.setObjectName(u"pause_4")
        self.pause_4.setMinimumSize(QSize(0, 30))
        self.pause_4.setMaximumSize(QSize(16777215, 30))
        self.pause_4.setFont(font7)
        self.pause_4.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-width: 2px;\n"
                                   "border-radius: 10px;")
        self.pause_4.setIcon(icon13)
        self.pause_4.setIconSize(QSize(24, 24))

        self.verticalLayout_19.addWidget(self.pause_4)

        self.horizontalLayout_88.addWidget(self.frame_151)

        self.file_uav4 = QPlainTextEdit(self.frame_58)
        self.file_uav4.setObjectName(u"file_uav4")
        palette4 = QPalette()
        palette4.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette4.setBrush(QPalette.Active, QPalette.Text, brush)
        palette4.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette4.setBrush(QPalette.Active, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
# endif
        palette4.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette4.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette4.setBrush(QPalette.Inactive, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
# endif
        palette4.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette4.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette4.setBrush(QPalette.Disabled, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
# endif
        self.file_uav4.setPalette(palette4)
        self.file_uav4.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_88.addWidget(self.file_uav4)

        self.horizontalLayout_34.addWidget(self.frame_58)

        self.frame_59 = QFrame(self.frame_40)
        self.frame_59.setObjectName(u"frame_59")
        self.frame_59.setStyleSheet(u"background-color: rgb(118, 118, 118);")
        self.frame_59.setFrameShape(QFrame.StyledPanel)
        self.frame_59.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_87 = QHBoxLayout(self.frame_59)
        self.horizontalLayout_87.setObjectName(u"horizontalLayout_87")
        self.frame_152 = QFrame(self.frame_59)
        self.frame_152.setObjectName(u"frame_152")
        self.frame_152.setMinimumSize(QSize(25, 0))
        self.frame_152.setMaximumSize(QSize(25, 16777215))
        self.frame_152.setStyleSheet(u"background-color: rgb(83, 83, 83);")
        self.frame_152.setFrameShape(QFrame.StyledPanel)
        self.frame_152.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame_152)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.Load_MS_5 = QPushButton(self.frame_152)
        self.Load_MS_5.setObjectName(u"Load_MS_5")
        self.Load_MS_5.setMinimumSize(QSize(0, 30))
        self.Load_MS_5.setMaximumSize(QSize(16777215, 30))
        self.Load_MS_5.setFont(font7)
        self.Load_MS_5.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")
        self.Load_MS_5.setIcon(icon11)
        self.Load_MS_5.setIconSize(QSize(24, 24))

        self.verticalLayout_20.addWidget(self.Load_MS_5)

        self.mission_uav5 = QPushButton(self.frame_152)
        self.mission_uav5.setObjectName(u"mission_uav5")
        self.mission_uav5.setMinimumSize(QSize(0, 30))
        self.mission_uav5.setMaximumSize(QSize(16777215, 30))
        self.mission_uav5.setFont(font7)
        self.mission_uav5.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-width: 2px;\n"
                                        "border-radius: 10px;")
        self.mission_uav5.setIcon(icon12)
        self.mission_uav5.setIconSize(QSize(24, 24))

        self.verticalLayout_20.addWidget(self.mission_uav5)

        self.pause_5 = QPushButton(self.frame_152)
        self.pause_5.setObjectName(u"pause_5")
        self.pause_5.setMinimumSize(QSize(0, 30))
        self.pause_5.setMaximumSize(QSize(16777215, 30))
        self.pause_5.setFont(font7)
        self.pause_5.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-width: 2px;\n"
                                   "border-radius: 10px;")
        self.pause_5.setIcon(icon13)
        self.pause_5.setIconSize(QSize(24, 24))

        self.verticalLayout_20.addWidget(self.pause_5)

        self.horizontalLayout_87.addWidget(self.frame_152)

        self.file_uav5 = QPlainTextEdit(self.frame_59)
        self.file_uav5.setObjectName(u"file_uav5")
        palette5 = QPalette()
        palette5.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette5.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette5.setBrush(QPalette.Active, QPalette.Text, brush)
        palette5.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette5.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette5.setBrush(QPalette.Active, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
# endif
        palette5.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette5.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette5.setBrush(QPalette.Inactive, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
# endif
        palette5.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette5.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette5.setBrush(QPalette.Disabled, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
# endif
        self.file_uav5.setPalette(palette5)
        self.file_uav5.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_87.addWidget(self.file_uav5)

        self.horizontalLayout_34.addWidget(self.frame_59)

        self.frame_60 = QFrame(self.frame_40)
        self.frame_60.setObjectName(u"frame_60")
        self.frame_60.setStyleSheet(u"background-color: rgb(118, 118, 118);")
        self.frame_60.setFrameShape(QFrame.StyledPanel)
        self.frame_60.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_86 = QHBoxLayout(self.frame_60)
        self.horizontalLayout_86.setObjectName(u"horizontalLayout_86")
        self.frame_153 = QFrame(self.frame_60)
        self.frame_153.setObjectName(u"frame_153")
        self.frame_153.setMinimumSize(QSize(25, 0))
        self.frame_153.setMaximumSize(QSize(25, 16777215))
        self.frame_153.setStyleSheet(u"background-color: rgb(83, 83, 83);")
        self.frame_153.setFrameShape(QFrame.StyledPanel)
        self.frame_153.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_153)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.Load_MS_6 = QPushButton(self.frame_153)
        self.Load_MS_6.setObjectName(u"Load_MS_6")
        self.Load_MS_6.setMinimumSize(QSize(0, 30))
        self.Load_MS_6.setMaximumSize(QSize(16777215, 30))
        self.Load_MS_6.setFont(font7)
        self.Load_MS_6.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")
        self.Load_MS_6.setIcon(icon11)
        self.Load_MS_6.setIconSize(QSize(24, 24))

        self.verticalLayout_21.addWidget(self.Load_MS_6)

        self.mission_uav6 = QPushButton(self.frame_153)
        self.mission_uav6.setObjectName(u"mission_uav6")
        self.mission_uav6.setMinimumSize(QSize(0, 30))
        self.mission_uav6.setMaximumSize(QSize(16777215, 30))
        self.mission_uav6.setFont(font7)
        self.mission_uav6.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-width: 2px;\n"
                                        "border-radius: 10px;")
        self.mission_uav6.setIcon(icon12)
        self.mission_uav6.setIconSize(QSize(24, 24))

        self.verticalLayout_21.addWidget(self.mission_uav6)

        self.pause_6 = QPushButton(self.frame_153)
        self.pause_6.setObjectName(u"pause_6")
        self.pause_6.setMinimumSize(QSize(0, 30))
        self.pause_6.setMaximumSize(QSize(16777215, 30))
        self.pause_6.setFont(font7)
        self.pause_6.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-width: 2px;\n"
                                   "border-radius: 10px;")
        self.pause_6.setIcon(icon13)
        self.pause_6.setIconSize(QSize(24, 24))

        self.verticalLayout_21.addWidget(self.pause_6)

        self.horizontalLayout_86.addWidget(self.frame_153)

        self.file_uav6 = QPlainTextEdit(self.frame_60)
        self.file_uav6.setObjectName(u"file_uav6")
        palette6 = QPalette()
        palette6.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette6.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette6.setBrush(QPalette.Active, QPalette.Text, brush)
        palette6.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette6.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette6.setBrush(QPalette.Active, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette6.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
# endif
        palette6.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette6.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette6.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette6.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette6.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette6.setBrush(QPalette.Inactive, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette6.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
# endif
        palette6.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette6.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette6.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette6.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette6.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette6.setBrush(QPalette.Disabled, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette6.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
# endif
        self.file_uav6.setPalette(palette6)
        self.file_uav6.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_86.addWidget(self.file_uav6)

        self.horizontalLayout_34.addWidget(self.frame_60)

        self.verticalLayout_15.addWidget(self.frame_40)

        self.frame_42 = QFrame(self.page_map)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setFrameShape(QFrame.StyledPanel)
        self.frame_42.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_54 = QHBoxLayout(self.frame_42)
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.frame_141 = QFrame(self.frame_42)
        self.frame_141.setObjectName(u"frame_141")
        self.frame_141.setMinimumSize(QSize(800, 0))
        self.frame_141.setMaximumSize(QSize(800, 16777215))
        self.frame_141.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_141.setFrameShape(QFrame.StyledPanel)
        self.frame_141.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_78 = QHBoxLayout(self.frame_141)
        self.horizontalLayout_78.setObjectName(u"horizontalLayout_78")
        self.frame_70 = QFrame(self.frame_141)
        self.frame_70.setObjectName(u"frame_70")
        self.frame_70.setMinimumSize(QSize(280, 140))
        self.frame_70.setMaximumSize(QSize(280, 180))
        self.frame_70.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_70.setFrameShape(QFrame.StyledPanel)
        self.frame_70.setFrameShadow(QFrame.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_70)
        self.verticalLayout_22.setSpacing(6)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 3, 0, 0)
        self.file_all = QPushButton(self.frame_70)
        self.file_all.setObjectName(u"file_all")
        self.file_all.setMinimumSize(QSize(0, 30))
        self.file_all.setMaximumSize(QSize(16777215, 30))
        self.file_all.setFont(font7)
        self.file_all.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                    "border-width: 2px;\n"
                                    "color: rgb(255, 0, 0);\n"
                                    "border-radius: 10px;")

        self.verticalLayout_22.addWidget(self.file_all)

        self.frame_68 = QFrame(self.frame_70)
        self.frame_68.setObjectName(u"frame_68")
        self.frame_68.setMinimumSize(QSize(0, 30))
        self.frame_68.setMaximumSize(QSize(16777215, 30))
        self.frame_68.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.frame_68.setFrameShape(QFrame.StyledPanel)
        self.frame_68.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_55 = QHBoxLayout(self.frame_68)
        self.horizontalLayout_55.setSpacing(0)
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.horizontalLayout_55.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.frame_68)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setIcon(icon10)
        self.pushButton_2.setIconSize(QSize(24, 24))

        self.horizontalLayout_55.addWidget(self.pushButton_2)

        self.link_all_uav = QPlainTextEdit(self.frame_68)
        self.link_all_uav.setObjectName(u"link_all_uav")
        self.link_all_uav.setMinimumSize(QSize(0, 23))
        self.link_all_uav.setMaximumSize(QSize(16777215, 23))
        self.link_all_uav.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                        "color: rgb(0, 0, 0);\n"
                                        "border-width: 2px;\n"
                                        "border-radius: 10px;")

        self.horizontalLayout_55.addWidget(self.link_all_uav)

        self.verticalLayout_22.addWidget(self.frame_68)

        self.Load_MS_all = QPushButton(self.frame_70)
        self.Load_MS_all.setObjectName(u"Load_MS_all")
        self.Load_MS_all.setMinimumSize(QSize(0, 30))
        self.Load_MS_all.setMaximumSize(QSize(16777215, 30))
        self.Load_MS_all.setFont(font7)
        self.Load_MS_all.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "border-width: 2px;\n"
                                       "border-radius: 10px;")

        self.verticalLayout_22.addWidget(self.Load_MS_all)

        self.frame_133 = QFrame(self.frame_70)
        self.frame_133.setObjectName(u"frame_133")
        self.frame_133.setFrameShape(QFrame.StyledPanel)
        self.frame_133.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_70 = QHBoxLayout(self.frame_133)
        self.horizontalLayout_70.setSpacing(0)
        self.horizontalLayout_70.setObjectName(u"horizontalLayout_70")
        self.horizontalLayout_70.setContentsMargins(0, 0, 0, 0)
        self.mission_all_2 = QPushButton(self.frame_133)
        self.mission_all_2.setObjectName(u"mission_all_2")
        self.mission_all_2.setMinimumSize(QSize(0, 30))
        self.mission_all_2.setMaximumSize(QSize(16777215, 30))
        self.mission_all_2.setFont(font7)
        self.mission_all_2.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "border-width: 2px;\n"
                                         "border-radius: 10px;")

        self.horizontalLayout_70.addWidget(self.mission_all_2)

        self.pause_all = QPushButton(self.frame_133)
        self.pause_all.setObjectName(u"pause_all")
        self.pause_all.setMinimumSize(QSize(0, 30))
        self.pause_all.setMaximumSize(QSize(16777215, 30))
        self.pause_all.setFont(font7)
        self.pause_all.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px;")

        self.horizontalLayout_70.addWidget(self.pause_all)

        self.verticalLayout_22.addWidget(self.frame_133)

        self.frame_121 = QFrame(self.frame_70)
        self.frame_121.setObjectName(u"frame_121")
        self.frame_121.setFrameShape(QFrame.StyledPanel)
        self.frame_121.setFrameShadow(QFrame.Raised)

        self.verticalLayout_22.addWidget(self.frame_121)

        self.horizontalLayout_78.addWidget(self.frame_70)

        self.frame_69 = QFrame(self.frame_141)
        self.frame_69.setObjectName(u"frame_69")
        self.frame_69.setMinimumSize(QSize(500, 0))
        self.frame_69.setMaximumSize(QSize(500, 16777215))
        self.frame_69.setStyleSheet(u"background-color: rgb(118,118,118);")
        self.frame_69.setFrameShape(QFrame.StyledPanel)
        self.frame_69.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_56 = QHBoxLayout(self.frame_69)
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.file_all_uav = QPlainTextEdit(self.frame_69)
        self.file_all_uav.setObjectName(u"file_all_uav")
        self.file_all_uav.setStyleSheet(u"border-width: 2px;\n"
                                        "border-radius: 10px;background-color: rgb(0, 0, 0);\n"
                                        "color: rgb(255, 255, 255);")

        self.horizontalLayout_56.addWidget(self.file_all_uav)

        self.btn_map_all = QPushButton(self.frame_69)
        self.btn_map_all.setObjectName(u"btn_map_all")
        self.btn_map_all.setMinimumSize(QSize(0, 280))
        self.btn_map_all.setMaximumSize(QSize(16777215, 280))
        self.btn_map_all.setFont(font7)
        self.btn_map_all.setStyleSheet(u"background-color: rgb(118, 118, 118);\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "border-width: 2px;\n"
                                       "border-radius: 10px;")

        self.horizontalLayout_56.addWidget(self.btn_map_all)

        self.horizontalLayout_78.addWidget(self.frame_69)

        self.horizontalLayout_54.addWidget(self.frame_141)

        self.frame_140 = QFrame(self.frame_42)
        self.frame_140.setObjectName(u"frame_140")
        self.frame_140.setMinimumSize(QSize(500, 0))
        self.frame_140.setMaximumSize(QSize(16777215, 16777215))
        self.frame_140.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_140.setFrameShape(QFrame.StyledPanel)
        self.frame_140.setFrameShadow(QFrame.Raised)
        self.latitude = QPlainTextEdit(self.frame_140)
        self.latitude.setObjectName(u"latitude")
        self.latitude.setGeometry(QRect(490, 20, 256, 31))
        self.latitude.setStyleSheet(u"background-color: rgb(255, 255, 255);border-width: 2px;\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "border-radius: 10px;")
        self.longtitude = QPlainTextEdit(self.frame_140)
        self.longtitude.setObjectName(u"longtitude")
        self.longtitude.setGeometry(QRect(90, 20, 256, 31))
        self.longtitude.setStyleSheet(u"color: rgb(0, 0, 0);\n"
                                      "border-width: 2px;\n"
                                      "border-radius: 10px;background-color: rgb(255, 255, 255);")
        self.label_22 = QLabel(self.frame_140)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(370, 20, 121, 41))
        self.label_22.setFont(font7)
        self.label_22.setStyleSheet(u"color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(0, 0, 0);")
        self.label_16 = QLabel(self.frame_140)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(0, 20, 91, 41))
        self.label_16.setFont(font7)
        self.label_16.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
                                    "color: rgb(255, 255, 255);")
        self.horizontalLayoutWidget = QWidget(self.frame_140)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(90, 80, 631, 71))
        self.horizontalLayout_77 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_77.setObjectName(u"horizontalLayout_77")
        self.horizontalLayout_77.setContentsMargins(0, 0, 0, 0)
        self.goto_1 = QPushButton(self.horizontalLayoutWidget)
        self.goto_1.setObjectName(u"goto_1")
        self.goto_1.setMinimumSize(QSize(0, 30))
        self.goto_1.setMaximumSize(QSize(16777215, 30))
        palette7 = QPalette()
        palette7.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        brush2 = QBrush(QColor(118, 118, 118, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette7.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette7.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette7.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette7.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette7.setBrush(QPalette.Active, QPalette.Window, brush2)
        brush3 = QBrush(QColor(255, 255, 127, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette7.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush4 = QBrush(QColor(0, 0, 0, 128))
        brush4.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette7.setBrush(QPalette.Active, QPalette.PlaceholderText, brush4)
# endif
        palette7.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette7.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette7.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette7.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette7.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette7.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette7.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush5 = QBrush(QColor(0, 0, 0, 128))
        brush5.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette7.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush5)
# endif
        palette7.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette7.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette7.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette7.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette7.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette7.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette7.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush6 = QBrush(QColor(0, 0, 0, 128))
        brush6.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette7.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush6)
# endif
        self.goto_1.setPalette(palette7)
        font10 = QFont()
        font10.setFamily(u".VnArial")
        font10.setPointSize(12)
        font10.setBold(True)
        font10.setItalic(True)
        font10.setWeight(75)
        self.goto_1.setFont(font10)
        self.goto_1.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.goto_1.setAutoDefault(False)

        self.horizontalLayout_77.addWidget(self.goto_1)

        self.goto_2 = QPushButton(self.horizontalLayoutWidget)
        self.goto_2.setObjectName(u"goto_2")
        self.goto_2.setMinimumSize(QSize(0, 30))
        self.goto_2.setMaximumSize(QSize(16777215, 30))
        palette8 = QPalette()
        palette8.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette8.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette8.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette8.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette8.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette8.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette8.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush7 = QBrush(QColor(0, 0, 0, 128))
        brush7.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Active, QPalette.PlaceholderText, brush7)
# endif
        palette8.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette8.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette8.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette8.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette8.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette8.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette8.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush8 = QBrush(QColor(0, 0, 0, 128))
        brush8.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush8)
# endif
        palette8.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette8.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette8.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette8.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette8.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette8.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette8.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush9 = QBrush(QColor(0, 0, 0, 128))
        brush9.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush9)
# endif
        self.goto_2.setPalette(palette8)
        self.goto_2.setFont(font10)
        self.goto_2.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.goto_2.setAutoDefault(False)

        self.horizontalLayout_77.addWidget(self.goto_2)

        self.goto_3 = QPushButton(self.horizontalLayoutWidget)
        self.goto_3.setObjectName(u"goto_3")
        self.goto_3.setMinimumSize(QSize(0, 30))
        self.goto_3.setMaximumSize(QSize(16777215, 30))
        palette9 = QPalette()
        palette9.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette9.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette9.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette9.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette9.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette9.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette9.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush10 = QBrush(QColor(0, 0, 0, 128))
        brush10.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Active, QPalette.PlaceholderText, brush10)
# endif
        palette9.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette9.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette9.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette9.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette9.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette9.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette9.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush11 = QBrush(QColor(0, 0, 0, 128))
        brush11.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush11)
# endif
        palette9.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette9.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette9.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette9.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette9.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette9.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette9.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush12 = QBrush(QColor(0, 0, 0, 128))
        brush12.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush12)
# endif
        self.goto_3.setPalette(palette9)
        self.goto_3.setFont(font10)
        self.goto_3.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.goto_3.setAutoDefault(False)

        self.horizontalLayout_77.addWidget(self.goto_3)

        self.goto_4 = QPushButton(self.horizontalLayoutWidget)
        self.goto_4.setObjectName(u"goto_4")
        self.goto_4.setMinimumSize(QSize(0, 30))
        self.goto_4.setMaximumSize(QSize(16777215, 30))
        palette10 = QPalette()
        palette10.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette10.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette10.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette10.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette10.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette10.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette10.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush13 = QBrush(QColor(0, 0, 0, 128))
        brush13.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette10.setBrush(QPalette.Active, QPalette.PlaceholderText, brush13)
# endif
        palette10.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette10.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette10.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette10.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette10.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette10.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette10.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush14 = QBrush(QColor(0, 0, 0, 128))
        brush14.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette10.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush14)
# endif
        palette10.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette10.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette10.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette10.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette10.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette10.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette10.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush15 = QBrush(QColor(0, 0, 0, 128))
        brush15.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette10.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush15)
# endif
        self.goto_4.setPalette(palette10)
        self.goto_4.setFont(font10)
        self.goto_4.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.goto_4.setAutoDefault(False)

        self.horizontalLayout_77.addWidget(self.goto_4)

        self.goto_5 = QPushButton(self.horizontalLayoutWidget)
        self.goto_5.setObjectName(u"goto_5")
        self.goto_5.setMinimumSize(QSize(0, 30))
        self.goto_5.setMaximumSize(QSize(16777215, 30))
        palette11 = QPalette()
        palette11.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette11.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette11.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette11.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette11.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette11.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette11.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush16 = QBrush(QColor(0, 0, 0, 128))
        brush16.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette11.setBrush(QPalette.Active, QPalette.PlaceholderText, brush16)
# endif
        palette11.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette11.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette11.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette11.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette11.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette11.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette11.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush17 = QBrush(QColor(0, 0, 0, 128))
        brush17.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette11.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush17)
# endif
        palette11.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette11.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette11.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette11.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette11.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette11.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette11.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush18 = QBrush(QColor(0, 0, 0, 128))
        brush18.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette11.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush18)
# endif
        self.goto_5.setPalette(palette11)
        self.goto_5.setFont(font10)
        self.goto_5.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.goto_5.setAutoDefault(False)

        self.horizontalLayout_77.addWidget(self.goto_5)

        self.goto_6 = QPushButton(self.horizontalLayoutWidget)
        self.goto_6.setObjectName(u"goto_6")
        self.goto_6.setMinimumSize(QSize(0, 30))
        self.goto_6.setMaximumSize(QSize(16777215, 30))
        palette12 = QPalette()
        palette12.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette12.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette12.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette12.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette12.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette12.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette12.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush19 = QBrush(QColor(0, 0, 0, 128))
        brush19.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette12.setBrush(QPalette.Active, QPalette.PlaceholderText, brush19)
# endif
        palette12.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette12.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette12.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette12.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette12.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette12.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette12.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush20 = QBrush(QColor(0, 0, 0, 128))
        brush20.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette12.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush20)
# endif
        palette12.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette12.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette12.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette12.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette12.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette12.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette12.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush21 = QBrush(QColor(0, 0, 0, 128))
        brush21.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette12.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush21)
# endif
        self.goto_6.setPalette(palette12)
        self.goto_6.setFont(font10)
        self.goto_6.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.goto_6.setAutoDefault(False)

        self.horizontalLayout_77.addWidget(self.goto_6)

        self.goto_all = QPushButton(self.horizontalLayoutWidget)
        self.goto_all.setObjectName(u"goto_all")
        self.goto_all.setMinimumSize(QSize(0, 30))
        self.goto_all.setMaximumSize(QSize(16777215, 30))
        palette13 = QPalette()
        palette13.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        brush22 = QBrush(QColor(170, 0, 0, 255))
        brush22.setStyle(Qt.SolidPattern)
        palette13.setBrush(QPalette.Active, QPalette.Button, brush22)
        palette13.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette13.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette13.setBrush(QPalette.Active, QPalette.Base, brush22)
        palette13.setBrush(QPalette.Active, QPalette.Window, brush22)
        palette13.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush23 = QBrush(QColor(0, 0, 0, 128))
        brush23.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette13.setBrush(QPalette.Active, QPalette.PlaceholderText, brush23)
# endif
        palette13.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette13.setBrush(QPalette.Inactive, QPalette.Button, brush22)
        palette13.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette13.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette13.setBrush(QPalette.Inactive, QPalette.Base, brush22)
        palette13.setBrush(QPalette.Inactive, QPalette.Window, brush22)
        palette13.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush24 = QBrush(QColor(0, 0, 0, 128))
        brush24.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette13.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush24)
# endif
        palette13.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette13.setBrush(QPalette.Disabled, QPalette.Button, brush22)
        palette13.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette13.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette13.setBrush(QPalette.Disabled, QPalette.Base, brush22)
        palette13.setBrush(QPalette.Disabled, QPalette.Window, brush22)
        palette13.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush25 = QBrush(QColor(0, 0, 0, 128))
        brush25.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette13.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush25)
# endif
        self.goto_all.setPalette(palette13)
        self.goto_all.setFont(font10)
        self.goto_all.setStyleSheet(u"background-color: rgb(170, 0, 0);")
        self.goto_all.setAutoDefault(False)

        self.horizontalLayout_77.addWidget(self.goto_all)

        self.label_28 = QLabel(self.frame_140)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(10, 100, 71, 31))
        self.label_28.setFont(font7)
        self.label_28.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
                                    "color: rgb(255, 255, 255);")

        self.horizontalLayout_54.addWidget(self.frame_140)

        self.verticalLayout_15.addWidget(self.frame_42)

        self.stackedWidget.addWidget(self.page_map)
        self.page_connect = QWidget()
        self.page_connect.setObjectName(u"page_connect")
        self.horizontalLayout_10 = QHBoxLayout(self.page_connect)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.frame_10 = QFrame(self.page_connect)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(0, 300))
        self.frame_10.setMaximumSize(QSize(150, 400))
        self.frame_10.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_10)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.connect_all = QPushButton(self.frame_10)
        self.connect_all.setObjectName(u"connect_all")
        self.connect_all.setMinimumSize(QSize(0, 35))
        self.connect_all.setMaximumSize(QSize(16777215, 35))
        palette14 = QPalette()
        palette14.setBrush(QPalette.Active, QPalette.Button, brush2)
        brush26 = QBrush(QColor(255, 0, 0, 255))
        brush26.setStyle(Qt.SolidPattern)
        palette14.setBrush(QPalette.Active, QPalette.ButtonText, brush26)
        palette14.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette14.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette14.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette14.setBrush(QPalette.Inactive, QPalette.ButtonText, brush26)
        palette14.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette14.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette14.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        brush27 = QBrush(QColor(190, 190, 190, 255))
        brush27.setStyle(Qt.SolidPattern)
        palette14.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette14.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette14.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.connect_all.setPalette(palette14)
        font11 = QFont()
        font11.setPointSize(12)
        font11.setItalic(True)
        self.connect_all.setFont(font11)
        self.connect_all.setStyleSheet(u"background:rgb(118, 118, 118)")

        self.verticalLayout_7.addWidget(self.connect_all)

        self.arm_all = QPushButton(self.frame_10)
        self.arm_all.setObjectName(u"arm_all")
        self.arm_all.setMinimumSize(QSize(0, 35))
        self.arm_all.setMaximumSize(QSize(16777215, 35))
        palette15 = QPalette()
        palette15.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette15.setBrush(QPalette.Active, QPalette.ButtonText, brush26)
        palette15.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette15.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette15.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette15.setBrush(QPalette.Inactive, QPalette.ButtonText, brush26)
        palette15.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette15.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette15.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette15.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette15.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette15.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.arm_all.setPalette(palette15)
        font12 = QFont()
        font12.setPointSize(11)
        font12.setItalic(True)
        self.arm_all.setFont(font12)
        self.arm_all.setStyleSheet(u"background:rgb(118, 118, 118)")

        self.verticalLayout_7.addWidget(self.arm_all)

        self.take_off_all = QPushButton(self.frame_10)
        self.take_off_all.setObjectName(u"take_off_all")
        self.take_off_all.setMinimumSize(QSize(0, 35))
        self.take_off_all.setMaximumSize(QSize(16777215, 35))
        palette16 = QPalette()
        palette16.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette16.setBrush(QPalette.Active, QPalette.ButtonText, brush26)
        palette16.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette16.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette16.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette16.setBrush(QPalette.Inactive, QPalette.ButtonText, brush26)
        palette16.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette16.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette16.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette16.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette16.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette16.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.take_off_all.setPalette(palette16)
        self.take_off_all.setFont(font11)
        self.take_off_all.setStyleSheet(u"background:rgb(118, 118, 118)")

        self.verticalLayout_7.addWidget(self.take_off_all)

        self.land_all = QPushButton(self.frame_10)
        self.land_all.setObjectName(u"land_all")
        self.land_all.setMinimumSize(QSize(0, 35))
        self.land_all.setMaximumSize(QSize(16777215, 35))
        palette17 = QPalette()
        palette17.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette17.setBrush(QPalette.Active, QPalette.ButtonText, brush26)
        palette17.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette17.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette17.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette17.setBrush(QPalette.Inactive, QPalette.ButtonText, brush26)
        palette17.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette17.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette17.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette17.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette17.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette17.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.land_all.setPalette(palette17)
        self.land_all.setFont(font11)
        self.land_all.setStyleSheet(u"background:rgb(118, 118, 118)")

        self.verticalLayout_7.addWidget(self.land_all)

        self.RTL_all_2 = QPushButton(self.frame_10)
        self.RTL_all_2.setObjectName(u"RTL_all_2")
        self.RTL_all_2.setMinimumSize(QSize(0, 35))
        self.RTL_all_2.setMaximumSize(QSize(16777215, 35))
        palette18 = QPalette()
        palette18.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette18.setBrush(QPalette.Active, QPalette.ButtonText, brush26)
        palette18.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette18.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette18.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette18.setBrush(QPalette.Inactive, QPalette.ButtonText, brush26)
        palette18.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette18.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette18.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette18.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette18.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette18.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.RTL_all_2.setPalette(palette18)
        self.RTL_all_2.setFont(font11)
        self.RTL_all_2.setStyleSheet(u"background:rgb(118, 118, 118)")

        self.verticalLayout_7.addWidget(self.RTL_all_2)

        self.mission_all = QPushButton(self.frame_10)
        self.mission_all.setObjectName(u"mission_all")
        self.mission_all.setMinimumSize(QSize(0, 35))
        self.mission_all.setMaximumSize(QSize(16777215, 35))
        palette19 = QPalette()
        palette19.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette19.setBrush(QPalette.Active, QPalette.ButtonText, brush26)
        palette19.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette19.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette19.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette19.setBrush(QPalette.Inactive, QPalette.ButtonText, brush26)
        palette19.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette19.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette19.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette19.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette19.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette19.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.mission_all.setPalette(palette19)
        self.mission_all.setFont(font11)
        self.mission_all.setStyleSheet(u"background:rgb(118, 118, 118)")

        self.verticalLayout_7.addWidget(self.mission_all)

        self.pause_all_2 = QPushButton(self.frame_10)
        self.pause_all_2.setObjectName(u"pause_all_2")
        self.pause_all_2.setMinimumSize(QSize(0, 35))
        self.pause_all_2.setMaximumSize(QSize(16777215, 35))
        palette20 = QPalette()
        palette20.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette20.setBrush(QPalette.Active, QPalette.ButtonText, brush26)
        palette20.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette20.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette20.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette20.setBrush(QPalette.Inactive, QPalette.ButtonText, brush26)
        palette20.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette20.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette20.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette20.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette20.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette20.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.pause_all_2.setPalette(palette20)
        self.pause_all_2.setFont(font11)
        self.pause_all_2.setStyleSheet(
            u"background-color: rgb(118, 118, 118);")

        self.verticalLayout_7.addWidget(self.pause_all_2)

        self.horizontalLayout_10.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.page_connect)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.drone = QTabWidget(self.frame_11)
        self.drone.setObjectName(u"drone")
        palette21 = QPalette()
        brush28 = QBrush(QColor(61, 61, 61, 255))
        brush28.setStyle(Qt.SolidPattern)
        palette21.setBrush(QPalette.Active, QPalette.Button, brush28)
        palette21.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette21.setBrush(QPalette.Active, QPalette.Base, brush28)
        palette21.setBrush(QPalette.Active, QPalette.Window, brush28)
        palette21.setBrush(QPalette.Inactive, QPalette.Button, brush28)
        palette21.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette21.setBrush(QPalette.Inactive, QPalette.Base, brush28)
        palette21.setBrush(QPalette.Inactive, QPalette.Window, brush28)
        palette21.setBrush(QPalette.Disabled, QPalette.Button, brush28)
        palette21.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette21.setBrush(QPalette.Disabled, QPalette.Base, brush28)
        palette21.setBrush(QPalette.Disabled, QPalette.Window, brush28)
        self.drone.setPalette(palette21)
        font13 = QFont()
        font13.setPointSize(16)
        font13.setItalic(True)
        self.drone.setFont(font13)
        self.drone.setTabPosition(QTabWidget.North)
        self.drone.setTabShape(QTabWidget.Rounded)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label_drone_11 = QLabel(self.tab)
        self.label_drone_11.setObjectName(u"label_drone_11")
        self.label_drone_11.setGeometry(QRect(20, 10, 231, 31))
        font14 = QFont()
        font14.setPointSize(30)
        font14.setBold(True)
        font14.setItalic(True)
        font14.setUnderline(False)
        font14.setWeight(75)
        font14.setStrikeOut(False)
        self.label_drone_11.setFont(font14)
        self.label_drone_11.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_11.setAlignment(Qt.AlignCenter)
        self.label_drone_12 = QLabel(self.tab)
        self.label_drone_12.setObjectName(u"label_drone_12")
        self.label_drone_12.setGeometry(QRect(940, 10, 391, 31))
        self.label_drone_12.setFont(font14)
        self.label_drone_12.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_12.setAlignment(Qt.AlignCenter)
        self.connect_drone_1 = QPushButton(self.tab)
        self.connect_drone_1.setObjectName(u"connect_drone_1")
        self.connect_drone_1.setGeometry(QRect(10, 60, 180, 35))
        palette22 = QPalette()
        palette22.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette22.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette22.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette22.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette22.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette22.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette22.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush29 = QBrush(QColor(0, 0, 0, 128))
        brush29.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette22.setBrush(QPalette.Active, QPalette.PlaceholderText, brush29)
# endif
        palette22.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette22.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette22.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette22.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette22.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette22.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette22.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush30 = QBrush(QColor(0, 0, 0, 128))
        brush30.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette22.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush30)
# endif
        palette22.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette22.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette22.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette22.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette22.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette22.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette22.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush31 = QBrush(QColor(0, 0, 0, 128))
        brush31.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette22.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush31)
# endif
        self.connect_drone_1.setPalette(palette22)
        self.connect_drone_1.setFont(font10)
        self.connect_drone_1.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.connect_drone_1.setAutoDefault(False)
        self.arm_drone_1 = QPushButton(self.tab)
        self.arm_drone_1.setObjectName(u"arm_drone_1")
        self.arm_drone_1.setGeometry(QRect(10, 100, 90, 35))
        palette23 = QPalette()
        palette23.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette23.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette23.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette23.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette23.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette23.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette23.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette23.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette23.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        brush32 = QBrush(QColor(120, 120, 120, 255))
        brush32.setStyle(Qt.SolidPattern)
        palette23.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette23.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette23.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.arm_drone_1.setPalette(palette23)
        self.arm_drone_1.setFont(font10)
        self.arm_drone_1.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.disarm_drone_1 = QPushButton(self.tab)
        self.disarm_drone_1.setObjectName(u"disarm_drone_1")
        self.disarm_drone_1.setGeometry(QRect(100, 100, 90, 35))
        palette24 = QPalette()
        palette24.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette24.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette24.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette24.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette24.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette24.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette24.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette24.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette24.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette24.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette24.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette24.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.disarm_drone_1.setPalette(palette24)
        self.disarm_drone_1.setFont(font10)
        self.disarm_drone_1.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.waiting_connect_1 = QLabel(self.tab)
        self.waiting_connect_1.setObjectName(u"waiting_connect_1")
        self.waiting_connect_1.setGeometry(QRect(200, 70, 171, 19))
        font15 = QFont()
        font15.setItalic(True)
        self.waiting_connect_1.setFont(font15)
        self.arm_or_disarm_drone1 = QLabel(self.tab)
        self.arm_or_disarm_drone1.setObjectName(u"arm_or_disarm_drone1")
        self.arm_or_disarm_drone1.setGeometry(QRect(200, 110, 181, 31))
        self.arm_or_disarm_drone1.setFont(font15)
        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 150, 171, 31))
        self.label_4.setFont(font10)
        self.edit_high_drone_1 = QPlainTextEdit(self.tab)
        self.edit_high_drone_1.setObjectName(u"edit_high_drone_1")
        self.edit_high_drone_1.setGeometry(QRect(200, 150, 91, 31))
        self.edit_high_drone_1.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.take_off_drone_1 = QPushButton(self.tab)
        self.take_off_drone_1.setObjectName(u"take_off_drone_1")
        self.take_off_drone_1.setGeometry(QRect(10, 200, 291, 35))
        palette25 = QPalette()
        palette25.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette25.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette25.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette25.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette25.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette25.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette25.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette25.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette25.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette25.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette25.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette25.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.take_off_drone_1.setPalette(palette25)
        self.take_off_drone_1.setFont(font10)
        self.take_off_drone_1.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.change_altitude_drone1 = QPushButton(self.tab)
        self.change_altitude_drone1.setObjectName(u"change_altitude_drone1")
        self.change_altitude_drone1.setGeometry(QRect(10, 240, 291, 35))
        palette26 = QPalette()
        palette26.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette26.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette26.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette26.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette26.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette26.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette26.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette26.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette26.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette26.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette26.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette26.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_altitude_drone1.setPalette(palette26)
        self.change_altitude_drone1.setFont(font10)
        self.change_altitude_drone1.setStyleSheet(
            u"background:rgb(118, 118, 118)")
        self.land_drone_1 = QPushButton(self.tab)
        self.land_drone_1.setObjectName(u"land_drone_1")
        self.land_drone_1.setGeometry(QRect(10, 280, 291, 35))
        palette27 = QPalette()
        palette27.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette27.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette27.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette27.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette27.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette27.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette27.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette27.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette27.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette27.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette27.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette27.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.land_drone_1.setPalette(palette27)
        self.land_drone_1.setFont(font10)
        self.land_drone_1.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 330, 171, 31))
        self.label_5.setFont(font10)
        self.edit_yaw_drone_1 = QPlainTextEdit(self.tab)
        self.edit_yaw_drone_1.setObjectName(u"edit_yaw_drone_1")
        self.edit_yaw_drone_1.setGeometry(QRect(200, 330, 91, 31))
        self.edit_yaw_drone_1.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.change_yaw_drone_1 = QPushButton(self.tab)
        self.change_yaw_drone_1.setObjectName(u"change_yaw_drone_1")
        self.change_yaw_drone_1.setGeometry(QRect(10, 370, 291, 35))
        palette28 = QPalette()
        palette28.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette28.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette28.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette28.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette28.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette28.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette28.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette28.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette28.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette28.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette28.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette28.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_yaw_drone_1.setPalette(palette28)
        self.change_yaw_drone_1.setFont(font10)
        self.change_yaw_drone_1.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.Monitor_drone_1 = QLabel(self.tab)
        self.Monitor_drone_1.setObjectName(u"Monitor_drone_1")
        self.Monitor_drone_1.setGeometry(QRect(800, 60, 681, 401))
        font16 = QFont()
        font16.setFamily(u"Rockwell")
        font16.setPointSize(15)
        self.Monitor_drone_1.setFont(font16)
        self.Monitor_drone_1.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.Monitor_drone_1.setAlignment(Qt.AlignCenter)
        self.drone_status_1 = QPlainTextEdit(self.tab)
        self.drone_status_1.setObjectName(u"drone_status_1")
        self.drone_status_1.setGeometry(QRect(10, 480, 741, 261))
        palette29 = QPalette()
        palette29.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette29.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette29.setBrush(QPalette.Active, QPalette.Text, brush)
        palette29.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette29.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette29.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette29.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush33 = QBrush(QColor(255, 255, 255, 128))
        brush33.setStyle(Qt.SolidPattern)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette29.setBrush(QPalette.Active, QPalette.PlaceholderText, brush33)
# endif
        palette29.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette29.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette29.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette29.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette29.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette29.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette29.setBrush(QPalette.Inactive, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette29.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush33)
# endif
        palette29.setBrush(QPalette.Disabled, QPalette.WindowText, brush27)
        palette29.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette29.setBrush(QPalette.Disabled, QPalette.Text, brush27)
        palette29.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette29.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette29.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette29.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush34 = QBrush(QColor(0, 0, 0, 128))
        brush34.setStyle(Qt.SolidPattern)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette29.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush34)
# endif
        self.drone_status_1.setPalette(palette29)
        self.drone_status_1.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.camera_status_1 = QPlainTextEdit(self.tab)
        self.camera_status_1.setObjectName(u"camera_status_1")
        self.camera_status_1.setGeometry(QRect(770, 480, 741, 261))
        palette30 = QPalette()
        palette30.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette30.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette30.setBrush(QPalette.Active, QPalette.Text, brush)
        palette30.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette30.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette30.setBrush(QPalette.Active, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette30.setBrush(QPalette.Active, QPalette.PlaceholderText, brush33)
# endif
        palette30.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette30.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette30.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette30.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette30.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette30.setBrush(QPalette.Inactive, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette30.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush33)
# endif
        palette30.setBrush(QPalette.Disabled, QPalette.WindowText, brush27)
        palette30.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette30.setBrush(QPalette.Disabled, QPalette.Text, brush27)
        palette30.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette30.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette30.setBrush(QPalette.Disabled, QPalette.Window, brush1)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette30.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush34)
# endif
        self.camera_status_1.setPalette(palette30)
        self.camera_status_1.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_41 = QFrame(self.tab)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setGeometry(QRect(10, 420, 291, 35))
        self.frame_41.setMinimumSize(QSize(291, 35))
        self.frame_41.setMaximumSize(QSize(291, 35))
        self.frame_41.setFrameShape(QFrame.StyledPanel)
        self.frame_41.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.frame_41)
        self.horizontalLayout_36.setSpacing(2)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.mission_1 = QPushButton(self.frame_41)
        self.mission_1.setObjectName(u"mission_1")
        self.mission_1.setMinimumSize(QSize(97, 35))
        self.mission_1.setMaximumSize(QSize(97, 35))
        palette31 = QPalette()
        palette31.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette31.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette31.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette31.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette31.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette31.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette31.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette31.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette31.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette31.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette31.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette31.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.mission_1.setPalette(palette31)
        font17 = QFont()
        font17.setPointSize(12)
        font17.setBold(True)
        font17.setItalic(True)
        font17.setWeight(75)
        self.mission_1.setFont(font17)
        self.mission_1.setStyleSheet(u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_36.addWidget(self.mission_1)

        self.pause_uav_1 = QPushButton(self.frame_41)
        self.pause_uav_1.setObjectName(u"pause_uav_1")
        self.pause_uav_1.setMinimumSize(QSize(97, 35))
        self.pause_uav_1.setMaximumSize(QSize(97, 35))
        palette32 = QPalette()
        palette32.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette32.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette32.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette32.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette32.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette32.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette32.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette32.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette32.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette32.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette32.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette32.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.pause_uav_1.setPalette(palette32)
        self.pause_uav_1.setFont(font17)
        self.pause_uav_1.setStyleSheet(
            u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_36.addWidget(self.pause_uav_1)

        self.return_and_land_drone_1 = QPushButton(self.frame_41)
        self.return_and_land_drone_1.setObjectName(u"return_and_land_drone_1")
        self.return_and_land_drone_1.setMinimumSize(QSize(97, 35))
        self.return_and_land_drone_1.setMaximumSize(QSize(97, 35))
        palette33 = QPalette()
        palette33.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette33.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette33.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette33.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette33.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette33.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette33.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette33.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette33.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette33.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette33.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette33.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.return_and_land_drone_1.setPalette(palette33)
        self.return_and_land_drone_1.setFont(font10)
        self.return_and_land_drone_1.setStyleSheet(
            u"background:rgb(118, 118, 118)")

        self.horizontalLayout_36.addWidget(self.return_and_land_drone_1)

        self.layoutWidget = QWidget(self.tab)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(410, 60, 341, 401))
        self.layoutWidget.setStyleSheet(u"background-color: rgb(45, 45, 45);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "")
        self.verticalLayout_45 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.verticalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_47 = QHBoxLayout()
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.verticalLayout_46 = QVBoxLayout()
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")
        self.verticalLayout_47 = QVBoxLayout()
        self.verticalLayout_47.setSpacing(0)
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")
        font18 = QFont()
        font18.setPointSize(10)
        font18.setBold(True)
        font18.setItalic(True)
        font18.setWeight(75)
        self.label_6.setFont(font18)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_47.addWidget(self.label_6)

        self.ArmStatus_uav1 = QLabel(self.layoutWidget)
        self.ArmStatus_uav1.setObjectName(u"ArmStatus_uav1")
        self.ArmStatus_uav1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_47.addWidget(self.ArmStatus_uav1)

        self.verticalLayout_46.addLayout(self.verticalLayout_47)

        self.verticalLayout_48 = QVBoxLayout()
        self.verticalLayout_48.setSpacing(0)
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.label_12 = QLabel(self.layoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font18)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.verticalLayout_48.addWidget(self.label_12)

        self.Alt_Rel_uav1 = QLabel(self.layoutWidget)
        self.Alt_Rel_uav1.setObjectName(u"Alt_Rel_uav1")
        self.Alt_Rel_uav1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_48.addWidget(self.Alt_Rel_uav1)

        self.verticalLayout_46.addLayout(self.verticalLayout_48)

        self.verticalLayout_49 = QVBoxLayout()
        self.verticalLayout_49.setSpacing(0)
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.label_15 = QLabel(self.layoutWidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font18)
        self.label_15.setAlignment(Qt.AlignCenter)

        self.verticalLayout_49.addWidget(self.label_15)

        self.Batt_V_uav1 = QLabel(self.layoutWidget)
        self.Batt_V_uav1.setObjectName(u"Batt_V_uav1")
        self.Batt_V_uav1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_49.addWidget(self.Batt_V_uav1)

        self.verticalLayout_46.addLayout(self.verticalLayout_49)

        self.verticalLayout_50 = QVBoxLayout()
        self.verticalLayout_50.setSpacing(0)
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.label_17 = QLabel(self.layoutWidget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font18)
        self.label_17.setAlignment(Qt.AlignCenter)

        self.verticalLayout_50.addWidget(self.label_17)

        self.GPS_Fix_uav1 = QLabel(self.layoutWidget)
        self.GPS_Fix_uav1.setObjectName(u"GPS_Fix_uav1")
        self.GPS_Fix_uav1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_50.addWidget(self.GPS_Fix_uav1)

        self.verticalLayout_46.addLayout(self.verticalLayout_50)

        self.horizontalLayout_47.addLayout(self.verticalLayout_46)

        self.verticalLayout_51 = QVBoxLayout()
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.verticalLayout_52 = QVBoxLayout()
        self.verticalLayout_52.setSpacing(0)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.label_21 = QLabel(self.layoutWidget)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font18)
        self.label_21.setAlignment(Qt.AlignCenter)

        self.verticalLayout_52.addWidget(self.label_21)

        self.Mode_uav1 = QLabel(self.layoutWidget)
        self.Mode_uav1.setObjectName(u"Mode_uav1")
        self.Mode_uav1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_52.addWidget(self.Mode_uav1)

        self.verticalLayout_51.addLayout(self.verticalLayout_52)

        self.verticalLayout_53 = QVBoxLayout()
        self.verticalLayout_53.setSpacing(0)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.label_23 = QLabel(self.layoutWidget)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font18)
        self.label_23.setAlignment(Qt.AlignCenter)

        self.verticalLayout_53.addWidget(self.label_23)

        self.Alt_MSL_uav1 = QLabel(self.layoutWidget)
        self.Alt_MSL_uav1.setObjectName(u"Alt_MSL_uav1")
        self.Alt_MSL_uav1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_53.addWidget(self.Alt_MSL_uav1)

        self.verticalLayout_51.addLayout(self.verticalLayout_53)

        self.verticalLayout_54 = QVBoxLayout()
        self.verticalLayout_54.setSpacing(0)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.label_27 = QLabel(self.layoutWidget)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font18)
        self.label_27.setAlignment(Qt.AlignCenter)

        self.verticalLayout_54.addWidget(self.label_27)

        self.Batt_Rem_uav1 = QLabel(self.layoutWidget)
        self.Batt_Rem_uav1.setObjectName(u"Batt_Rem_uav1")
        self.Batt_Rem_uav1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_54.addWidget(self.Batt_Rem_uav1)

        self.verticalLayout_51.addLayout(self.verticalLayout_54)

        self.verticalLayout_55 = QVBoxLayout()
        self.verticalLayout_55.setSpacing(0)
        self.verticalLayout_55.setObjectName(u"verticalLayout_55")
        self.label_29 = QLabel(self.layoutWidget)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font18)
        self.label_29.setAlignment(Qt.AlignCenter)

        self.verticalLayout_55.addWidget(self.label_29)

        self.Sat_Num_uav1 = QLabel(self.layoutWidget)
        self.Sat_Num_uav1.setObjectName(u"Sat_Num_uav1")
        self.Sat_Num_uav1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_55.addWidget(self.Sat_Num_uav1)

        self.verticalLayout_51.addLayout(self.verticalLayout_55)

        self.horizontalLayout_47.addLayout(self.verticalLayout_51)

        self.verticalLayout_45.addLayout(self.horizontalLayout_47)

        self.verticalLayout_56 = QVBoxLayout()
        self.verticalLayout_56.setObjectName(u"verticalLayout_56")
        self.verticalLayout_57 = QVBoxLayout()
        self.verticalLayout_57.setSpacing(0)
        self.verticalLayout_57.setObjectName(u"verticalLayout_57")
        self.label_44 = QLabel(self.layoutWidget)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFont(font18)
        self.label_44.setAlignment(Qt.AlignCenter)

        self.verticalLayout_57.addWidget(self.label_44)

        self.longitude_uav1 = QLabel(self.layoutWidget)
        self.longitude_uav1.setObjectName(u"longitude_uav1")
        self.longitude_uav1.setStyleSheet(u"")
        self.longitude_uav1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_57.addWidget(self.longitude_uav1)

        self.verticalLayout_56.addLayout(self.verticalLayout_57)

        self.verticalLayout_58 = QVBoxLayout()
        self.verticalLayout_58.setSpacing(0)
        self.verticalLayout_58.setObjectName(u"verticalLayout_58")
        self.label_46 = QLabel(self.layoutWidget)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setFont(font18)
        self.label_46.setAlignment(Qt.AlignCenter)

        self.verticalLayout_58.addWidget(self.label_46)

        self.latitude_uav1 = QLabel(self.layoutWidget)
        self.latitude_uav1.setObjectName(u"latitude_uav1")
        self.latitude_uav1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_58.addWidget(self.latitude_uav1)

        self.verticalLayout_56.addLayout(self.verticalLayout_58)

        self.verticalLayout_45.addLayout(self.verticalLayout_56)

        self.drone.addTab(self.tab, "")
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.label_drone_13 = QLabel(self.widget)
        self.label_drone_13.setObjectName(u"label_drone_13")
        self.label_drone_13.setGeometry(QRect(20, 10, 231, 31))
        self.label_drone_13.setFont(font14)
        self.label_drone_13.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_13.setAlignment(Qt.AlignCenter)
        self.connect_drone_2 = QPushButton(self.widget)
        self.connect_drone_2.setObjectName(u"connect_drone_2")
        self.connect_drone_2.setGeometry(QRect(10, 60, 180, 35))
        palette34 = QPalette()
        palette34.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette34.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette34.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette34.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette34.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette34.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette34.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush35 = QBrush(QColor(0, 0, 0, 128))
        brush35.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette34.setBrush(QPalette.Active, QPalette.PlaceholderText, brush35)
# endif
        palette34.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette34.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette34.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette34.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette34.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette34.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette34.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush36 = QBrush(QColor(0, 0, 0, 128))
        brush36.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette34.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush36)
# endif
        palette34.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette34.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette34.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette34.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette34.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette34.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette34.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush37 = QBrush(QColor(0, 0, 0, 128))
        brush37.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette34.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush37)
# endif
        self.connect_drone_2.setPalette(palette34)
        self.connect_drone_2.setFont(font10)
        self.connect_drone_2.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.connect_drone_2.setAutoDefault(False)
        self.arm_drone_2 = QPushButton(self.widget)
        self.arm_drone_2.setObjectName(u"arm_drone_2")
        self.arm_drone_2.setGeometry(QRect(10, 100, 90, 35))
        palette35 = QPalette()
        palette35.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette35.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette35.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette35.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette35.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette35.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette35.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette35.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette35.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette35.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette35.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette35.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.arm_drone_2.setPalette(palette35)
        self.arm_drone_2.setFont(font10)
        self.arm_drone_2.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.disarm_drone_2 = QPushButton(self.widget)
        self.disarm_drone_2.setObjectName(u"disarm_drone_2")
        self.disarm_drone_2.setGeometry(QRect(100, 100, 90, 35))
        palette36 = QPalette()
        palette36.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette36.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette36.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette36.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette36.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette36.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette36.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette36.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette36.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette36.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette36.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette36.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.disarm_drone_2.setPalette(palette36)
        self.disarm_drone_2.setFont(font10)
        self.disarm_drone_2.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.waiting_connect_2 = QLabel(self.widget)
        self.waiting_connect_2.setObjectName(u"waiting_connect_2")
        self.waiting_connect_2.setGeometry(QRect(200, 70, 171, 19))
        self.waiting_connect_2.setFont(font15)
        self.arm_or_disarm_drone2 = QLabel(self.widget)
        self.arm_or_disarm_drone2.setObjectName(u"arm_or_disarm_drone2")
        self.arm_or_disarm_drone2.setGeometry(QRect(200, 110, 181, 31))
        self.arm_or_disarm_drone2.setFont(font15)
        self.label_13 = QLabel(self.widget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 150, 171, 31))
        self.label_13.setFont(font10)
        self.edit_high_drone_2 = QPlainTextEdit(self.widget)
        self.edit_high_drone_2.setObjectName(u"edit_high_drone_2")
        self.edit_high_drone_2.setGeometry(QRect(200, 150, 91, 31))
        self.edit_high_drone_2.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.take_off_drone_2 = QPushButton(self.widget)
        self.take_off_drone_2.setObjectName(u"take_off_drone_2")
        self.take_off_drone_2.setGeometry(QRect(10, 200, 291, 35))
        palette37 = QPalette()
        palette37.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette37.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette37.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette37.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette37.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette37.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette37.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette37.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette37.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette37.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette37.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette37.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.take_off_drone_2.setPalette(palette37)
        self.take_off_drone_2.setFont(font10)
        self.take_off_drone_2.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.change_altitude_drone2 = QPushButton(self.widget)
        self.change_altitude_drone2.setObjectName(u"change_altitude_drone2")
        self.change_altitude_drone2.setGeometry(QRect(10, 240, 291, 35))
        palette38 = QPalette()
        palette38.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette38.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette38.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette38.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette38.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette38.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette38.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette38.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette38.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette38.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette38.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette38.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_altitude_drone2.setPalette(palette38)
        self.change_altitude_drone2.setFont(font10)
        self.change_altitude_drone2.setStyleSheet(
            u"background:rgb(118, 118, 118)")
        self.land_drone_2 = QPushButton(self.widget)
        self.land_drone_2.setObjectName(u"land_drone_2")
        self.land_drone_2.setGeometry(QRect(10, 280, 291, 35))
        palette39 = QPalette()
        palette39.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette39.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette39.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette39.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette39.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette39.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette39.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette39.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette39.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette39.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette39.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette39.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.land_drone_2.setPalette(palette39)
        self.land_drone_2.setFont(font10)
        self.land_drone_2.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_14 = QLabel(self.widget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(10, 330, 171, 31))
        self.label_14.setFont(font10)
        self.edit_yaw_drone_2 = QPlainTextEdit(self.widget)
        self.edit_yaw_drone_2.setObjectName(u"edit_yaw_drone_2")
        self.edit_yaw_drone_2.setGeometry(QRect(200, 330, 91, 31))
        self.edit_yaw_drone_2.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.change_yaw_drone_2 = QPushButton(self.widget)
        self.change_yaw_drone_2.setObjectName(u"change_yaw_drone_2")
        self.change_yaw_drone_2.setGeometry(QRect(10, 370, 291, 35))
        palette40 = QPalette()
        palette40.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette40.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette40.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette40.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette40.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette40.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette40.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette40.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette40.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette40.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette40.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette40.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_yaw_drone_2.setPalette(palette40)
        self.change_yaw_drone_2.setFont(font10)
        self.change_yaw_drone_2.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_drone_14 = QLabel(self.widget)
        self.label_drone_14.setObjectName(u"label_drone_14")
        self.label_drone_14.setGeometry(QRect(940, 10, 391, 31))
        self.label_drone_14.setFont(font14)
        self.label_drone_14.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_14.setAlignment(Qt.AlignCenter)
        self.Monitor_drone_2 = QLabel(self.widget)
        self.Monitor_drone_2.setObjectName(u"Monitor_drone_2")
        self.Monitor_drone_2.setGeometry(QRect(800, 60, 681, 401))
        self.Monitor_drone_2.setFont(font16)
        self.Monitor_drone_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.Monitor_drone_2.setAlignment(Qt.AlignCenter)
        self.drone_status_2 = QPlainTextEdit(self.widget)
        self.drone_status_2.setObjectName(u"drone_status_2")
        self.drone_status_2.setGeometry(QRect(10, 480, 741, 261))
        self.drone_status_2.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.camera_status_2 = QPlainTextEdit(self.widget)
        self.camera_status_2.setObjectName(u"camera_status_2")
        self.camera_status_2.setGeometry(QRect(770, 480, 741, 261))
        self.camera_status_2.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_43 = QFrame(self.widget)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setGeometry(QRect(10, 420, 291, 35))
        self.frame_43.setMinimumSize(QSize(291, 35))
        self.frame_43.setMaximumSize(QSize(291, 35))
        self.frame_43.setFrameShape(QFrame.StyledPanel)
        self.frame_43.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_43)
        self.horizontalLayout_37.setSpacing(2)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.mission_2 = QPushButton(self.frame_43)
        self.mission_2.setObjectName(u"mission_2")
        self.mission_2.setMinimumSize(QSize(97, 35))
        self.mission_2.setMaximumSize(QSize(97, 35))
        palette41 = QPalette()
        palette41.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette41.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette41.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette41.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette41.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette41.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette41.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette41.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette41.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette41.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette41.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette41.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.mission_2.setPalette(palette41)
        self.mission_2.setFont(font17)
        self.mission_2.setStyleSheet(u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_37.addWidget(self.mission_2)

        self.pause_uav_2 = QPushButton(self.frame_43)
        self.pause_uav_2.setObjectName(u"pause_uav_2")
        self.pause_uav_2.setMinimumSize(QSize(97, 35))
        self.pause_uav_2.setMaximumSize(QSize(97, 35))
        palette42 = QPalette()
        palette42.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette42.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette42.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette42.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette42.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette42.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette42.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette42.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette42.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette42.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette42.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette42.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.pause_uav_2.setPalette(palette42)
        self.pause_uav_2.setFont(font17)
        self.pause_uav_2.setStyleSheet(
            u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_37.addWidget(self.pause_uav_2)

        self.return_and_land_drone_2 = QPushButton(self.frame_43)
        self.return_and_land_drone_2.setObjectName(u"return_and_land_drone_2")
        self.return_and_land_drone_2.setMinimumSize(QSize(97, 35))
        self.return_and_land_drone_2.setMaximumSize(QSize(97, 35))
        palette43 = QPalette()
        palette43.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette43.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette43.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette43.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette43.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette43.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette43.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette43.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette43.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette43.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette43.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette43.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.return_and_land_drone_2.setPalette(palette43)
        self.return_and_land_drone_2.setFont(font10)
        self.return_and_land_drone_2.setStyleSheet(
            u"background:rgb(118, 118, 118)")

        self.horizontalLayout_37.addWidget(self.return_and_land_drone_2)

        self.layoutWidget_2 = QWidget(self.widget)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(410, 60, 341, 401))
        self.layoutWidget_2.setStyleSheet(u"background-color: rgb(45, 45, 45);\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "")
        self.verticalLayout_73 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_73.setObjectName(u"verticalLayout_73")
        self.verticalLayout_73.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.verticalLayout_74 = QVBoxLayout()
        self.verticalLayout_74.setObjectName(u"verticalLayout_74")
        self.verticalLayout_75 = QVBoxLayout()
        self.verticalLayout_75.setSpacing(0)
        self.verticalLayout_75.setObjectName(u"verticalLayout_75")
        self.label_94 = QLabel(self.layoutWidget_2)
        self.label_94.setObjectName(u"label_94")
        self.label_94.setFont(font18)
        self.label_94.setAlignment(Qt.AlignCenter)

        self.verticalLayout_75.addWidget(self.label_94)

        self.ArmStatus_uav2 = QLabel(self.layoutWidget_2)
        self.ArmStatus_uav2.setObjectName(u"ArmStatus_uav2")
        self.ArmStatus_uav2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_75.addWidget(self.ArmStatus_uav2)

        self.verticalLayout_74.addLayout(self.verticalLayout_75)

        self.verticalLayout_76 = QVBoxLayout()
        self.verticalLayout_76.setSpacing(0)
        self.verticalLayout_76.setObjectName(u"verticalLayout_76")
        self.label_95 = QLabel(self.layoutWidget_2)
        self.label_95.setObjectName(u"label_95")
        self.label_95.setFont(font18)
        self.label_95.setAlignment(Qt.AlignCenter)

        self.verticalLayout_76.addWidget(self.label_95)

        self.Alt_Rel_uav2 = QLabel(self.layoutWidget_2)
        self.Alt_Rel_uav2.setObjectName(u"Alt_Rel_uav2")
        self.Alt_Rel_uav2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_76.addWidget(self.Alt_Rel_uav2)

        self.verticalLayout_74.addLayout(self.verticalLayout_76)

        self.verticalLayout_77 = QVBoxLayout()
        self.verticalLayout_77.setSpacing(0)
        self.verticalLayout_77.setObjectName(u"verticalLayout_77")
        self.label_96 = QLabel(self.layoutWidget_2)
        self.label_96.setObjectName(u"label_96")
        self.label_96.setFont(font18)
        self.label_96.setAlignment(Qt.AlignCenter)

        self.verticalLayout_77.addWidget(self.label_96)

        self.Batt_V_uav2 = QLabel(self.layoutWidget_2)
        self.Batt_V_uav2.setObjectName(u"Batt_V_uav2")
        self.Batt_V_uav2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_77.addWidget(self.Batt_V_uav2)

        self.verticalLayout_74.addLayout(self.verticalLayout_77)

        self.verticalLayout_78 = QVBoxLayout()
        self.verticalLayout_78.setSpacing(0)
        self.verticalLayout_78.setObjectName(u"verticalLayout_78")
        self.label_97 = QLabel(self.layoutWidget_2)
        self.label_97.setObjectName(u"label_97")
        self.label_97.setFont(font18)
        self.label_97.setAlignment(Qt.AlignCenter)

        self.verticalLayout_78.addWidget(self.label_97)

        self.GPS_Fix_uav2 = QLabel(self.layoutWidget_2)
        self.GPS_Fix_uav2.setObjectName(u"GPS_Fix_uav2")
        self.GPS_Fix_uav2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_78.addWidget(self.GPS_Fix_uav2)

        self.verticalLayout_74.addLayout(self.verticalLayout_78)

        self.horizontalLayout_49.addLayout(self.verticalLayout_74)

        self.verticalLayout_79 = QVBoxLayout()
        self.verticalLayout_79.setObjectName(u"verticalLayout_79")
        self.verticalLayout_80 = QVBoxLayout()
        self.verticalLayout_80.setSpacing(0)
        self.verticalLayout_80.setObjectName(u"verticalLayout_80")
        self.label_98 = QLabel(self.layoutWidget_2)
        self.label_98.setObjectName(u"label_98")
        self.label_98.setFont(font18)
        self.label_98.setAlignment(Qt.AlignCenter)

        self.verticalLayout_80.addWidget(self.label_98)

        self.Mode_uav2 = QLabel(self.layoutWidget_2)
        self.Mode_uav2.setObjectName(u"Mode_uav2")
        self.Mode_uav2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_80.addWidget(self.Mode_uav2)

        self.verticalLayout_79.addLayout(self.verticalLayout_80)

        self.verticalLayout_81 = QVBoxLayout()
        self.verticalLayout_81.setSpacing(0)
        self.verticalLayout_81.setObjectName(u"verticalLayout_81")
        self.label_99 = QLabel(self.layoutWidget_2)
        self.label_99.setObjectName(u"label_99")
        self.label_99.setFont(font18)
        self.label_99.setAlignment(Qt.AlignCenter)

        self.verticalLayout_81.addWidget(self.label_99)

        self.Alt_MSL_uav2 = QLabel(self.layoutWidget_2)
        self.Alt_MSL_uav2.setObjectName(u"Alt_MSL_uav2")
        self.Alt_MSL_uav2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_81.addWidget(self.Alt_MSL_uav2)

        self.verticalLayout_79.addLayout(self.verticalLayout_81)

        self.verticalLayout_82 = QVBoxLayout()
        self.verticalLayout_82.setSpacing(0)
        self.verticalLayout_82.setObjectName(u"verticalLayout_82")
        self.label_100 = QLabel(self.layoutWidget_2)
        self.label_100.setObjectName(u"label_100")
        self.label_100.setFont(font18)
        self.label_100.setAlignment(Qt.AlignCenter)

        self.verticalLayout_82.addWidget(self.label_100)

        self.Batt_Rem_uav2 = QLabel(self.layoutWidget_2)
        self.Batt_Rem_uav2.setObjectName(u"Batt_Rem_uav2")
        self.Batt_Rem_uav2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_82.addWidget(self.Batt_Rem_uav2)

        self.verticalLayout_79.addLayout(self.verticalLayout_82)

        self.verticalLayout_83 = QVBoxLayout()
        self.verticalLayout_83.setSpacing(0)
        self.verticalLayout_83.setObjectName(u"verticalLayout_83")
        self.label_101 = QLabel(self.layoutWidget_2)
        self.label_101.setObjectName(u"label_101")
        self.label_101.setFont(font18)
        self.label_101.setAlignment(Qt.AlignCenter)

        self.verticalLayout_83.addWidget(self.label_101)

        self.Sat_Num_uav2 = QLabel(self.layoutWidget_2)
        self.Sat_Num_uav2.setObjectName(u"Sat_Num_uav2")
        self.Sat_Num_uav2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_83.addWidget(self.Sat_Num_uav2)

        self.verticalLayout_79.addLayout(self.verticalLayout_83)

        self.horizontalLayout_49.addLayout(self.verticalLayout_79)

        self.verticalLayout_73.addLayout(self.horizontalLayout_49)

        self.verticalLayout_84 = QVBoxLayout()
        self.verticalLayout_84.setObjectName(u"verticalLayout_84")
        self.verticalLayout_85 = QVBoxLayout()
        self.verticalLayout_85.setSpacing(0)
        self.verticalLayout_85.setObjectName(u"verticalLayout_85")
        self.label_102 = QLabel(self.layoutWidget_2)
        self.label_102.setObjectName(u"label_102")
        self.label_102.setFont(font18)
        self.label_102.setAlignment(Qt.AlignCenter)

        self.verticalLayout_85.addWidget(self.label_102)

        self.longitude_uav2 = QLabel(self.layoutWidget_2)
        self.longitude_uav2.setObjectName(u"longitude_uav2")
        self.longitude_uav2.setStyleSheet(u"")
        self.longitude_uav2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_85.addWidget(self.longitude_uav2)

        self.verticalLayout_84.addLayout(self.verticalLayout_85)

        self.verticalLayout_86 = QVBoxLayout()
        self.verticalLayout_86.setSpacing(0)
        self.verticalLayout_86.setObjectName(u"verticalLayout_86")
        self.label_103 = QLabel(self.layoutWidget_2)
        self.label_103.setObjectName(u"label_103")
        self.label_103.setFont(font18)
        self.label_103.setAlignment(Qt.AlignCenter)

        self.verticalLayout_86.addWidget(self.label_103)

        self.latitude_uav2 = QLabel(self.layoutWidget_2)
        self.latitude_uav2.setObjectName(u"latitude_uav2")
        self.latitude_uav2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_86.addWidget(self.latitude_uav2)

        self.verticalLayout_84.addLayout(self.verticalLayout_86)

        self.verticalLayout_73.addLayout(self.verticalLayout_84)

        self.drone.addTab(self.widget, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.label_drone_15 = QLabel(self.tab_3)
        self.label_drone_15.setObjectName(u"label_drone_15")
        self.label_drone_15.setGeometry(QRect(20, 10, 231, 31))
        self.label_drone_15.setFont(font14)
        self.label_drone_15.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_15.setAlignment(Qt.AlignCenter)
        self.connect_drone_3 = QPushButton(self.tab_3)
        self.connect_drone_3.setObjectName(u"connect_drone_3")
        self.connect_drone_3.setGeometry(QRect(10, 60, 180, 35))
        palette44 = QPalette()
        palette44.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette44.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette44.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette44.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette44.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette44.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette44.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush38 = QBrush(QColor(0, 0, 0, 128))
        brush38.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette44.setBrush(QPalette.Active, QPalette.PlaceholderText, brush38)
# endif
        palette44.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette44.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette44.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette44.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette44.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette44.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette44.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush39 = QBrush(QColor(0, 0, 0, 128))
        brush39.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette44.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush39)
# endif
        palette44.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette44.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette44.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette44.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette44.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette44.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette44.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush40 = QBrush(QColor(0, 0, 0, 128))
        brush40.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette44.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush40)
# endif
        self.connect_drone_3.setPalette(palette44)
        self.connect_drone_3.setFont(font10)
        self.connect_drone_3.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.connect_drone_3.setAutoDefault(False)
        self.arm_drone_3 = QPushButton(self.tab_3)
        self.arm_drone_3.setObjectName(u"arm_drone_3")
        self.arm_drone_3.setGeometry(QRect(10, 100, 90, 35))
        palette45 = QPalette()
        palette45.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette45.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette45.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette45.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette45.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette45.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette45.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette45.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette45.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette45.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette45.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette45.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.arm_drone_3.setPalette(palette45)
        self.arm_drone_3.setFont(font10)
        self.arm_drone_3.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.disarm_drone_3 = QPushButton(self.tab_3)
        self.disarm_drone_3.setObjectName(u"disarm_drone_3")
        self.disarm_drone_3.setGeometry(QRect(100, 100, 90, 35))
        palette46 = QPalette()
        palette46.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette46.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette46.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette46.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette46.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette46.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette46.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette46.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette46.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette46.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette46.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette46.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.disarm_drone_3.setPalette(palette46)
        self.disarm_drone_3.setFont(font10)
        self.disarm_drone_3.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.waiting_connect_3 = QLabel(self.tab_3)
        self.waiting_connect_3.setObjectName(u"waiting_connect_3")
        self.waiting_connect_3.setGeometry(QRect(200, 70, 171, 19))
        self.waiting_connect_3.setFont(font15)
        self.arm_or_disarm_drone3 = QLabel(self.tab_3)
        self.arm_or_disarm_drone3.setObjectName(u"arm_or_disarm_drone3")
        self.arm_or_disarm_drone3.setGeometry(QRect(200, 110, 181, 31))
        self.arm_or_disarm_drone3.setFont(font15)
        self.label_19 = QLabel(self.tab_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(10, 150, 171, 31))
        self.label_19.setFont(font10)
        self.edit_high_drone_3 = QPlainTextEdit(self.tab_3)
        self.edit_high_drone_3.setObjectName(u"edit_high_drone_3")
        self.edit_high_drone_3.setGeometry(QRect(200, 150, 91, 31))
        self.edit_high_drone_3.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.take_off_drone_3 = QPushButton(self.tab_3)
        self.take_off_drone_3.setObjectName(u"take_off_drone_3")
        self.take_off_drone_3.setGeometry(QRect(10, 200, 291, 35))
        palette47 = QPalette()
        palette47.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette47.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette47.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette47.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette47.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette47.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette47.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette47.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette47.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette47.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette47.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette47.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.take_off_drone_3.setPalette(palette47)
        self.take_off_drone_3.setFont(font10)
        self.take_off_drone_3.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.change_altitude_drone3 = QPushButton(self.tab_3)
        self.change_altitude_drone3.setObjectName(u"change_altitude_drone3")
        self.change_altitude_drone3.setGeometry(QRect(10, 240, 291, 35))
        palette48 = QPalette()
        palette48.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette48.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette48.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette48.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette48.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette48.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette48.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette48.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette48.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette48.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette48.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette48.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_altitude_drone3.setPalette(palette48)
        self.change_altitude_drone3.setFont(font10)
        self.change_altitude_drone3.setStyleSheet(
            u"background:rgb(118, 118, 118)")
        self.land_drone_3 = QPushButton(self.tab_3)
        self.land_drone_3.setObjectName(u"land_drone_3")
        self.land_drone_3.setGeometry(QRect(10, 280, 291, 35))
        palette49 = QPalette()
        palette49.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette49.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette49.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette49.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette49.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette49.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette49.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette49.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette49.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette49.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette49.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette49.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.land_drone_3.setPalette(palette49)
        self.land_drone_3.setFont(font10)
        self.land_drone_3.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_20 = QLabel(self.tab_3)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(10, 330, 171, 31))
        self.label_20.setFont(font10)
        self.edit_yaw_drone_3 = QPlainTextEdit(self.tab_3)
        self.edit_yaw_drone_3.setObjectName(u"edit_yaw_drone_3")
        self.edit_yaw_drone_3.setGeometry(QRect(200, 330, 91, 31))
        self.edit_yaw_drone_3.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.change_yaw_drone_3 = QPushButton(self.tab_3)
        self.change_yaw_drone_3.setObjectName(u"change_yaw_drone_3")
        self.change_yaw_drone_3.setGeometry(QRect(10, 370, 291, 35))
        palette50 = QPalette()
        palette50.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette50.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette50.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette50.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette50.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette50.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette50.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette50.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette50.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette50.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette50.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette50.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_yaw_drone_3.setPalette(palette50)
        self.change_yaw_drone_3.setFont(font10)
        self.change_yaw_drone_3.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_drone_16 = QLabel(self.tab_3)
        self.label_drone_16.setObjectName(u"label_drone_16")
        self.label_drone_16.setGeometry(QRect(940, 10, 391, 31))
        self.label_drone_16.setFont(font14)
        self.label_drone_16.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_16.setAlignment(Qt.AlignCenter)
        self.Monitor_drone_3 = QLabel(self.tab_3)
        self.Monitor_drone_3.setObjectName(u"Monitor_drone_3")
        self.Monitor_drone_3.setGeometry(QRect(800, 60, 681, 401))
        self.Monitor_drone_3.setFont(font16)
        self.Monitor_drone_3.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.Monitor_drone_3.setAlignment(Qt.AlignCenter)
        self.drone_status_3 = QPlainTextEdit(self.tab_3)
        self.drone_status_3.setObjectName(u"drone_status_3")
        self.drone_status_3.setGeometry(QRect(10, 480, 741, 261))
        self.drone_status_3.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.camera_status_3 = QPlainTextEdit(self.tab_3)
        self.camera_status_3.setObjectName(u"camera_status_3")
        self.camera_status_3.setGeometry(QRect(770, 480, 741, 261))
        self.camera_status_3.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_44 = QFrame(self.tab_3)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setGeometry(QRect(10, 420, 291, 35))
        self.frame_44.setMinimumSize(QSize(291, 35))
        self.frame_44.setMaximumSize(QSize(291, 35))
        self.frame_44.setFrameShape(QFrame.StyledPanel)
        self.frame_44.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_38 = QHBoxLayout(self.frame_44)
        self.horizontalLayout_38.setSpacing(2)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.mission_3 = QPushButton(self.frame_44)
        self.mission_3.setObjectName(u"mission_3")
        self.mission_3.setMinimumSize(QSize(97, 35))
        self.mission_3.setMaximumSize(QSize(97, 35))
        palette51 = QPalette()
        palette51.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette51.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette51.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette51.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette51.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette51.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette51.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette51.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette51.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette51.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette51.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette51.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.mission_3.setPalette(palette51)
        self.mission_3.setFont(font17)
        self.mission_3.setStyleSheet(u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_38.addWidget(self.mission_3)

        self.pause_uav_3 = QPushButton(self.frame_44)
        self.pause_uav_3.setObjectName(u"pause_uav_3")
        self.pause_uav_3.setMinimumSize(QSize(97, 35))
        self.pause_uav_3.setMaximumSize(QSize(97, 35))
        palette52 = QPalette()
        palette52.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette52.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette52.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette52.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette52.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette52.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette52.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette52.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette52.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette52.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette52.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette52.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.pause_uav_3.setPalette(palette52)
        self.pause_uav_3.setFont(font17)
        self.pause_uav_3.setStyleSheet(
            u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_38.addWidget(self.pause_uav_3)

        self.return_and_land_drone_3 = QPushButton(self.frame_44)
        self.return_and_land_drone_3.setObjectName(u"return_and_land_drone_3")
        self.return_and_land_drone_3.setMinimumSize(QSize(97, 35))
        self.return_and_land_drone_3.setMaximumSize(QSize(97, 35))
        palette53 = QPalette()
        palette53.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette53.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette53.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette53.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette53.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette53.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette53.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette53.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette53.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette53.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette53.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette53.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.return_and_land_drone_3.setPalette(palette53)
        self.return_and_land_drone_3.setFont(font10)
        self.return_and_land_drone_3.setStyleSheet(
            u"background:rgb(118, 118, 118)")

        self.horizontalLayout_38.addWidget(self.return_and_land_drone_3)

        self.layoutWidget_3 = QWidget(self.tab_3)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(410, 60, 341, 401))
        self.layoutWidget_3.setStyleSheet(u"background-color: rgb(45, 45, 45);\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "")
        self.verticalLayout_87 = QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_87.setObjectName(u"verticalLayout_87")
        self.verticalLayout_87.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.verticalLayout_88 = QVBoxLayout()
        self.verticalLayout_88.setObjectName(u"verticalLayout_88")
        self.verticalLayout_89 = QVBoxLayout()
        self.verticalLayout_89.setSpacing(0)
        self.verticalLayout_89.setObjectName(u"verticalLayout_89")
        self.label_104 = QLabel(self.layoutWidget_3)
        self.label_104.setObjectName(u"label_104")
        self.label_104.setFont(font18)
        self.label_104.setAlignment(Qt.AlignCenter)

        self.verticalLayout_89.addWidget(self.label_104)

        self.ArmStatus_uav3 = QLabel(self.layoutWidget_3)
        self.ArmStatus_uav3.setObjectName(u"ArmStatus_uav3")
        self.ArmStatus_uav3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_89.addWidget(self.ArmStatus_uav3)

        self.verticalLayout_88.addLayout(self.verticalLayout_89)

        self.verticalLayout_90 = QVBoxLayout()
        self.verticalLayout_90.setSpacing(0)
        self.verticalLayout_90.setObjectName(u"verticalLayout_90")
        self.label_105 = QLabel(self.layoutWidget_3)
        self.label_105.setObjectName(u"label_105")
        self.label_105.setFont(font18)
        self.label_105.setAlignment(Qt.AlignCenter)

        self.verticalLayout_90.addWidget(self.label_105)

        self.Alt_Rel_uav3 = QLabel(self.layoutWidget_3)
        self.Alt_Rel_uav3.setObjectName(u"Alt_Rel_uav3")
        self.Alt_Rel_uav3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_90.addWidget(self.Alt_Rel_uav3)

        self.verticalLayout_88.addLayout(self.verticalLayout_90)

        self.verticalLayout_91 = QVBoxLayout()
        self.verticalLayout_91.setSpacing(0)
        self.verticalLayout_91.setObjectName(u"verticalLayout_91")
        self.label_106 = QLabel(self.layoutWidget_3)
        self.label_106.setObjectName(u"label_106")
        self.label_106.setFont(font18)
        self.label_106.setAlignment(Qt.AlignCenter)

        self.verticalLayout_91.addWidget(self.label_106)

        self.Batt_V_uav3 = QLabel(self.layoutWidget_3)
        self.Batt_V_uav3.setObjectName(u"Batt_V_uav3")
        self.Batt_V_uav3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_91.addWidget(self.Batt_V_uav3)

        self.verticalLayout_88.addLayout(self.verticalLayout_91)

        self.verticalLayout_92 = QVBoxLayout()
        self.verticalLayout_92.setSpacing(0)
        self.verticalLayout_92.setObjectName(u"verticalLayout_92")
        self.label_107 = QLabel(self.layoutWidget_3)
        self.label_107.setObjectName(u"label_107")
        self.label_107.setFont(font18)
        self.label_107.setAlignment(Qt.AlignCenter)

        self.verticalLayout_92.addWidget(self.label_107)

        self.GPS_Fix_uav3 = QLabel(self.layoutWidget_3)
        self.GPS_Fix_uav3.setObjectName(u"GPS_Fix_uav3")
        self.GPS_Fix_uav3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_92.addWidget(self.GPS_Fix_uav3)

        self.verticalLayout_88.addLayout(self.verticalLayout_92)

        self.horizontalLayout_50.addLayout(self.verticalLayout_88)

        self.verticalLayout_93 = QVBoxLayout()
        self.verticalLayout_93.setObjectName(u"verticalLayout_93")
        self.verticalLayout_94 = QVBoxLayout()
        self.verticalLayout_94.setSpacing(0)
        self.verticalLayout_94.setObjectName(u"verticalLayout_94")
        self.label_108 = QLabel(self.layoutWidget_3)
        self.label_108.setObjectName(u"label_108")
        self.label_108.setFont(font18)
        self.label_108.setAlignment(Qt.AlignCenter)

        self.verticalLayout_94.addWidget(self.label_108)

        self.Mode_uav3 = QLabel(self.layoutWidget_3)
        self.Mode_uav3.setObjectName(u"Mode_uav3")
        self.Mode_uav3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_94.addWidget(self.Mode_uav3)

        self.verticalLayout_93.addLayout(self.verticalLayout_94)

        self.verticalLayout_95 = QVBoxLayout()
        self.verticalLayout_95.setSpacing(0)
        self.verticalLayout_95.setObjectName(u"verticalLayout_95")
        self.label_109 = QLabel(self.layoutWidget_3)
        self.label_109.setObjectName(u"label_109")
        self.label_109.setFont(font18)
        self.label_109.setAlignment(Qt.AlignCenter)

        self.verticalLayout_95.addWidget(self.label_109)

        self.Alt_MSL_uav3 = QLabel(self.layoutWidget_3)
        self.Alt_MSL_uav3.setObjectName(u"Alt_MSL_uav3")
        self.Alt_MSL_uav3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_95.addWidget(self.Alt_MSL_uav3)

        self.verticalLayout_93.addLayout(self.verticalLayout_95)

        self.verticalLayout_96 = QVBoxLayout()
        self.verticalLayout_96.setSpacing(0)
        self.verticalLayout_96.setObjectName(u"verticalLayout_96")
        self.label_110 = QLabel(self.layoutWidget_3)
        self.label_110.setObjectName(u"label_110")
        self.label_110.setFont(font18)
        self.label_110.setAlignment(Qt.AlignCenter)

        self.verticalLayout_96.addWidget(self.label_110)

        self.Batt_Rem_uav3 = QLabel(self.layoutWidget_3)
        self.Batt_Rem_uav3.setObjectName(u"Batt_Rem_uav3")
        self.Batt_Rem_uav3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_96.addWidget(self.Batt_Rem_uav3)

        self.verticalLayout_93.addLayout(self.verticalLayout_96)

        self.verticalLayout_97 = QVBoxLayout()
        self.verticalLayout_97.setSpacing(0)
        self.verticalLayout_97.setObjectName(u"verticalLayout_97")
        self.label_111 = QLabel(self.layoutWidget_3)
        self.label_111.setObjectName(u"label_111")
        self.label_111.setFont(font18)
        self.label_111.setAlignment(Qt.AlignCenter)

        self.verticalLayout_97.addWidget(self.label_111)

        self.Sat_Num_uav3 = QLabel(self.layoutWidget_3)
        self.Sat_Num_uav3.setObjectName(u"Sat_Num_uav3")
        self.Sat_Num_uav3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_97.addWidget(self.Sat_Num_uav3)

        self.verticalLayout_93.addLayout(self.verticalLayout_97)

        self.horizontalLayout_50.addLayout(self.verticalLayout_93)

        self.verticalLayout_87.addLayout(self.horizontalLayout_50)

        self.verticalLayout_98 = QVBoxLayout()
        self.verticalLayout_98.setObjectName(u"verticalLayout_98")
        self.verticalLayout_99 = QVBoxLayout()
        self.verticalLayout_99.setSpacing(0)
        self.verticalLayout_99.setObjectName(u"verticalLayout_99")
        self.label_112 = QLabel(self.layoutWidget_3)
        self.label_112.setObjectName(u"label_112")
        self.label_112.setFont(font18)
        self.label_112.setAlignment(Qt.AlignCenter)

        self.verticalLayout_99.addWidget(self.label_112)

        self.longitude_uav3 = QLabel(self.layoutWidget_3)
        self.longitude_uav3.setObjectName(u"longitude_uav3")
        self.longitude_uav3.setStyleSheet(u"")
        self.longitude_uav3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_99.addWidget(self.longitude_uav3)

        self.verticalLayout_98.addLayout(self.verticalLayout_99)

        self.verticalLayout_100 = QVBoxLayout()
        self.verticalLayout_100.setSpacing(0)
        self.verticalLayout_100.setObjectName(u"verticalLayout_100")
        self.label_113 = QLabel(self.layoutWidget_3)
        self.label_113.setObjectName(u"label_113")
        self.label_113.setFont(font18)
        self.label_113.setAlignment(Qt.AlignCenter)

        self.verticalLayout_100.addWidget(self.label_113)

        self.latitude_uav3 = QLabel(self.layoutWidget_3)
        self.latitude_uav3.setObjectName(u"latitude_uav3")
        self.latitude_uav3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_100.addWidget(self.latitude_uav3)

        self.verticalLayout_98.addLayout(self.verticalLayout_100)

        self.verticalLayout_87.addLayout(self.verticalLayout_98)

        self.drone.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.label_drone_17 = QLabel(self.tab_4)
        self.label_drone_17.setObjectName(u"label_drone_17")
        self.label_drone_17.setGeometry(QRect(20, 10, 231, 31))
        self.label_drone_17.setFont(font14)
        self.label_drone_17.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_17.setAlignment(Qt.AlignCenter)
        self.connect_drone_4 = QPushButton(self.tab_4)
        self.connect_drone_4.setObjectName(u"connect_drone_4")
        self.connect_drone_4.setGeometry(QRect(10, 60, 180, 35))
        palette54 = QPalette()
        palette54.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette54.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette54.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette54.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette54.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette54.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette54.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush41 = QBrush(QColor(0, 0, 0, 128))
        brush41.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette54.setBrush(QPalette.Active, QPalette.PlaceholderText, brush41)
# endif
        palette54.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette54.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette54.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette54.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette54.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette54.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette54.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush42 = QBrush(QColor(0, 0, 0, 128))
        brush42.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette54.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush42)
# endif
        palette54.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette54.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette54.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette54.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette54.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette54.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette54.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush43 = QBrush(QColor(0, 0, 0, 128))
        brush43.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette54.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush43)
# endif
        self.connect_drone_4.setPalette(palette54)
        self.connect_drone_4.setFont(font10)
        self.connect_drone_4.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.connect_drone_4.setAutoDefault(False)
        self.arm_drone_4 = QPushButton(self.tab_4)
        self.arm_drone_4.setObjectName(u"arm_drone_4")
        self.arm_drone_4.setGeometry(QRect(10, 100, 90, 35))
        palette55 = QPalette()
        palette55.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette55.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette55.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette55.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette55.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette55.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette55.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette55.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette55.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette55.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette55.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette55.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.arm_drone_4.setPalette(palette55)
        self.arm_drone_4.setFont(font10)
        self.arm_drone_4.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.disarm_drone_4 = QPushButton(self.tab_4)
        self.disarm_drone_4.setObjectName(u"disarm_drone_4")
        self.disarm_drone_4.setGeometry(QRect(100, 100, 90, 35))
        palette56 = QPalette()
        palette56.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette56.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette56.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette56.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette56.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette56.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette56.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette56.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette56.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette56.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette56.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette56.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.disarm_drone_4.setPalette(palette56)
        self.disarm_drone_4.setFont(font10)
        self.disarm_drone_4.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.waiting_connect_4 = QLabel(self.tab_4)
        self.waiting_connect_4.setObjectName(u"waiting_connect_4")
        self.waiting_connect_4.setGeometry(QRect(200, 70, 171, 19))
        self.waiting_connect_4.setFont(font15)
        self.arm_or_disarm_drone4 = QLabel(self.tab_4)
        self.arm_or_disarm_drone4.setObjectName(u"arm_or_disarm_drone4")
        self.arm_or_disarm_drone4.setGeometry(QRect(200, 110, 181, 31))
        self.arm_or_disarm_drone4.setFont(font15)
        self.label_25 = QLabel(self.tab_4)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(10, 150, 171, 31))
        self.label_25.setFont(font10)
        self.edit_high_drone_4 = QPlainTextEdit(self.tab_4)
        self.edit_high_drone_4.setObjectName(u"edit_high_drone_4")
        self.edit_high_drone_4.setGeometry(QRect(200, 150, 91, 31))
        self.edit_high_drone_4.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.take_off_drone_4 = QPushButton(self.tab_4)
        self.take_off_drone_4.setObjectName(u"take_off_drone_4")
        self.take_off_drone_4.setGeometry(QRect(10, 200, 291, 35))
        palette57 = QPalette()
        palette57.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette57.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette57.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette57.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette57.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette57.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette57.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette57.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette57.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette57.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette57.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette57.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.take_off_drone_4.setPalette(palette57)
        self.take_off_drone_4.setFont(font10)
        self.take_off_drone_4.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.change_altitude_drone4 = QPushButton(self.tab_4)
        self.change_altitude_drone4.setObjectName(u"change_altitude_drone4")
        self.change_altitude_drone4.setGeometry(QRect(10, 240, 291, 35))
        palette58 = QPalette()
        palette58.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette58.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette58.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette58.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette58.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette58.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette58.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette58.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette58.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette58.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette58.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette58.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_altitude_drone4.setPalette(palette58)
        self.change_altitude_drone4.setFont(font10)
        self.change_altitude_drone4.setStyleSheet(
            u"background:rgb(118, 118, 118)")
        self.land_drone_4 = QPushButton(self.tab_4)
        self.land_drone_4.setObjectName(u"land_drone_4")
        self.land_drone_4.setGeometry(QRect(10, 280, 291, 35))
        palette59 = QPalette()
        palette59.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette59.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette59.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette59.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette59.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette59.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette59.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette59.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette59.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette59.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette59.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette59.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.land_drone_4.setPalette(palette59)
        self.land_drone_4.setFont(font10)
        self.land_drone_4.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_26 = QLabel(self.tab_4)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(10, 330, 171, 31))
        self.label_26.setFont(font10)
        self.edit_yaw_drone_4 = QPlainTextEdit(self.tab_4)
        self.edit_yaw_drone_4.setObjectName(u"edit_yaw_drone_4")
        self.edit_yaw_drone_4.setGeometry(QRect(200, 330, 91, 31))
        self.edit_yaw_drone_4.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.change_yaw_drone_4 = QPushButton(self.tab_4)
        self.change_yaw_drone_4.setObjectName(u"change_yaw_drone_4")
        self.change_yaw_drone_4.setGeometry(QRect(10, 370, 291, 35))
        palette60 = QPalette()
        palette60.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette60.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette60.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette60.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette60.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette60.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette60.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette60.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette60.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette60.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette60.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette60.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_yaw_drone_4.setPalette(palette60)
        self.change_yaw_drone_4.setFont(font10)
        self.change_yaw_drone_4.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_drone_18 = QLabel(self.tab_4)
        self.label_drone_18.setObjectName(u"label_drone_18")
        self.label_drone_18.setGeometry(QRect(940, 10, 391, 31))
        self.label_drone_18.setFont(font14)
        self.label_drone_18.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_18.setAlignment(Qt.AlignCenter)
        self.Monitor_drone_4 = QLabel(self.tab_4)
        self.Monitor_drone_4.setObjectName(u"Monitor_drone_4")
        self.Monitor_drone_4.setGeometry(QRect(800, 60, 681, 401))
        self.Monitor_drone_4.setFont(font16)
        self.Monitor_drone_4.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.Monitor_drone_4.setAlignment(Qt.AlignCenter)
        self.drone_status_4 = QPlainTextEdit(self.tab_4)
        self.drone_status_4.setObjectName(u"drone_status_4")
        self.drone_status_4.setGeometry(QRect(10, 480, 741, 261))
        self.drone_status_4.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.camera_status_4 = QPlainTextEdit(self.tab_4)
        self.camera_status_4.setObjectName(u"camera_status_4")
        self.camera_status_4.setGeometry(QRect(770, 480, 741, 261))
        self.camera_status_4.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_45 = QFrame(self.tab_4)
        self.frame_45.setObjectName(u"frame_45")
        self.frame_45.setGeometry(QRect(10, 420, 291, 35))
        self.frame_45.setMinimumSize(QSize(291, 35))
        self.frame_45.setMaximumSize(QSize(291, 35))
        self.frame_45.setFrameShape(QFrame.StyledPanel)
        self.frame_45.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_39 = QHBoxLayout(self.frame_45)
        self.horizontalLayout_39.setSpacing(2)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.horizontalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.mission_4 = QPushButton(self.frame_45)
        self.mission_4.setObjectName(u"mission_4")
        self.mission_4.setMinimumSize(QSize(97, 35))
        self.mission_4.setMaximumSize(QSize(97, 35))
        palette61 = QPalette()
        palette61.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette61.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette61.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette61.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette61.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette61.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette61.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette61.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette61.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette61.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette61.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette61.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.mission_4.setPalette(palette61)
        self.mission_4.setFont(font17)
        self.mission_4.setStyleSheet(u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_39.addWidget(self.mission_4)

        self.pause_uav_4 = QPushButton(self.frame_45)
        self.pause_uav_4.setObjectName(u"pause_uav_4")
        self.pause_uav_4.setMinimumSize(QSize(97, 35))
        self.pause_uav_4.setMaximumSize(QSize(97, 35))
        palette62 = QPalette()
        palette62.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette62.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette62.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette62.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette62.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette62.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette62.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette62.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette62.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette62.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette62.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette62.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.pause_uav_4.setPalette(palette62)
        self.pause_uav_4.setFont(font17)
        self.pause_uav_4.setStyleSheet(
            u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_39.addWidget(self.pause_uav_4)

        self.return_and_land_drone_4 = QPushButton(self.frame_45)
        self.return_and_land_drone_4.setObjectName(u"return_and_land_drone_4")
        self.return_and_land_drone_4.setMinimumSize(QSize(97, 35))
        self.return_and_land_drone_4.setMaximumSize(QSize(97, 35))
        palette63 = QPalette()
        palette63.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette63.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette63.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette63.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette63.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette63.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette63.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette63.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette63.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette63.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette63.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette63.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.return_and_land_drone_4.setPalette(palette63)
        self.return_and_land_drone_4.setFont(font10)
        self.return_and_land_drone_4.setStyleSheet(
            u"background:rgb(118, 118, 118)")

        self.horizontalLayout_39.addWidget(self.return_and_land_drone_4)

        self.layoutWidget_4 = QWidget(self.tab_4)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(410, 60, 341, 401))
        self.layoutWidget_4.setStyleSheet(u"background-color: rgb(45, 45, 45);\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "")
        self.verticalLayout_101 = QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_101.setObjectName(u"verticalLayout_101")
        self.verticalLayout_101.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_51 = QHBoxLayout()
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.verticalLayout_102 = QVBoxLayout()
        self.verticalLayout_102.setObjectName(u"verticalLayout_102")
        self.verticalLayout_103 = QVBoxLayout()
        self.verticalLayout_103.setSpacing(0)
        self.verticalLayout_103.setObjectName(u"verticalLayout_103")
        self.label_114 = QLabel(self.layoutWidget_4)
        self.label_114.setObjectName(u"label_114")
        self.label_114.setFont(font18)
        self.label_114.setAlignment(Qt.AlignCenter)

        self.verticalLayout_103.addWidget(self.label_114)

        self.ArmStatus_uav4 = QLabel(self.layoutWidget_4)
        self.ArmStatus_uav4.setObjectName(u"ArmStatus_uav4")
        self.ArmStatus_uav4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_103.addWidget(self.ArmStatus_uav4)

        self.verticalLayout_102.addLayout(self.verticalLayout_103)

        self.verticalLayout_104 = QVBoxLayout()
        self.verticalLayout_104.setSpacing(0)
        self.verticalLayout_104.setObjectName(u"verticalLayout_104")
        self.label_115 = QLabel(self.layoutWidget_4)
        self.label_115.setObjectName(u"label_115")
        self.label_115.setFont(font18)
        self.label_115.setAlignment(Qt.AlignCenter)

        self.verticalLayout_104.addWidget(self.label_115)

        self.Alt_Rel_uav4 = QLabel(self.layoutWidget_4)
        self.Alt_Rel_uav4.setObjectName(u"Alt_Rel_uav4")
        self.Alt_Rel_uav4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_104.addWidget(self.Alt_Rel_uav4)

        self.verticalLayout_102.addLayout(self.verticalLayout_104)

        self.verticalLayout_105 = QVBoxLayout()
        self.verticalLayout_105.setSpacing(0)
        self.verticalLayout_105.setObjectName(u"verticalLayout_105")
        self.label_116 = QLabel(self.layoutWidget_4)
        self.label_116.setObjectName(u"label_116")
        self.label_116.setFont(font18)
        self.label_116.setAlignment(Qt.AlignCenter)

        self.verticalLayout_105.addWidget(self.label_116)

        self.Batt_V_uav4 = QLabel(self.layoutWidget_4)
        self.Batt_V_uav4.setObjectName(u"Batt_V_uav4")
        self.Batt_V_uav4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_105.addWidget(self.Batt_V_uav4)

        self.verticalLayout_102.addLayout(self.verticalLayout_105)

        self.verticalLayout_106 = QVBoxLayout()
        self.verticalLayout_106.setSpacing(0)
        self.verticalLayout_106.setObjectName(u"verticalLayout_106")
        self.label_117 = QLabel(self.layoutWidget_4)
        self.label_117.setObjectName(u"label_117")
        self.label_117.setFont(font18)
        self.label_117.setAlignment(Qt.AlignCenter)

        self.verticalLayout_106.addWidget(self.label_117)

        self.GPS_Fix_uav4 = QLabel(self.layoutWidget_4)
        self.GPS_Fix_uav4.setObjectName(u"GPS_Fix_uav4")
        self.GPS_Fix_uav4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_106.addWidget(self.GPS_Fix_uav4)

        self.verticalLayout_102.addLayout(self.verticalLayout_106)

        self.horizontalLayout_51.addLayout(self.verticalLayout_102)

        self.verticalLayout_107 = QVBoxLayout()
        self.verticalLayout_107.setObjectName(u"verticalLayout_107")
        self.verticalLayout_108 = QVBoxLayout()
        self.verticalLayout_108.setSpacing(0)
        self.verticalLayout_108.setObjectName(u"verticalLayout_108")
        self.label_118 = QLabel(self.layoutWidget_4)
        self.label_118.setObjectName(u"label_118")
        self.label_118.setFont(font18)
        self.label_118.setAlignment(Qt.AlignCenter)

        self.verticalLayout_108.addWidget(self.label_118)

        self.Mode_uav4 = QLabel(self.layoutWidget_4)
        self.Mode_uav4.setObjectName(u"Mode_uav4")
        self.Mode_uav4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_108.addWidget(self.Mode_uav4)

        self.verticalLayout_107.addLayout(self.verticalLayout_108)

        self.verticalLayout_109 = QVBoxLayout()
        self.verticalLayout_109.setSpacing(0)
        self.verticalLayout_109.setObjectName(u"verticalLayout_109")
        self.label_119 = QLabel(self.layoutWidget_4)
        self.label_119.setObjectName(u"label_119")
        self.label_119.setFont(font18)
        self.label_119.setAlignment(Qt.AlignCenter)

        self.verticalLayout_109.addWidget(self.label_119)

        self.Alt_MSL_uav4 = QLabel(self.layoutWidget_4)
        self.Alt_MSL_uav4.setObjectName(u"Alt_MSL_uav4")
        self.Alt_MSL_uav4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_109.addWidget(self.Alt_MSL_uav4)

        self.verticalLayout_107.addLayout(self.verticalLayout_109)

        self.verticalLayout_110 = QVBoxLayout()
        self.verticalLayout_110.setSpacing(0)
        self.verticalLayout_110.setObjectName(u"verticalLayout_110")
        self.label_120 = QLabel(self.layoutWidget_4)
        self.label_120.setObjectName(u"label_120")
        self.label_120.setFont(font18)
        self.label_120.setAlignment(Qt.AlignCenter)

        self.verticalLayout_110.addWidget(self.label_120)

        self.Batt_Rem_uav4 = QLabel(self.layoutWidget_4)
        self.Batt_Rem_uav4.setObjectName(u"Batt_Rem_uav4")
        self.Batt_Rem_uav4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_110.addWidget(self.Batt_Rem_uav4)

        self.verticalLayout_107.addLayout(self.verticalLayout_110)

        self.verticalLayout_111 = QVBoxLayout()
        self.verticalLayout_111.setSpacing(0)
        self.verticalLayout_111.setObjectName(u"verticalLayout_111")
        self.label_121 = QLabel(self.layoutWidget_4)
        self.label_121.setObjectName(u"label_121")
        self.label_121.setFont(font18)
        self.label_121.setAlignment(Qt.AlignCenter)

        self.verticalLayout_111.addWidget(self.label_121)

        self.Sat_Num_uav4 = QLabel(self.layoutWidget_4)
        self.Sat_Num_uav4.setObjectName(u"Sat_Num_uav4")
        self.Sat_Num_uav4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_111.addWidget(self.Sat_Num_uav4)

        self.verticalLayout_107.addLayout(self.verticalLayout_111)

        self.horizontalLayout_51.addLayout(self.verticalLayout_107)

        self.verticalLayout_101.addLayout(self.horizontalLayout_51)

        self.verticalLayout_112 = QVBoxLayout()
        self.verticalLayout_112.setObjectName(u"verticalLayout_112")
        self.verticalLayout_113 = QVBoxLayout()
        self.verticalLayout_113.setSpacing(0)
        self.verticalLayout_113.setObjectName(u"verticalLayout_113")
        self.label_122 = QLabel(self.layoutWidget_4)
        self.label_122.setObjectName(u"label_122")
        self.label_122.setFont(font18)
        self.label_122.setAlignment(Qt.AlignCenter)

        self.verticalLayout_113.addWidget(self.label_122)

        self.longitude_uav4 = QLabel(self.layoutWidget_4)
        self.longitude_uav4.setObjectName(u"longitude_uav4")
        self.longitude_uav4.setStyleSheet(u"")
        self.longitude_uav4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_113.addWidget(self.longitude_uav4)

        self.verticalLayout_112.addLayout(self.verticalLayout_113)

        self.verticalLayout_114 = QVBoxLayout()
        self.verticalLayout_114.setSpacing(0)
        self.verticalLayout_114.setObjectName(u"verticalLayout_114")
        self.label_123 = QLabel(self.layoutWidget_4)
        self.label_123.setObjectName(u"label_123")
        self.label_123.setFont(font18)
        self.label_123.setAlignment(Qt.AlignCenter)

        self.verticalLayout_114.addWidget(self.label_123)

        self.latitude_uav4 = QLabel(self.layoutWidget_4)
        self.latitude_uav4.setObjectName(u"latitude_uav4")
        self.latitude_uav4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_114.addWidget(self.latitude_uav4)

        self.verticalLayout_112.addLayout(self.verticalLayout_114)

        self.verticalLayout_101.addLayout(self.verticalLayout_112)

        self.drone.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.label_drone_25 = QLabel(self.tab_5)
        self.label_drone_25.setObjectName(u"label_drone_25")
        self.label_drone_25.setGeometry(QRect(20, 10, 231, 31))
        self.label_drone_25.setFont(font14)
        self.label_drone_25.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_25.setAlignment(Qt.AlignCenter)
        self.connect_drone_5 = QPushButton(self.tab_5)
        self.connect_drone_5.setObjectName(u"connect_drone_5")
        self.connect_drone_5.setGeometry(QRect(10, 60, 180, 35))
        palette64 = QPalette()
        palette64.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette64.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette64.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette64.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette64.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette64.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette64.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush44 = QBrush(QColor(0, 0, 0, 128))
        brush44.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette64.setBrush(QPalette.Active, QPalette.PlaceholderText, brush44)
# endif
        palette64.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette64.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette64.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette64.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette64.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette64.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette64.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush45 = QBrush(QColor(0, 0, 0, 128))
        brush45.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette64.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush45)
# endif
        palette64.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette64.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette64.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette64.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette64.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette64.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette64.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush46 = QBrush(QColor(0, 0, 0, 128))
        brush46.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette64.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush46)
# endif
        self.connect_drone_5.setPalette(palette64)
        self.connect_drone_5.setFont(font10)
        self.connect_drone_5.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.connect_drone_5.setAutoDefault(False)
        self.waiting_connect_5 = QLabel(self.tab_5)
        self.waiting_connect_5.setObjectName(u"waiting_connect_5")
        self.waiting_connect_5.setGeometry(QRect(200, 70, 171, 19))
        self.waiting_connect_5.setFont(font15)
        self.arm_drone_5 = QPushButton(self.tab_5)
        self.arm_drone_5.setObjectName(u"arm_drone_5")
        self.arm_drone_5.setGeometry(QRect(10, 100, 90, 35))
        palette65 = QPalette()
        palette65.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette65.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette65.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette65.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette65.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette65.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette65.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette65.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette65.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette65.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette65.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette65.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.arm_drone_5.setPalette(palette65)
        self.arm_drone_5.setFont(font10)
        self.arm_drone_5.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.disarm_drone_5 = QPushButton(self.tab_5)
        self.disarm_drone_5.setObjectName(u"disarm_drone_5")
        self.disarm_drone_5.setGeometry(QRect(100, 100, 90, 35))
        palette66 = QPalette()
        palette66.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette66.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette66.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette66.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette66.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette66.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette66.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette66.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette66.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette66.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette66.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette66.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.disarm_drone_5.setPalette(palette66)
        self.disarm_drone_5.setFont(font10)
        self.disarm_drone_5.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.arm_or_disarm_drone5 = QLabel(self.tab_5)
        self.arm_or_disarm_drone5.setObjectName(u"arm_or_disarm_drone5")
        self.arm_or_disarm_drone5.setGeometry(QRect(200, 110, 181, 31))
        self.arm_or_disarm_drone5.setFont(font15)
        self.label_42 = QLabel(self.tab_5)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setGeometry(QRect(10, 150, 171, 31))
        self.label_42.setFont(font10)
        self.edit_high_drone_5 = QPlainTextEdit(self.tab_5)
        self.edit_high_drone_5.setObjectName(u"edit_high_drone_5")
        self.edit_high_drone_5.setGeometry(QRect(200, 150, 91, 31))
        self.edit_high_drone_5.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.take_off_drone_5 = QPushButton(self.tab_5)
        self.take_off_drone_5.setObjectName(u"take_off_drone_5")
        self.take_off_drone_5.setGeometry(QRect(10, 200, 291, 35))
        palette67 = QPalette()
        palette67.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette67.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette67.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette67.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette67.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette67.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette67.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette67.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette67.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette67.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette67.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette67.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.take_off_drone_5.setPalette(palette67)
        self.take_off_drone_5.setFont(font10)
        self.take_off_drone_5.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.change_altitude_drone5 = QPushButton(self.tab_5)
        self.change_altitude_drone5.setObjectName(u"change_altitude_drone5")
        self.change_altitude_drone5.setGeometry(QRect(10, 240, 291, 35))
        palette68 = QPalette()
        palette68.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette68.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette68.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette68.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette68.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette68.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette68.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette68.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette68.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette68.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette68.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette68.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_altitude_drone5.setPalette(palette68)
        self.change_altitude_drone5.setFont(font10)
        self.change_altitude_drone5.setStyleSheet(
            u"background:rgb(118, 118, 118)")
        self.land_drone_5 = QPushButton(self.tab_5)
        self.land_drone_5.setObjectName(u"land_drone_5")
        self.land_drone_5.setGeometry(QRect(10, 280, 291, 35))
        palette69 = QPalette()
        palette69.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette69.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette69.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette69.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette69.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette69.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette69.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette69.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette69.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette69.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette69.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette69.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.land_drone_5.setPalette(palette69)
        self.land_drone_5.setFont(font10)
        self.land_drone_5.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_43 = QLabel(self.tab_5)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setGeometry(QRect(10, 330, 171, 31))
        self.label_43.setFont(font10)
        self.edit_yaw_drone_5 = QPlainTextEdit(self.tab_5)
        self.edit_yaw_drone_5.setObjectName(u"edit_yaw_drone_5")
        self.edit_yaw_drone_5.setGeometry(QRect(200, 330, 91, 31))
        self.edit_yaw_drone_5.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.change_yaw_drone_5 = QPushButton(self.tab_5)
        self.change_yaw_drone_5.setObjectName(u"change_yaw_drone_5")
        self.change_yaw_drone_5.setGeometry(QRect(10, 370, 291, 35))
        palette70 = QPalette()
        palette70.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette70.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette70.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette70.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette70.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette70.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette70.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette70.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette70.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette70.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette70.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette70.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_yaw_drone_5.setPalette(palette70)
        self.change_yaw_drone_5.setFont(font10)
        self.change_yaw_drone_5.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_drone_26 = QLabel(self.tab_5)
        self.label_drone_26.setObjectName(u"label_drone_26")
        self.label_drone_26.setGeometry(QRect(940, 10, 391, 31))
        self.label_drone_26.setFont(font14)
        self.label_drone_26.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_26.setAlignment(Qt.AlignCenter)
        self.Monitor_drone_5 = QLabel(self.tab_5)
        self.Monitor_drone_5.setObjectName(u"Monitor_drone_5")
        self.Monitor_drone_5.setGeometry(QRect(800, 60, 681, 401))
        self.Monitor_drone_5.setFont(font16)
        self.Monitor_drone_5.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.Monitor_drone_5.setAlignment(Qt.AlignCenter)
        self.drone_status_5 = QPlainTextEdit(self.tab_5)
        self.drone_status_5.setObjectName(u"drone_status_5")
        self.drone_status_5.setGeometry(QRect(10, 480, 741, 261))
        self.drone_status_5.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.camera_status_5 = QPlainTextEdit(self.tab_5)
        self.camera_status_5.setObjectName(u"camera_status_5")
        self.camera_status_5.setGeometry(QRect(770, 480, 741, 261))
        self.camera_status_5.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_46 = QFrame(self.tab_5)
        self.frame_46.setObjectName(u"frame_46")
        self.frame_46.setGeometry(QRect(10, 420, 291, 35))
        self.frame_46.setMinimumSize(QSize(291, 35))
        self.frame_46.setMaximumSize(QSize(291, 35))
        self.frame_46.setFrameShape(QFrame.StyledPanel)
        self.frame_46.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_40 = QHBoxLayout(self.frame_46)
        self.horizontalLayout_40.setSpacing(2)
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.horizontalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.mission_5 = QPushButton(self.frame_46)
        self.mission_5.setObjectName(u"mission_5")
        self.mission_5.setMinimumSize(QSize(97, 35))
        self.mission_5.setMaximumSize(QSize(97, 35))
        palette71 = QPalette()
        palette71.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette71.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette71.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette71.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette71.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette71.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette71.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette71.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette71.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette71.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette71.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette71.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.mission_5.setPalette(palette71)
        self.mission_5.setFont(font17)
        self.mission_5.setStyleSheet(u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_40.addWidget(self.mission_5)

        self.pause_uav_5 = QPushButton(self.frame_46)
        self.pause_uav_5.setObjectName(u"pause_uav_5")
        self.pause_uav_5.setMinimumSize(QSize(97, 35))
        self.pause_uav_5.setMaximumSize(QSize(97, 35))
        palette72 = QPalette()
        palette72.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette72.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette72.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette72.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette72.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette72.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette72.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette72.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette72.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette72.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette72.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette72.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.pause_uav_5.setPalette(palette72)
        self.pause_uav_5.setFont(font17)
        self.pause_uav_5.setStyleSheet(
            u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_40.addWidget(self.pause_uav_5)

        self.return_and_land_drone_5 = QPushButton(self.frame_46)
        self.return_and_land_drone_5.setObjectName(u"return_and_land_drone_5")
        self.return_and_land_drone_5.setMinimumSize(QSize(97, 35))
        self.return_and_land_drone_5.setMaximumSize(QSize(97, 35))
        palette73 = QPalette()
        palette73.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette73.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette73.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette73.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette73.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette73.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette73.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette73.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette73.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette73.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette73.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette73.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.return_and_land_drone_5.setPalette(palette73)
        self.return_and_land_drone_5.setFont(font10)
        self.return_and_land_drone_5.setStyleSheet(
            u"background:rgb(118, 118, 118)")

        self.horizontalLayout_40.addWidget(self.return_and_land_drone_5)

        self.layoutWidget_5 = QWidget(self.tab_5)
        self.layoutWidget_5.setObjectName(u"layoutWidget_5")
        self.layoutWidget_5.setGeometry(QRect(410, 60, 341, 401))
        self.layoutWidget_5.setStyleSheet(u"background-color: rgb(45, 45, 45);\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "")
        self.verticalLayout_115 = QVBoxLayout(self.layoutWidget_5)
        self.verticalLayout_115.setObjectName(u"verticalLayout_115")
        self.verticalLayout_115.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_52 = QHBoxLayout()
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.verticalLayout_116 = QVBoxLayout()
        self.verticalLayout_116.setObjectName(u"verticalLayout_116")
        self.verticalLayout_117 = QVBoxLayout()
        self.verticalLayout_117.setSpacing(0)
        self.verticalLayout_117.setObjectName(u"verticalLayout_117")
        self.label_124 = QLabel(self.layoutWidget_5)
        self.label_124.setObjectName(u"label_124")
        self.label_124.setFont(font18)
        self.label_124.setAlignment(Qt.AlignCenter)

        self.verticalLayout_117.addWidget(self.label_124)

        self.ArmStatus_uav5 = QLabel(self.layoutWidget_5)
        self.ArmStatus_uav5.setObjectName(u"ArmStatus_uav5")
        self.ArmStatus_uav5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_117.addWidget(self.ArmStatus_uav5)

        self.verticalLayout_116.addLayout(self.verticalLayout_117)

        self.verticalLayout_118 = QVBoxLayout()
        self.verticalLayout_118.setSpacing(0)
        self.verticalLayout_118.setObjectName(u"verticalLayout_118")
        self.label_125 = QLabel(self.layoutWidget_5)
        self.label_125.setObjectName(u"label_125")
        self.label_125.setFont(font18)
        self.label_125.setAlignment(Qt.AlignCenter)

        self.verticalLayout_118.addWidget(self.label_125)

        self.Alt_Rel_uav5 = QLabel(self.layoutWidget_5)
        self.Alt_Rel_uav5.setObjectName(u"Alt_Rel_uav5")
        self.Alt_Rel_uav5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_118.addWidget(self.Alt_Rel_uav5)

        self.verticalLayout_116.addLayout(self.verticalLayout_118)

        self.verticalLayout_119 = QVBoxLayout()
        self.verticalLayout_119.setSpacing(0)
        self.verticalLayout_119.setObjectName(u"verticalLayout_119")
        self.label_126 = QLabel(self.layoutWidget_5)
        self.label_126.setObjectName(u"label_126")
        self.label_126.setFont(font18)
        self.label_126.setAlignment(Qt.AlignCenter)

        self.verticalLayout_119.addWidget(self.label_126)

        self.Batt_V_uav5 = QLabel(self.layoutWidget_5)
        self.Batt_V_uav5.setObjectName(u"Batt_V_uav5")
        self.Batt_V_uav5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_119.addWidget(self.Batt_V_uav5)

        self.verticalLayout_116.addLayout(self.verticalLayout_119)

        self.verticalLayout_120 = QVBoxLayout()
        self.verticalLayout_120.setSpacing(0)
        self.verticalLayout_120.setObjectName(u"verticalLayout_120")
        self.label_127 = QLabel(self.layoutWidget_5)
        self.label_127.setObjectName(u"label_127")
        self.label_127.setFont(font18)
        self.label_127.setAlignment(Qt.AlignCenter)

        self.verticalLayout_120.addWidget(self.label_127)

        self.GPS_Fix_uav5 = QLabel(self.layoutWidget_5)
        self.GPS_Fix_uav5.setObjectName(u"GPS_Fix_uav5")
        self.GPS_Fix_uav5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_120.addWidget(self.GPS_Fix_uav5)

        self.verticalLayout_116.addLayout(self.verticalLayout_120)

        self.horizontalLayout_52.addLayout(self.verticalLayout_116)

        self.verticalLayout_121 = QVBoxLayout()
        self.verticalLayout_121.setObjectName(u"verticalLayout_121")
        self.verticalLayout_122 = QVBoxLayout()
        self.verticalLayout_122.setSpacing(0)
        self.verticalLayout_122.setObjectName(u"verticalLayout_122")
        self.label_128 = QLabel(self.layoutWidget_5)
        self.label_128.setObjectName(u"label_128")
        self.label_128.setFont(font18)
        self.label_128.setAlignment(Qt.AlignCenter)

        self.verticalLayout_122.addWidget(self.label_128)

        self.Mode_uav5 = QLabel(self.layoutWidget_5)
        self.Mode_uav5.setObjectName(u"Mode_uav5")
        self.Mode_uav5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_122.addWidget(self.Mode_uav5)

        self.verticalLayout_121.addLayout(self.verticalLayout_122)

        self.verticalLayout_123 = QVBoxLayout()
        self.verticalLayout_123.setSpacing(0)
        self.verticalLayout_123.setObjectName(u"verticalLayout_123")
        self.label_129 = QLabel(self.layoutWidget_5)
        self.label_129.setObjectName(u"label_129")
        self.label_129.setFont(font18)
        self.label_129.setAlignment(Qt.AlignCenter)

        self.verticalLayout_123.addWidget(self.label_129)

        self.Alt_MSL_uav5 = QLabel(self.layoutWidget_5)
        self.Alt_MSL_uav5.setObjectName(u"Alt_MSL_uav5")
        self.Alt_MSL_uav5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_123.addWidget(self.Alt_MSL_uav5)

        self.verticalLayout_121.addLayout(self.verticalLayout_123)

        self.verticalLayout_124 = QVBoxLayout()
        self.verticalLayout_124.setSpacing(0)
        self.verticalLayout_124.setObjectName(u"verticalLayout_124")
        self.label_130 = QLabel(self.layoutWidget_5)
        self.label_130.setObjectName(u"label_130")
        self.label_130.setFont(font18)
        self.label_130.setAlignment(Qt.AlignCenter)

        self.verticalLayout_124.addWidget(self.label_130)

        self.Batt_Rem_uav5 = QLabel(self.layoutWidget_5)
        self.Batt_Rem_uav5.setObjectName(u"Batt_Rem_uav5")
        self.Batt_Rem_uav5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_124.addWidget(self.Batt_Rem_uav5)

        self.verticalLayout_121.addLayout(self.verticalLayout_124)

        self.verticalLayout_125 = QVBoxLayout()
        self.verticalLayout_125.setSpacing(0)
        self.verticalLayout_125.setObjectName(u"verticalLayout_125")
        self.label_131 = QLabel(self.layoutWidget_5)
        self.label_131.setObjectName(u"label_131")
        self.label_131.setFont(font18)
        self.label_131.setAlignment(Qt.AlignCenter)

        self.verticalLayout_125.addWidget(self.label_131)

        self.Sat_Num_uav5 = QLabel(self.layoutWidget_5)
        self.Sat_Num_uav5.setObjectName(u"Sat_Num_uav5")
        self.Sat_Num_uav5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_125.addWidget(self.Sat_Num_uav5)

        self.verticalLayout_121.addLayout(self.verticalLayout_125)

        self.horizontalLayout_52.addLayout(self.verticalLayout_121)

        self.verticalLayout_115.addLayout(self.horizontalLayout_52)

        self.verticalLayout_126 = QVBoxLayout()
        self.verticalLayout_126.setObjectName(u"verticalLayout_126")
        self.verticalLayout_127 = QVBoxLayout()
        self.verticalLayout_127.setSpacing(0)
        self.verticalLayout_127.setObjectName(u"verticalLayout_127")
        self.label_132 = QLabel(self.layoutWidget_5)
        self.label_132.setObjectName(u"label_132")
        self.label_132.setFont(font18)
        self.label_132.setAlignment(Qt.AlignCenter)

        self.verticalLayout_127.addWidget(self.label_132)

        self.longitude_uav5 = QLabel(self.layoutWidget_5)
        self.longitude_uav5.setObjectName(u"longitude_uav5")
        self.longitude_uav5.setStyleSheet(u"")
        self.longitude_uav5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_127.addWidget(self.longitude_uav5)

        self.verticalLayout_126.addLayout(self.verticalLayout_127)

        self.verticalLayout_128 = QVBoxLayout()
        self.verticalLayout_128.setSpacing(0)
        self.verticalLayout_128.setObjectName(u"verticalLayout_128")
        self.label_133 = QLabel(self.layoutWidget_5)
        self.label_133.setObjectName(u"label_133")
        self.label_133.setFont(font18)
        self.label_133.setAlignment(Qt.AlignCenter)

        self.verticalLayout_128.addWidget(self.label_133)

        self.latitude_uav5 = QLabel(self.layoutWidget_5)
        self.latitude_uav5.setObjectName(u"latitude_uav5")
        self.latitude_uav5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_128.addWidget(self.latitude_uav5)

        self.verticalLayout_126.addLayout(self.verticalLayout_128)

        self.verticalLayout_115.addLayout(self.verticalLayout_126)

        self.drone.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.label_drone_39 = QLabel(self.tab_6)
        self.label_drone_39.setObjectName(u"label_drone_39")
        self.label_drone_39.setGeometry(QRect(20, 10, 231, 31))
        self.label_drone_39.setFont(font14)
        self.label_drone_39.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_39.setAlignment(Qt.AlignCenter)
        self.connect_drone_6 = QPushButton(self.tab_6)
        self.connect_drone_6.setObjectName(u"connect_drone_6")
        self.connect_drone_6.setGeometry(QRect(10, 60, 180, 35))
        palette74 = QPalette()
        palette74.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette74.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette74.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette74.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette74.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette74.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette74.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
        brush47 = QBrush(QColor(0, 0, 0, 128))
        brush47.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette74.setBrush(QPalette.Active, QPalette.PlaceholderText, brush47)
# endif
        palette74.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette74.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette74.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette74.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette74.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette74.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette74.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
        brush48 = QBrush(QColor(0, 0, 0, 128))
        brush48.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette74.setBrush(QPalette.Inactive,
                           QPalette.PlaceholderText, brush48)
# endif
        palette74.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette74.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette74.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette74.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette74.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette74.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        palette74.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
        brush49 = QBrush(QColor(0, 0, 0, 128))
        brush49.setStyle(Qt.NoBrush)
# if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette74.setBrush(QPalette.Disabled,
                           QPalette.PlaceholderText, brush49)
# endif
        self.connect_drone_6.setPalette(palette74)
        self.connect_drone_6.setFont(font10)
        self.connect_drone_6.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.connect_drone_6.setAutoDefault(False)
        self.waiting_connect_6 = QLabel(self.tab_6)
        self.waiting_connect_6.setObjectName(u"waiting_connect_6")
        self.waiting_connect_6.setGeometry(QRect(200, 70, 171, 19))
        self.waiting_connect_6.setFont(font15)
        self.arm_drone_6 = QPushButton(self.tab_6)
        self.arm_drone_6.setObjectName(u"arm_drone_6")
        self.arm_drone_6.setGeometry(QRect(10, 100, 90, 35))
        palette75 = QPalette()
        palette75.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette75.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette75.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette75.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette75.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette75.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette75.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette75.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette75.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette75.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette75.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette75.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.arm_drone_6.setPalette(palette75)
        self.arm_drone_6.setFont(font10)
        self.arm_drone_6.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.disarm_drone_6 = QPushButton(self.tab_6)
        self.disarm_drone_6.setObjectName(u"disarm_drone_6")
        self.disarm_drone_6.setGeometry(QRect(100, 100, 90, 35))
        palette76 = QPalette()
        palette76.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette76.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette76.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette76.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette76.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette76.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette76.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette76.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette76.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette76.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette76.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette76.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.disarm_drone_6.setPalette(palette76)
        self.disarm_drone_6.setFont(font10)
        self.disarm_drone_6.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.arm_or_disarm_drone6 = QLabel(self.tab_6)
        self.arm_or_disarm_drone6.setObjectName(u"arm_or_disarm_drone6")
        self.arm_or_disarm_drone6.setGeometry(QRect(200, 110, 181, 31))
        self.arm_or_disarm_drone6.setFont(font15)
        self.label_77 = QLabel(self.tab_6)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setGeometry(QRect(10, 150, 171, 31))
        self.label_77.setFont(font10)
        self.edit_high_drone_6 = QPlainTextEdit(self.tab_6)
        self.edit_high_drone_6.setObjectName(u"edit_high_drone_6")
        self.edit_high_drone_6.setGeometry(QRect(200, 150, 91, 31))
        self.edit_high_drone_6.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.take_off_drone_6 = QPushButton(self.tab_6)
        self.take_off_drone_6.setObjectName(u"take_off_drone_6")
        self.take_off_drone_6.setGeometry(QRect(10, 200, 291, 35))
        palette77 = QPalette()
        palette77.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette77.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette77.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette77.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette77.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette77.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette77.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette77.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette77.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette77.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette77.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette77.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.take_off_drone_6.setPalette(palette77)
        self.take_off_drone_6.setFont(font10)
        self.take_off_drone_6.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.change_altitude_drone6 = QPushButton(self.tab_6)
        self.change_altitude_drone6.setObjectName(u"change_altitude_drone6")
        self.change_altitude_drone6.setGeometry(QRect(10, 240, 291, 35))
        palette78 = QPalette()
        palette78.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette78.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette78.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette78.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette78.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette78.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette78.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette78.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette78.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette78.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette78.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette78.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_altitude_drone6.setPalette(palette78)
        self.change_altitude_drone6.setFont(font10)
        self.change_altitude_drone6.setStyleSheet(
            u"background:rgb(118, 118, 118)")
        self.land_drone_6 = QPushButton(self.tab_6)
        self.land_drone_6.setObjectName(u"land_drone_6")
        self.land_drone_6.setGeometry(QRect(10, 280, 291, 35))
        palette79 = QPalette()
        palette79.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette79.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette79.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette79.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette79.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette79.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette79.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette79.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette79.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette79.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette79.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette79.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.land_drone_6.setPalette(palette79)
        self.land_drone_6.setFont(font10)
        self.land_drone_6.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_78 = QLabel(self.tab_6)
        self.label_78.setObjectName(u"label_78")
        self.label_78.setGeometry(QRect(10, 330, 171, 31))
        self.label_78.setFont(font10)
        self.edit_yaw_drone_7 = QPlainTextEdit(self.tab_6)
        self.edit_yaw_drone_7.setObjectName(u"edit_yaw_drone_7")
        self.edit_yaw_drone_7.setGeometry(QRect(200, 330, 91, 31))
        self.edit_yaw_drone_7.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.change_yaw_drone_6 = QPushButton(self.tab_6)
        self.change_yaw_drone_6.setObjectName(u"change_yaw_drone_6")
        self.change_yaw_drone_6.setGeometry(QRect(10, 370, 291, 35))
        palette80 = QPalette()
        palette80.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette80.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette80.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette80.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette80.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette80.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette80.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette80.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette80.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette80.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette80.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette80.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.change_yaw_drone_6.setPalette(palette80)
        self.change_yaw_drone_6.setFont(font10)
        self.change_yaw_drone_6.setStyleSheet(u"background:rgb(118, 118, 118)")
        self.label_drone_40 = QLabel(self.tab_6)
        self.label_drone_40.setObjectName(u"label_drone_40")
        self.label_drone_40.setGeometry(QRect(940, 10, 391, 31))
        self.label_drone_40.setFont(font14)
        self.label_drone_40.setStyleSheet(u"\n"
                                          "\n"
                                          "color: rgb(237, 51, 59);")
        self.label_drone_40.setAlignment(Qt.AlignCenter)
        self.Monitor_drone_6 = QLabel(self.tab_6)
        self.Monitor_drone_6.setObjectName(u"Monitor_drone_6")
        self.Monitor_drone_6.setGeometry(QRect(800, 60, 681, 401))
        self.Monitor_drone_6.setFont(font16)
        self.Monitor_drone_6.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.Monitor_drone_6.setAlignment(Qt.AlignCenter)
        self.drone_status_6 = QPlainTextEdit(self.tab_6)
        self.drone_status_6.setObjectName(u"drone_status_6")
        self.drone_status_6.setGeometry(QRect(10, 480, 741, 261))
        self.drone_status_6.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.camera_status_6 = QPlainTextEdit(self.tab_6)
        self.camera_status_6.setObjectName(u"camera_status_6")
        self.camera_status_6.setGeometry(QRect(770, 480, 741, 261))
        self.camera_status_6.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_47 = QFrame(self.tab_6)
        self.frame_47.setObjectName(u"frame_47")
        self.frame_47.setGeometry(QRect(10, 420, 291, 35))
        self.frame_47.setMinimumSize(QSize(291, 35))
        self.frame_47.setMaximumSize(QSize(291, 35))
        self.frame_47.setFrameShape(QFrame.StyledPanel)
        self.frame_47.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_41 = QHBoxLayout(self.frame_47)
        self.horizontalLayout_41.setSpacing(2)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.horizontalLayout_41.setContentsMargins(0, 0, 0, 0)
        self.mission_6 = QPushButton(self.frame_47)
        self.mission_6.setObjectName(u"mission_6")
        self.mission_6.setMinimumSize(QSize(97, 35))
        self.mission_6.setMaximumSize(QSize(97, 35))
        palette81 = QPalette()
        palette81.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette81.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette81.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette81.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette81.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette81.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette81.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette81.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette81.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette81.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette81.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette81.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.mission_6.setPalette(palette81)
        self.mission_6.setFont(font17)
        self.mission_6.setStyleSheet(u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_41.addWidget(self.mission_6)

        self.pause_uav_6 = QPushButton(self.frame_47)
        self.pause_uav_6.setObjectName(u"pause_uav_6")
        self.pause_uav_6.setMinimumSize(QSize(97, 35))
        self.pause_uav_6.setMaximumSize(QSize(97, 35))
        palette82 = QPalette()
        palette82.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette82.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette82.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette82.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette82.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette82.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette82.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette82.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette82.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette82.setBrush(QPalette.Disabled, QPalette.ButtonText, brush27)
        palette82.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette82.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.pause_uav_6.setPalette(palette82)
        self.pause_uav_6.setFont(font17)
        self.pause_uav_6.setStyleSheet(
            u"background-color: rgb(118, 118, 118);")

        self.horizontalLayout_41.addWidget(self.pause_uav_6)

        self.return_and_land_drone_6 = QPushButton(self.frame_47)
        self.return_and_land_drone_6.setObjectName(u"return_and_land_drone_6")
        self.return_and_land_drone_6.setMinimumSize(QSize(97, 35))
        self.return_and_land_drone_6.setMaximumSize(QSize(97, 35))
        palette83 = QPalette()
        palette83.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette83.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette83.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette83.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette83.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette83.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette83.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette83.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette83.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette83.setBrush(QPalette.Disabled, QPalette.ButtonText, brush32)
        palette83.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette83.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.return_and_land_drone_6.setPalette(palette83)
        self.return_and_land_drone_6.setFont(font10)
        self.return_and_land_drone_6.setStyleSheet(
            u"background:rgb(118, 118, 118)")

        self.horizontalLayout_41.addWidget(self.return_and_land_drone_6)

        self.layoutWidget_6 = QWidget(self.tab_6)
        self.layoutWidget_6.setObjectName(u"layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(410, 60, 341, 401))
        self.layoutWidget_6.setStyleSheet(u"background-color: rgb(45, 45, 45);\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "")
        self.verticalLayout_129 = QVBoxLayout(self.layoutWidget_6)
        self.verticalLayout_129.setObjectName(u"verticalLayout_129")
        self.verticalLayout_129.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_53 = QHBoxLayout()
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.verticalLayout_130 = QVBoxLayout()
        self.verticalLayout_130.setObjectName(u"verticalLayout_130")
        self.verticalLayout_131 = QVBoxLayout()
        self.verticalLayout_131.setSpacing(0)
        self.verticalLayout_131.setObjectName(u"verticalLayout_131")
        self.label_134 = QLabel(self.layoutWidget_6)
        self.label_134.setObjectName(u"label_134")
        self.label_134.setFont(font18)
        self.label_134.setAlignment(Qt.AlignCenter)

        self.verticalLayout_131.addWidget(self.label_134)

        self.ArmStatus_uav6 = QLabel(self.layoutWidget_6)
        self.ArmStatus_uav6.setObjectName(u"ArmStatus_uav6")
        self.ArmStatus_uav6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_131.addWidget(self.ArmStatus_uav6)

        self.verticalLayout_130.addLayout(self.verticalLayout_131)

        self.verticalLayout_132 = QVBoxLayout()
        self.verticalLayout_132.setSpacing(0)
        self.verticalLayout_132.setObjectName(u"verticalLayout_132")
        self.label_135 = QLabel(self.layoutWidget_6)
        self.label_135.setObjectName(u"label_135")
        self.label_135.setFont(font18)
        self.label_135.setAlignment(Qt.AlignCenter)

        self.verticalLayout_132.addWidget(self.label_135)

        self.Alt_Rel_uav6 = QLabel(self.layoutWidget_6)
        self.Alt_Rel_uav6.setObjectName(u"Alt_Rel_uav6")
        self.Alt_Rel_uav6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_132.addWidget(self.Alt_Rel_uav6)

        self.verticalLayout_130.addLayout(self.verticalLayout_132)

        self.verticalLayout_133 = QVBoxLayout()
        self.verticalLayout_133.setSpacing(0)
        self.verticalLayout_133.setObjectName(u"verticalLayout_133")
        self.label_136 = QLabel(self.layoutWidget_6)
        self.label_136.setObjectName(u"label_136")
        self.label_136.setFont(font18)
        self.label_136.setAlignment(Qt.AlignCenter)

        self.verticalLayout_133.addWidget(self.label_136)

        self.Batt_V_uav6 = QLabel(self.layoutWidget_6)
        self.Batt_V_uav6.setObjectName(u"Batt_V_uav6")
        self.Batt_V_uav6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_133.addWidget(self.Batt_V_uav6)

        self.verticalLayout_130.addLayout(self.verticalLayout_133)

        self.verticalLayout_134 = QVBoxLayout()
        self.verticalLayout_134.setSpacing(0)
        self.verticalLayout_134.setObjectName(u"verticalLayout_134")
        self.label_137 = QLabel(self.layoutWidget_6)
        self.label_137.setObjectName(u"label_137")
        self.label_137.setFont(font18)
        self.label_137.setAlignment(Qt.AlignCenter)

        self.verticalLayout_134.addWidget(self.label_137)

        self.GPS_Fix_uav6 = QLabel(self.layoutWidget_6)
        self.GPS_Fix_uav6.setObjectName(u"GPS_Fix_uav6")
        self.GPS_Fix_uav6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_134.addWidget(self.GPS_Fix_uav6)

        self.verticalLayout_130.addLayout(self.verticalLayout_134)

        self.horizontalLayout_53.addLayout(self.verticalLayout_130)

        self.verticalLayout_135 = QVBoxLayout()
        self.verticalLayout_135.setObjectName(u"verticalLayout_135")
        self.verticalLayout_136 = QVBoxLayout()
        self.verticalLayout_136.setSpacing(0)
        self.verticalLayout_136.setObjectName(u"verticalLayout_136")
        self.label_138 = QLabel(self.layoutWidget_6)
        self.label_138.setObjectName(u"label_138")
        self.label_138.setFont(font18)
        self.label_138.setAlignment(Qt.AlignCenter)

        self.verticalLayout_136.addWidget(self.label_138)

        self.Mode_uav6 = QLabel(self.layoutWidget_6)
        self.Mode_uav6.setObjectName(u"Mode_uav6")
        self.Mode_uav6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_136.addWidget(self.Mode_uav6)

        self.verticalLayout_135.addLayout(self.verticalLayout_136)

        self.verticalLayout_137 = QVBoxLayout()
        self.verticalLayout_137.setSpacing(0)
        self.verticalLayout_137.setObjectName(u"verticalLayout_137")
        self.label_139 = QLabel(self.layoutWidget_6)
        self.label_139.setObjectName(u"label_139")
        self.label_139.setFont(font18)
        self.label_139.setAlignment(Qt.AlignCenter)

        self.verticalLayout_137.addWidget(self.label_139)

        self.Alt_MSL_uav6 = QLabel(self.layoutWidget_6)
        self.Alt_MSL_uav6.setObjectName(u"Alt_MSL_uav6")
        self.Alt_MSL_uav6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_137.addWidget(self.Alt_MSL_uav6)

        self.verticalLayout_135.addLayout(self.verticalLayout_137)

        self.verticalLayout_138 = QVBoxLayout()
        self.verticalLayout_138.setSpacing(0)
        self.verticalLayout_138.setObjectName(u"verticalLayout_138")
        self.label_140 = QLabel(self.layoutWidget_6)
        self.label_140.setObjectName(u"label_140")
        self.label_140.setFont(font18)
        self.label_140.setAlignment(Qt.AlignCenter)

        self.verticalLayout_138.addWidget(self.label_140)

        self.Batt_Rem_uav6 = QLabel(self.layoutWidget_6)
        self.Batt_Rem_uav6.setObjectName(u"Batt_Rem_uav6")
        self.Batt_Rem_uav6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_138.addWidget(self.Batt_Rem_uav6)

        self.verticalLayout_135.addLayout(self.verticalLayout_138)

        self.verticalLayout_139 = QVBoxLayout()
        self.verticalLayout_139.setSpacing(0)
        self.verticalLayout_139.setObjectName(u"verticalLayout_139")
        self.label_141 = QLabel(self.layoutWidget_6)
        self.label_141.setObjectName(u"label_141")
        self.label_141.setFont(font18)
        self.label_141.setAlignment(Qt.AlignCenter)

        self.verticalLayout_139.addWidget(self.label_141)

        self.Sat_Num_uav6 = QLabel(self.layoutWidget_6)
        self.Sat_Num_uav6.setObjectName(u"Sat_Num_uav6")
        self.Sat_Num_uav6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_139.addWidget(self.Sat_Num_uav6)

        self.verticalLayout_135.addLayout(self.verticalLayout_139)

        self.horizontalLayout_53.addLayout(self.verticalLayout_135)

        self.verticalLayout_129.addLayout(self.horizontalLayout_53)

        self.verticalLayout_140 = QVBoxLayout()
        self.verticalLayout_140.setObjectName(u"verticalLayout_140")
        self.verticalLayout_141 = QVBoxLayout()
        self.verticalLayout_141.setSpacing(0)
        self.verticalLayout_141.setObjectName(u"verticalLayout_141")
        self.label_142 = QLabel(self.layoutWidget_6)
        self.label_142.setObjectName(u"label_142")
        self.label_142.setFont(font18)
        self.label_142.setAlignment(Qt.AlignCenter)

        self.verticalLayout_141.addWidget(self.label_142)

        self.longitude_uav6 = QLabel(self.layoutWidget_6)
        self.longitude_uav6.setObjectName(u"longitude_uav6")
        self.longitude_uav6.setStyleSheet(u"")
        self.longitude_uav6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_141.addWidget(self.longitude_uav6)

        self.verticalLayout_140.addLayout(self.verticalLayout_141)

        self.verticalLayout_142 = QVBoxLayout()
        self.verticalLayout_142.setSpacing(0)
        self.verticalLayout_142.setObjectName(u"verticalLayout_142")
        self.label_143 = QLabel(self.layoutWidget_6)
        self.label_143.setObjectName(u"label_143")
        self.label_143.setFont(font18)
        self.label_143.setAlignment(Qt.AlignCenter)

        self.verticalLayout_142.addWidget(self.label_143)

        self.latitude_uav6 = QLabel(self.layoutWidget_6)
        self.latitude_uav6.setObjectName(u"latitude_uav6")
        self.latitude_uav6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_142.addWidget(self.latitude_uav6)

        self.verticalLayout_140.addLayout(self.verticalLayout_142)

        self.verticalLayout_129.addLayout(self.verticalLayout_140)

        self.drone.addTab(self.tab_6, "")

        self.horizontalLayout_11.addWidget(self.drone)

        self.horizontalLayout_10.addWidget(self.frame_11)

        self.stackedWidget.addWidget(self.page_connect)

        self.verticalLayout_8.addWidget(self.stackedWidget)

        self.verticalLayout.addWidget(self.main_body_contents)

        self.footer = QFrame(self.main_body)
        self.footer.setObjectName(u"footer")
        self.footer.setFrameShape(QFrame.StyledPanel)
        self.footer.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.footer)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.footer)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.footer)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3.addWidget(self.frame_5)

        self.size_grip = QFrame(self.footer)
        self.size_grip.setObjectName(u"size_grip")
        self.size_grip.setMinimumSize(QSize(10, 10))
        self.size_grip.setMaximumSize(QSize(10, 10))
        self.size_grip.setFrameShape(QFrame.StyledPanel)
        self.size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_3.addWidget(
            self.size_grip, 0, Qt.AlignRight | Qt.AlignBottom)

        self.verticalLayout.addWidget(self.footer, 0, Qt.AlignBottom)

        self.horizontalLayout.addWidget(self.main_body)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)
        self.drone.setCurrentIndex(5)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate(
            "MainWindow", u"MENU", None))
        self.btn_home.setText(QCoreApplication.translate(
            "MainWindow", u"HOME", None))
        self.btn_connect.setText(QCoreApplication.translate(
            "MainWindow", u"CONNECT", None))
        self.btn_map.setText(QCoreApplication.translate(
            "MainWindow", u"MAP", None))
        self.btn_parameter.setText(QCoreApplication.translate(
            "MainWindow", u"PARAMETER", None))
        self.btn_algorithm.setText(QCoreApplication.translate(
            "MainWindow", u"ALGORITHM", None))
        self.exit_button.setText(
            QCoreApplication.translate("MainWindow", u"Exit", None))
        self.open_close_side_bar_btn.setText("")
        self.label.setText(QCoreApplication.translate(
            "MainWindow", u"PH\u1ea6N M\u1ec0M \u0110I\u1ec0U KHI\u1ec2N T\u00cdCH H\u1ee2P GI\u00c1M S\u00c1T TH\u00d4NG MINH CHO B\u1ea6Y \u0110\u00c0N M\u00c1Y BAY KH\u00d4NG NG\u01af\u1edcI L\u00c1I", None))
        self.minimize_window_button.setText("")
        self.restore_window_button.setText("")
        self.close_window_button.setText("")
        self.label_76.setText(QCoreApplication.translate(
            "MainWindow", u"LATITUDE", None))
        self.label_82.setText(QCoreApplication.translate(
            "MainWindow", u"LONGTITUDE", None))
        self.pushButton.setText(
            QCoreApplication.translate("MainWindow", u"ADD", None))
        self.fly_1_uav.setText(QCoreApplication.translate(
            "MainWindow", u"1 UAV", None))
        self.fly_2_uav.setText(QCoreApplication.translate(
            "MainWindow", u"2 UAV", None))
        self.fly_3_UAV.setText(QCoreApplication.translate(
            "MainWindow", u"3 UAV", None))
        self.fly_4_UAV.setText(QCoreApplication.translate(
            "MainWindow", u"4 UAV", None))
        self.label_24.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 1", None))
        self.label_30.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 2", None))
        self.label_31.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 3", None))
        self.label_32.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 4", None))
        self.label_33.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 5", None))
        self.label_34.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 6", None))
        self.label_3.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone1's Camera", None))
        self.label_7.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone2's Camera", None))
        self.label_8.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone3's Camera", None))
        self.label_9.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone4's Camera", None))
        self.label_10.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone5's Camera", None))
        self.label_18.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone6's Camera", None))
        self.label_35.setText(QCoreApplication.translate(
            "MainWindow", u"Photo from Drone 1", None))
        self.label_36.setText(QCoreApplication.translate(
            "MainWindow", u"Photo from Drone 2", None))
        self.label_37.setText(QCoreApplication.translate(
            "MainWindow", u"Photo from Drone 3", None))
        self.label_38.setText(QCoreApplication.translate(
            "MainWindow", u"Photo from Drone 4", None))
        self.label_39.setText(QCoreApplication.translate(
            "MainWindow", u"Photo from Drone 5", None))
        self.label_40.setText(QCoreApplication.translate(
            "MainWindow", u"Photo from Drone 6", None))
        self.pushButton_3.setText(
            QCoreApplication.translate("MainWindow", u"DETECT", None))
        self.pushButton_4.setText(QCoreApplication.translate(
            "MainWindow", u"CAMERA CONTROL", None))
        self.pushButton_5.setText(
            QCoreApplication.translate("MainWindow", u"RTL ALL", None))
        self.label_41.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 1", None))
        self.label_47.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 2", None))
        self.label_48.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 3", None))
        self.label_49.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 4", None))
        self.label_50.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 5", None))
        self.label_51.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 6", None))
        self.label_52.setText(QCoreApplication.translate(
            "MainWindow", u"MIS_TAKEOFF_ALT", None))
        self.label_53.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_TKO_SPEED", None))
        self.label_54.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_LAND_SPEED", None))
        self.label_55.setText(QCoreApplication.translate(
            "MainWindow", u"COM_DISARM_LAND", None))
        self.label_56.setText(QCoreApplication.translate(
            "MainWindow", u"MIS_TAKEOFF_ALT", None))
        self.label_57.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_TKO_SPEED", None))
        self.label_58.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_LAND_SPEED", None))
        self.label_59.setText(QCoreApplication.translate(
            "MainWindow", u"COM_DISARM_LAND", None))
        self.label_60.setText(QCoreApplication.translate(
            "MainWindow", u"MIS_TAKEOFF_ALT", None))
        self.label_61.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_TKO_SPEED", None))
        self.label_62.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_LAND_SPEED", None))
        self.label_63.setText(QCoreApplication.translate(
            "MainWindow", u"COM_DISARM_LAND", None))
        self.label_64.setText(QCoreApplication.translate(
            "MainWindow", u"MIS_TAKEOFF_ALT", None))
        self.label_65.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_TKO_SPEED", None))
        self.label_66.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_LAND_SPEED", None))
        self.label_67.setText(QCoreApplication.translate(
            "MainWindow", u"COM_DISARM_LAND", None))
        self.label_68.setText(QCoreApplication.translate(
            "MainWindow", u"MIS_TAKEOFF_ALT", None))
        self.label_69.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_TKO_SPEED", None))
        self.label_70.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_LAND_SPEED", None))
        self.label_71.setText(QCoreApplication.translate(
            "MainWindow", u"COM_DISARM_LAND", None))
        self.label_72.setText(QCoreApplication.translate(
            "MainWindow", u"MIS_TAKEOFF_ALT", None))
        self.label_73.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_TKO_SPEED", None))
        self.label_74.setText(QCoreApplication.translate(
            "MainWindow", u"MPC_LAND_SPEED", None))
        self.label_75.setText(QCoreApplication.translate(
            "MainWindow", u"COM_DISARM_LAND", None))
        self.label_11.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 1", None))
        self.label_45.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 2", None))
        self.label_80.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 3", None))
        self.label_83.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 4", None))
        self.label_84.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 5", None))
        self.label_85.setText(QCoreApplication.translate(
            "MainWindow", u"UAV 6", None))
        self.file_1.setText("")
        self.file_2.setText("")
        self.file_3.setText("")
        self.file_4.setText("")
        self.file_5.setText("")
        self.file_6.setText("")
        self.Load_MS_1.setText("")
        self.mission_uav1.setText("")
        self.pause_1.setText("")
        self.Load_MS_2.setText("")
        self.mission_uav2.setText("")
        self.pause_2.setText("")
        self.Load_MS_3.setText("")
        self.mission_uav3.setText("")
        self.pause_3.setText("")
        self.Load_MS_4.setText("")
        self.mission_uav4.setText("")
        self.pause_4.setText("")
        self.Load_MS_5.setText("")
        self.mission_uav5.setText("")
        self.pause_5.setText("")
        self.Load_MS_6.setText("")
        self.mission_uav6.setText("")
        self.pause_6.setText("")
        self.file_all.setText(QCoreApplication.translate(
            "MainWindow", u"FILE ALL UAV", None))
        self.pushButton_2.setText("")
        self.Load_MS_all.setText(QCoreApplication.translate(
            "MainWindow", u"UPLOAD ALL", None))
        self.mission_all_2.setText(QCoreApplication.translate(
            "MainWindow", u"MISSION ALL", None))
        self.pause_all.setText(QCoreApplication.translate(
            "MainWindow", u"PAUSE ALL", None))
        self.btn_map_all.setText(
            QCoreApplication.translate("MainWindow", u"MAP", None))
        self.label_22.setText(QCoreApplication.translate(
            "MainWindow", u"Longtitude:", None))
        self.label_16.setText(QCoreApplication.translate(
            "MainWindow", u"Latitude:", None))
        self.goto_1.setText(QCoreApplication.translate(
            "MainWindow", u"Drone 1", None))
        self.goto_2.setText(QCoreApplication.translate(
            "MainWindow", u"Drone 2", None))
        self.goto_3.setText(QCoreApplication.translate(
            "MainWindow", u"Drone 3", None))
        self.goto_4.setText(QCoreApplication.translate(
            "MainWindow", u"Drone 4", None))
        self.goto_5.setText(QCoreApplication.translate(
            "MainWindow", u"Drone 5", None))
        self.goto_6.setText(QCoreApplication.translate(
            "MainWindow", u"Drone 6", None))
        self.goto_all.setText(
            QCoreApplication.translate("MainWindow", u"ALL", None))
        self.label_28.setText(QCoreApplication.translate(
            "MainWindow", u"GO TO:", None))
        self.connect_all.setText(QCoreApplication.translate(
            "MainWindow", u"Connect all", None))
        self.arm_all.setText(QCoreApplication.translate(
            "MainWindow", u"Arm all", None))
        self.take_off_all.setText(QCoreApplication.translate(
            "MainWindow", u"Take off all", None))
        self.land_all.setText(QCoreApplication.translate(
            "MainWindow", u"Land all", None))
        self.RTL_all_2.setText(QCoreApplication.translate(
            "MainWindow", u"RTL all", None))
        self.mission_all.setText(QCoreApplication.translate(
            "MainWindow", u"Mission all", None))
        self.pause_all_2.setText(QCoreApplication.translate(
            "MainWindow", u"Pause all", None))
        self.label_drone_11.setText(
            QCoreApplication.translate("MainWindow", u"UAV 1", None))
        self.label_drone_12.setText(QCoreApplication.translate(
            "MainWindow", u"Camera UAV 1", None))
        self.connect_drone_1.setText(QCoreApplication.translate(
            "MainWindow", u"Connect drone 1", None))
        self.arm_drone_1.setText(
            QCoreApplication.translate("MainWindow", u"Arm", None))
        self.disarm_drone_1.setText(
            QCoreApplication.translate("MainWindow", u"Disarm", None))
        self.waiting_connect_1.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.arm_or_disarm_drone1.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Altitude:</span></p></body></html>", None))
        self.take_off_drone_1.setText(
            QCoreApplication.translate("MainWindow", u"Take off", None))
        self.change_altitude_drone1.setText(
            QCoreApplication.translate("MainWindow", u"Change altitude", None))
        self.land_drone_1.setText(
            QCoreApplication.translate("MainWindow", u"Land", None))
        self.label_5.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Yaw:</span></p></body></html>", None))
        self.change_yaw_drone_1.setText(
            QCoreApplication.translate("MainWindow", u"Change yaw", None))
        self.Monitor_drone_1.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone1's Camera", None))
        self.mission_1.setText(QCoreApplication.translate(
            "MainWindow", u"MISSION", None))
        self.pause_uav_1.setText(
            QCoreApplication.translate("MainWindow", u"PAUSE", None))
        self.return_and_land_drone_1.setText(
            QCoreApplication.translate("MainWindow", u"RTL", None))
        self.label_6.setText(QCoreApplication.translate(
            "MainWindow", u"Arm Status", None))
        self.ArmStatus_uav1.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_12.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (Rel)", None))
        self.Alt_Rel_uav1.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_15.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. V.", None))
        self.Batt_V_uav1.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_17.setText(QCoreApplication.translate(
            "MainWindow", u"GPS Fix", None))
        self.GPS_Fix_uav1.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_21.setText(QCoreApplication.translate(
            "MainWindow", u"Mode", None))
        self.Mode_uav1.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_23.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (MSL)", None))
        self.Alt_MSL_uav1.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_27.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. Rem.", None))
        self.Batt_Rem_uav1.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_29.setText(QCoreApplication.translate(
            "MainWindow", u"Sat. Num.", None))
        self.Sat_Num_uav1.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_44.setText(QCoreApplication.translate(
            "MainWindow", u"Longitude", None))
        self.longitude_uav1.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_46.setText(QCoreApplication.translate(
            "MainWindow", u"Latitude", None))
        self.latitude_uav1.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.drone.setTabText(self.drone.indexOf(
            self.tab), QCoreApplication.translate("MainWindow", u"Drone 1", None))
        self.label_drone_13.setText(
            QCoreApplication.translate("MainWindow", u"UAV 2", None))
        self.connect_drone_2.setText(QCoreApplication.translate(
            "MainWindow", u"Connect drone 2", None))
        self.arm_drone_2.setText(
            QCoreApplication.translate("MainWindow", u"Arm", None))
        self.disarm_drone_2.setText(
            QCoreApplication.translate("MainWindow", u"Disarm", None))
        self.waiting_connect_2.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.arm_or_disarm_drone2.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Altitude:</span></p></body></html>", None))
        self.take_off_drone_2.setText(
            QCoreApplication.translate("MainWindow", u"Take off", None))
        self.change_altitude_drone2.setText(
            QCoreApplication.translate("MainWindow", u"Change altitude", None))
        self.land_drone_2.setText(
            QCoreApplication.translate("MainWindow", u"Land", None))
        self.label_14.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Yaw:</span></p></body></html>", None))
        self.change_yaw_drone_2.setText(
            QCoreApplication.translate("MainWindow", u"Change yaw", None))
        self.label_drone_14.setText(QCoreApplication.translate(
            "MainWindow", u"Camera UAV 2", None))
        self.Monitor_drone_2.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone2's Camera", None))
        self.mission_2.setText(QCoreApplication.translate(
            "MainWindow", u"MISSION", None))
        self.pause_uav_2.setText(
            QCoreApplication.translate("MainWindow", u"PAUSE", None))
        self.return_and_land_drone_2.setText(
            QCoreApplication.translate("MainWindow", u"RTL", None))
        self.label_94.setText(QCoreApplication.translate(
            "MainWindow", u"Arm Status", None))
        self.ArmStatus_uav2.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_95.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (Rel)", None))
        self.Alt_Rel_uav2.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_96.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. V.", None))
        self.Batt_V_uav2.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_97.setText(QCoreApplication.translate(
            "MainWindow", u"GPS Fix", None))
        self.GPS_Fix_uav2.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_98.setText(QCoreApplication.translate(
            "MainWindow", u"Mode", None))
        self.Mode_uav2.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_99.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (MSL)", None))
        self.Alt_MSL_uav2.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_100.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. Rem.", None))
        self.Batt_Rem_uav2.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_101.setText(QCoreApplication.translate(
            "MainWindow", u"Sat. Num.", None))
        self.Sat_Num_uav2.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_102.setText(QCoreApplication.translate(
            "MainWindow", u"Longitude", None))
        self.longitude_uav2.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_103.setText(QCoreApplication.translate(
            "MainWindow", u"Latitude", None))
        self.latitude_uav2.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.drone.setTabText(self.drone.indexOf(
            self.widget), QCoreApplication.translate("MainWindow", u"Drone 2", None))
        self.label_drone_15.setText(
            QCoreApplication.translate("MainWindow", u"UAV 3", None))
        self.connect_drone_3.setText(QCoreApplication.translate(
            "MainWindow", u"Connect drone 3", None))
        self.arm_drone_3.setText(
            QCoreApplication.translate("MainWindow", u"Arm", None))
        self.disarm_drone_3.setText(
            QCoreApplication.translate("MainWindow", u"Disarm", None))
        self.waiting_connect_3.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.arm_or_disarm_drone3.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.label_19.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Altitude:</span></p></body></html>", None))
        self.take_off_drone_3.setText(
            QCoreApplication.translate("MainWindow", u"Take off", None))
        self.change_altitude_drone3.setText(
            QCoreApplication.translate("MainWindow", u"Change altitude", None))
        self.land_drone_3.setText(
            QCoreApplication.translate("MainWindow", u"Land", None))
        self.label_20.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Yaw:</span></p></body></html>", None))
        self.change_yaw_drone_3.setText(
            QCoreApplication.translate("MainWindow", u"Change yaw", None))
        self.label_drone_16.setText(QCoreApplication.translate(
            "MainWindow", u"Camera UAV 3", None))
        self.Monitor_drone_3.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone3's Camera", None))
        self.mission_3.setText(QCoreApplication.translate(
            "MainWindow", u"MISSION", None))
        self.pause_uav_3.setText(
            QCoreApplication.translate("MainWindow", u"PAUSE", None))
        self.return_and_land_drone_3.setText(
            QCoreApplication.translate("MainWindow", u"RTL", None))
        self.label_104.setText(QCoreApplication.translate(
            "MainWindow", u"Arm Status", None))
        self.ArmStatus_uav3.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_105.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (Rel)", None))
        self.Alt_Rel_uav3.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_106.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. V.", None))
        self.Batt_V_uav3.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_107.setText(QCoreApplication.translate(
            "MainWindow", u"GPS Fix", None))
        self.GPS_Fix_uav3.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_108.setText(
            QCoreApplication.translate("MainWindow", u"Mode", None))
        self.Mode_uav3.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_109.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (MSL)", None))
        self.Alt_MSL_uav3.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_110.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. Rem.", None))
        self.Batt_Rem_uav3.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_111.setText(QCoreApplication.translate(
            "MainWindow", u"Sat. Num.", None))
        self.Sat_Num_uav3.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_112.setText(QCoreApplication.translate(
            "MainWindow", u"Longitude", None))
        self.longitude_uav3.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_113.setText(QCoreApplication.translate(
            "MainWindow", u"Latitude", None))
        self.latitude_uav3.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.drone.setTabText(self.drone.indexOf(
            self.tab_3), QCoreApplication.translate("MainWindow", u"Drone 3", None))
        self.label_drone_17.setText(
            QCoreApplication.translate("MainWindow", u"UAV 4", None))
        self.connect_drone_4.setText(QCoreApplication.translate(
            "MainWindow", u"Connect drone 4", None))
        self.arm_drone_4.setText(
            QCoreApplication.translate("MainWindow", u"Arm", None))
        self.disarm_drone_4.setText(
            QCoreApplication.translate("MainWindow", u"Disarm", None))
        self.waiting_connect_4.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.arm_or_disarm_drone4.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.label_25.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Altitude:</span></p></body></html>", None))
        self.take_off_drone_4.setText(
            QCoreApplication.translate("MainWindow", u"Take off", None))
        self.change_altitude_drone4.setText(
            QCoreApplication.translate("MainWindow", u"Change altitude", None))
        self.land_drone_4.setText(
            QCoreApplication.translate("MainWindow", u"Land", None))
        self.label_26.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Yaw:</span></p></body></html>", None))
        self.change_yaw_drone_4.setText(
            QCoreApplication.translate("MainWindow", u"Change yaw", None))
        self.label_drone_18.setText(QCoreApplication.translate(
            "MainWindow", u"Camera UAV 4", None))
        self.Monitor_drone_4.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone4's Camera", None))
        self.mission_4.setText(QCoreApplication.translate(
            "MainWindow", u"MISSION", None))
        self.pause_uav_4.setText(
            QCoreApplication.translate("MainWindow", u"PAUSE", None))
        self.return_and_land_drone_4.setText(
            QCoreApplication.translate("MainWindow", u"RTL", None))
        self.label_114.setText(QCoreApplication.translate(
            "MainWindow", u"Arm Status", None))
        self.ArmStatus_uav4.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_115.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (Rel)", None))
        self.Alt_Rel_uav4.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_116.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. V.", None))
        self.Batt_V_uav4.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_117.setText(QCoreApplication.translate(
            "MainWindow", u"GPS Fix", None))
        self.GPS_Fix_uav4.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_118.setText(
            QCoreApplication.translate("MainWindow", u"Mode", None))
        self.Mode_uav4.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_119.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (MSL)", None))
        self.Alt_MSL_uav4.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_120.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. Rem.", None))
        self.Batt_Rem_uav4.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_121.setText(QCoreApplication.translate(
            "MainWindow", u"Sat. Num.", None))
        self.Sat_Num_uav4.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_122.setText(QCoreApplication.translate(
            "MainWindow", u"Longitude", None))
        self.longitude_uav4.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_123.setText(QCoreApplication.translate(
            "MainWindow", u"Latitude", None))
        self.latitude_uav4.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.drone.setTabText(self.drone.indexOf(
            self.tab_4), QCoreApplication.translate("MainWindow", u"Drone 4", None))
        self.label_drone_25.setText(
            QCoreApplication.translate("MainWindow", u"UAV 5", None))
        self.connect_drone_5.setText(QCoreApplication.translate(
            "MainWindow", u"Connect drone 5", None))
        self.waiting_connect_5.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.arm_drone_5.setText(
            QCoreApplication.translate("MainWindow", u"Arm", None))
        self.disarm_drone_5.setText(
            QCoreApplication.translate("MainWindow", u"Disarm", None))
        self.arm_or_disarm_drone5.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.label_42.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Altitude:</span></p></body></html>", None))
        self.take_off_drone_5.setText(
            QCoreApplication.translate("MainWindow", u"Take off", None))
        self.change_altitude_drone5.setText(
            QCoreApplication.translate("MainWindow", u"Change altitude", None))
        self.land_drone_5.setText(
            QCoreApplication.translate("MainWindow", u"Land", None))
        self.label_43.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Yaw:</span></p></body></html>", None))
        self.change_yaw_drone_5.setText(
            QCoreApplication.translate("MainWindow", u"Change yaw", None))
        self.label_drone_26.setText(QCoreApplication.translate(
            "MainWindow", u"Camera UAV 5", None))
        self.Monitor_drone_5.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone6's Camera", None))
        self.mission_5.setText(QCoreApplication.translate(
            "MainWindow", u"MISSION", None))
        self.pause_uav_5.setText(
            QCoreApplication.translate("MainWindow", u"PAUSE", None))
        self.return_and_land_drone_5.setText(
            QCoreApplication.translate("MainWindow", u"RTL", None))
        self.label_124.setText(QCoreApplication.translate(
            "MainWindow", u"Arm Status", None))
        self.ArmStatus_uav5.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_125.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (Rel)", None))
        self.Alt_Rel_uav5.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_126.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. V.", None))
        self.Batt_V_uav5.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_127.setText(QCoreApplication.translate(
            "MainWindow", u"GPS Fix", None))
        self.GPS_Fix_uav5.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_128.setText(
            QCoreApplication.translate("MainWindow", u"Mode", None))
        self.Mode_uav5.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_129.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (MSL)", None))
        self.Alt_MSL_uav5.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_130.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. Rem.", None))
        self.Batt_Rem_uav5.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_131.setText(QCoreApplication.translate(
            "MainWindow", u"Sat. Num.", None))
        self.Sat_Num_uav5.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_132.setText(QCoreApplication.translate(
            "MainWindow", u"Longitude", None))
        self.longitude_uav5.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_133.setText(QCoreApplication.translate(
            "MainWindow", u"Latitude", None))
        self.latitude_uav5.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.drone.setTabText(self.drone.indexOf(
            self.tab_5), QCoreApplication.translate("MainWindow", u"Drone 5", None))
        self.label_drone_39.setText(
            QCoreApplication.translate("MainWindow", u"UAV 6", None))
        self.connect_drone_6.setText(QCoreApplication.translate(
            "MainWindow", u"Connect drone 6", None))
        self.waiting_connect_6.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.arm_drone_6.setText(
            QCoreApplication.translate("MainWindow", u"Arm", None))
        self.disarm_drone_6.setText(
            QCoreApplication.translate("MainWindow", u"Disarm", None))
        self.arm_or_disarm_drone6.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; color:#ff0000;\">Waiting...</span></p></body></html>", None))
        self.label_77.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Altitude:</span></p></body></html>", None))
        self.take_off_drone_6.setText(
            QCoreApplication.translate("MainWindow", u"Take off", None))
        self.change_altitude_drone6.setText(
            QCoreApplication.translate("MainWindow", u"Change altitude", None))
        self.land_drone_6.setText(
            QCoreApplication.translate("MainWindow", u"Land", None))
        self.label_78.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Desired Yaw:</span></p></body></html>", None))
        self.change_yaw_drone_6.setText(
            QCoreApplication.translate("MainWindow", u"Change yaw", None))
        self.label_drone_40.setText(QCoreApplication.translate(
            "MainWindow", u"Camera UAV 6", None))
        self.Monitor_drone_6.setText(QCoreApplication.translate(
            "MainWindow", u"Waiting Signal from Drone5's Camera", None))
        self.mission_6.setText(QCoreApplication.translate(
            "MainWindow", u"MISSION", None))
        self.pause_uav_6.setText(
            QCoreApplication.translate("MainWindow", u"PAUSE", None))
        self.return_and_land_drone_6.setText(
            QCoreApplication.translate("MainWindow", u"RTL", None))
        self.label_134.setText(QCoreApplication.translate(
            "MainWindow", u"Arm Status", None))
        self.ArmStatus_uav6.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_135.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (Rel)", None))
        self.Alt_Rel_uav6.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_136.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. V.", None))
        self.Batt_V_uav6.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_137.setText(QCoreApplication.translate(
            "MainWindow", u"GPS Fix", None))
        self.GPS_Fix_uav6.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_138.setText(
            QCoreApplication.translate("MainWindow", u"Mode", None))
        self.Mode_uav6.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_139.setText(QCoreApplication.translate(
            "MainWindow", u"Alt (MSL)", None))
        self.Alt_MSL_uav6.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_140.setText(QCoreApplication.translate(
            "MainWindow", u"Batt. Rem.", None))
        self.Batt_Rem_uav6.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_141.setText(QCoreApplication.translate(
            "MainWindow", u"Sat. Num.", None))
        self.Sat_Num_uav6.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.label_142.setText(QCoreApplication.translate(
            "MainWindow", u"Longitude", None))
        self.longitude_uav6.setText(
            QCoreApplication.translate("MainWindow", u"---------", None))
        self.label_143.setText(QCoreApplication.translate(
            "MainWindow", u"Latitude", None))
        self.latitude_uav6.setText(QCoreApplication.translate(
            "MainWindow", u"---------", None))
        self.drone.setTabText(self.drone.indexOf(
            self.tab_6), QCoreApplication.translate("MainWindow", u"Drone 6", None))
    # retranslateUi
