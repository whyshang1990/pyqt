from PyQt5.QtCore import pyqtSlot
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QTableView

from utils import loggers
from utils.constants import Constants

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
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        model = QSqlTableModel()
        model.setTable(Constants.TRANSACTIONS_TABLE)
        # model.setHeaderData(0, Qt.Horizontal, "name")

        table_view = QTableView()
        table_view.setModel(model)

        layout.addWidget(table_view)

        self.setLayout(layout)
