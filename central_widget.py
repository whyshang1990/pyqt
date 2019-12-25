from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QFormLayout, \
    QLineEdit, QCalendarWidget, QMessageBox

from db import db_tools
from utils import loggers

logger = loggers.get_logger("central_widget")


class CentralWidget(QWidget):
    """主窗口中心控件"""
    def __init__(self):
        logger.debug("主窗口中心控件初始化")
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
        logger.debug("主窗口导航控件初始化")
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
        logger.debug("主窗口主页控件初始化")
        super().__init__()
        self.create_btn = QPushButton("创建交易")
        self.init_ui()
        self.cw = CreateWidget()
        self.create_btn.clicked.connect(self.cw.show)

    def init_ui(self):
        layout = QVBoxLayout()

        create = QHBoxLayout()
        create.addStretch(1)
        create.addWidget(self.create_btn)
        recent_transaction = QGroupBox("最近交易")
        total = QGroupBox("交易总计")

        layout.addLayout(create)
        layout.addWidget(recent_transaction)
        layout.addWidget(total)

        self.setLayout(layout)

    @pyqtSlot()
    def open_created_widget(self):
        self.cw.show()
        logger.debug("test")


class CreateWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setWindowTitle("创建交易")
        self.layout = QVBoxLayout()
        self.init_ui()
        self.setLayout(self.layout)

    def init_ui(self):
        # 创建表单布局
        form_layout = QFormLayout()

        amount_edit = QLineEdit()
        type_edit = QLineEdit()
        remarks_edit = QLineEdit()
        date_edit = QCalendarWidget()

        form_layout.addRow("Amount", amount_edit)
        form_layout.addRow("Type", type_edit)
        form_layout.addRow("Remarks", remarks_edit)
        form_layout.addRow("date", date_edit)

        remarks_edit.setPlaceholderText("添加备注信息")

        # 创建按钮布局
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        btn_layout.addStretch(1)
        btn_layout.addWidget(save_btn)
        s = amount_edit.text()
        logger.debug("s: %s", type)
        save_btn.clicked.connect(lambda: self.save(amount_edit.text()))

        self.layout.addLayout(form_layout)
        self.layout.addLayout(btn_layout)

    @pyqtSlot(str)
    def save(self, cost):
        try:
            logger.debug("cost: %f", float(cost))
            db_tools.insert_into(cost)
        except ValueError as e:
            logger.debug(repr(e))
            tips = QMessageBox()
            tips.warning(self, '输入错误', '警告框消息正文', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
