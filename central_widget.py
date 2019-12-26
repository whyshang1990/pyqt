from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QFormLayout, \
    QLineEdit, QCalendarWidget, QMessageBox, QTableView

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

        self.cw_widget = CreateWidget()
        self.rt_widget = RecentTrans("最近交易")
        self.tt_widget = QGroupBox("交易总计")
        self.layout = QVBoxLayout()

        self.init_ui()
        self.create_btn.clicked.connect(self.cw_widget.show)
        self.cw_widget.refresh_tb_signal.connect(self.rt_widget.init_query_model)
        # self.cw_widget.refresh_tb_signal.connect(self.rt_widget.refresh_table)

    @pyqtSlot()
    def init_ui(self):
        create_layout = QHBoxLayout()
        create_layout.addStretch(1)
        create_layout.addWidget(self.create_btn)

        self.layout.addLayout(create_layout)
        self.layout.addWidget(self.rt_widget)
        self.layout.addWidget(self.tt_widget)

        self.setLayout(self.layout)


class CreateWidget(QWidget):
    """
    创建控件界面
    """
    # 初始化信号
    refresh_tb_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # 页面文本输入框
        self.amount_edit = QLineEdit()
        self.type_edit = QLineEdit()
        self.remarks_edit = QLineEdit()
        self.date_edit = QCalendarWidget()
        self.save_btn = QPushButton("Save")
        # 页面顶层布局
        self.layout = QVBoxLayout()

        # 开始初始化
        self.init_ui()
        self.set_ui_style()
        self.signal_conn_slot()

        self.setLayout(self.layout)
        self.resize(400, 400)
        self.setWindowTitle("创建交易")

    def init_ui(self):
        # 创建子布局1
        form_layout = QFormLayout()
        form_layout.addRow("Amount", self.amount_edit)
        form_layout.addRow("Type", self.type_edit)
        form_layout.addRow("Remarks", self.remarks_edit)
        form_layout.addRow("date", self.date_edit)

        # 创建子布局2
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.save_btn)

        self.layout.addLayout(form_layout)
        self.layout.addLayout(btn_layout)

    def set_ui_style(self):
        """
        设置CreateWidget页面样式
        """
        # logger.debug("设置CreateWidget页面样式")
        self.remarks_edit.setPlaceholderText("添加备注信息")
        self.save_btn.setEnabled(False)

    def signal_conn_slot(self):
        """
        连接信号与槽
        """
        # logger.debug("CreateWidget：连接信号与槽")
        # save按钮
        amount_edit_text = self.amount_edit.text()
        logger.debug("amount_edit_text: %s", amount_edit_text)
        self.save_btn.clicked.connect(lambda: self.save())
        # save按钮是否激活
        self.amount_edit.textChanged.connect(self.check_save_disable)
        self.type_edit.textChanged.connect(self.check_save_disable)

    @pyqtSlot()
    def save(self):
        """save按钮槽函数"""
        try:
            params_dict = {
                "cost": self.amount_edit.text(),
                "trans_type": self.type_edit.text()
            }
            db_tools.insert_into("tb_transactions", params_dict)
            self.refresh_tb_signal.emit()
            self.close()
        except ValueError as e:
            logger.debug(repr(e))
            tips = QMessageBox()
            tips.warning(self, '输入错误', '警告框消息正文', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    @pyqtSlot()
    def check_save_disable(self):
        """save按钮是否激活槽函数"""
        logger.debug("amount_changed: %s", self.amount_edit.text())
        if self.type_edit.text() and self.amount_edit.text():
            self.save_btn.setEnabled(True)
        else:
            self.save_btn.setEnabled(False)


class RecentTrans(QGroupBox):
    """
    最近交易控件
    """
    def __init__(self, name):
        super().__init__(name)
        self.layout = QHBoxLayout()
        self.table_view = QTableView()
        self.query_model = QSqlQueryModel(parent=self)

        self.init_query_model()
        self.init_ui()
        self.setMaximumSize(600, 277)

    def init_ui(self):
        self.table_view.setModel(self.query_model)
        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)

    @pyqtSlot()
    def init_query_model(self):
        """表格刷新"""
        logger.debug("表格刷新")
        self.query_model.setQuery("select cost,trans_type from tb_transactions LIMIT 7")
        self.query_model.setHeaderData(0, Qt.Horizontal, '金额')
        self.query_model.setHeaderData(1, Qt.Horizontal, '分类')
