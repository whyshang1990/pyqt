# -*- coding: UTF-8 -*-
"""中心窗口模块"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel

from utils import loggers
from widgets.home_page import TotalTrans, CreateWidget, RecentTrans

LOGGER = loggers.get_logger("central_widget")


class CentralWidget(QWidget):
    """主窗口中心控件"""
    def __init__(self):
        LOGGER.debug("主窗口中心控件初始化")
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        left = NavigateWidget()
        right = HomeWidget()
        layout.addWidget(left)
        layout.addWidget(right)

        # 设置两个控件的拉伸系数
        layout.setStretchFactor(left, 1)
        layout.setStretchFactor(right, 4)

        self.setLayout(layout)


class NavigateWidget(QWidget):
    """导航控件"""
    def __init__(self):
        LOGGER.debug("主窗口导航控件初始化")
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        home = QPushButton("主页")
        acct_book = QPushButton("账本")
        statistics = QPushButton("统计")
        layout.addWidget(home)
        layout.addWidget(acct_book)
        layout.addWidget(statistics)
        layout.addStretch(1)

        self.setLayout(layout)


class HomeWidget(QWidget):
    """主页展示控件"""
    def __init__(self):
        LOGGER.debug("主窗口主页控件初始化")
        super().__init__()
        self.create_btn = QPushButton("创建交易")

        self.cw_widget = CreateWidget()
        self.rt_widget = RecentTrans("最近交易")
        self.tt_widget_title = QLabel("交易总计")
        self.tt_widget = TotalTrans()
        self.layout = QVBoxLayout()

        self.init_ui()
        self.create_btn.clicked.connect(self.cw_widget.show)
        # 绑定保存按钮信号到槽（刷新页面）
        self.cw_widget.save_signal.connect(self.update_data)

    @pyqtSlot()
    def init_ui(self):
        create_layout = QHBoxLayout()
        create_layout.addStretch(1)
        create_layout.addWidget(self.create_btn)

        self.layout.addLayout(create_layout)
        self.layout.addWidget(self.rt_widget)
        self.layout.addWidget(self.tt_widget_title)
        self.layout.addWidget(self.tt_widget)

        self.setLayout(self.layout)

    @pyqtSlot()
    def update_data(self):
        """更新控件显示内容"""
        self.rt_widget.model.refresh_model()
        self.tt_widget.update_cost()
