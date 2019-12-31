# -*- coding: UTF-8 -*-
"""中心窗口模块"""
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from utils import loggers
from widgets.home_page import HomeWidget

LOGGER = loggers.get_logger("central_widget")


class CentralWidget(QWidget):
    """主窗口中心控件"""
    def __init__(self):
        LOGGER.debug("主窗口中心控件初始化")
        super().__init__()
        self.layout = QHBoxLayout()
        self.left = NavigateWidget()
        self.right = HomeWidget()
        self.layout = self._init_layout()

        self.setLayout(self.layout)

    def _init_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.left)
        layout.addWidget(self.right)
        # 设置两个控件的拉伸系数
        layout.setStretchFactor(self.left, 1)
        layout.setStretchFactor(self.right, 4)
        return layout


class NavigateWidget(QWidget):
    """导航控件"""
    def __init__(self):
        LOGGER.debug("主窗口导航控件初始化")
        super().__init__()
        self.home = QPushButton("主页")
        self.acct_book = QPushButton("账本")
        self.statistics = QPushButton("统计")
        self.layout = self._init_layout()

        self.setLayout(self.layout)

    def _init_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.home)
        layout.addWidget(self.acct_book)
        layout.addWidget(self.statistics)
        layout.addStretch(1)
        return layout
