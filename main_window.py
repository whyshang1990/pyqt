# -*- coding: UTF-8 -*-
"""主窗口类"""
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget

from central_widget import CentralWidget
from utils import loggers

LOGGER = loggers.get_logger("main_window")


class MainWindow(QMainWindow):
    """应用程序主窗口"""
    def __init__(self):
        LOGGER.debug("主窗口初始化")
        super().__init__()
        self.menu_bar = self.init_menubar()
        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)

        self.init_style()

    def init_style(self):
        self.setWindowTitle("记账日志")
        self.setGeometry(0, 0, 1366, 768)
        self.setMinimumWidth(300)
        self.center()

    def center(self):
        """
        使用自身和桌面屏幕的geometry，使mainWindow移动到屏幕中心
        """
        s_size = self.geometry()
        screen = QDesktopWidget().screenGeometry()
        LOGGER.debug("桌面分辨率: width[%s]-height[%s]", screen.width(), screen.height())
        self.move((screen.width() - s_size.width()) / 2, (screen.height() - s_size.height()) / 2)

    def init_menubar(self):
        """菜单栏初始化"""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("New File")
        return menu_bar
