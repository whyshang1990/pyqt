# -*- coding: UTF-8 -*-
"""中心窗口模块"""
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, \
    QFormLayout, QLineEdit, QCalendarWidget, QMessageBox, QTableView, QRadioButton, QComboBox

from db import db_tools
from models.custom_models import MyTableModel
from utils import loggers

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
        self.tt_widget = QGroupBox("交易总计")
        self.layout = QVBoxLayout()

        self.init_ui()
        self.create_btn.clicked.connect(self.cw_widget.show)
        self.cw_widget.refresh_tb_signal.connect(self.rt_widget.model.refresh_model)

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
        self.category_edit = QComboBox()
        self.income_r_btn = QRadioButton("收入", self)
        self.expense_r_btn = QRadioButton("支出", self)
        self.date_edit = QCalendarWidget()
        self.remarks_edit = QLineEdit()
        self.save_btn = QPushButton("Save")
        # 页面顶层布局
        self.layout = QVBoxLayout()

        # 开始初始化
        self.init_type()
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
        form_layout.addRow("Category", self.category_edit)
        # 类型设置单选按钮
        r_btn_layout = QHBoxLayout()
        r_btn_layout.addWidget(self.income_r_btn)
        r_btn_layout.addWidget(self.expense_r_btn)
        form_layout.addRow("Type", r_btn_layout)
        form_layout.addRow("date", self.date_edit)
        form_layout.addRow("Remarks", self.remarks_edit)

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
        self.expense_r_btn.setChecked(True)
        self.remarks_edit.setPlaceholderText("添加备注信息")
        self.save_btn.setEnabled(False)

    def signal_conn_slot(self):
        """
        连接信号与槽
        """
        # logger.debug("CreateWidget：连接信号与槽")
        # save按钮
        self.save_btn.clicked.connect(self.save)
        # save按钮是否激活
        self.amount_edit.textChanged.connect(self.check_save_disable)

    @pyqtSlot()
    def save(self):
        """save按钮槽函数"""
        try:
            date = self.date_edit.selectedDate().toString(Qt.ISODate)
            params_dict = {
                "cost": self.amount_edit.text(),
                "trans_type": self.check_radio_btn(),
                "category": self.category_edit.currentText(),
                "create_date": date
            }
            db_tools.insert_into("tb_transactions", params_dict)
            self.refresh_tb_signal.emit()
            self.close()
        except Exception as exp:
            LOGGER.debug(repr(exp))
            tips = QMessageBox()
            tips.warning(self, '输入错误', '请检查后台日志', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    @pyqtSlot()
    def check_save_disable(self):
        """save按钮是否激活槽函数"""
        if self.amount_edit.text():
            self.save_btn.setEnabled(True)
        else:
            self.save_btn.setEnabled(False)

    def check_radio_btn(self):
        """设定单选按钮返回值"""
        if self.income_r_btn.isChecked():
            return 1
        else:
            return -1

    def init_type(self):
        """初始化分类下拉控件，控件显示内容由数据库获取"""
        query_model = QSqlQueryModel()
        query_model.setQuery("select name from tb_trans_type where level=0;")
        categories = [query_model.record(row).value("name") for row in range(query_model.rowCount())]
        self.category_edit.addItems(categories)
        LOGGER.debug("categories: %s", categories)


class RecentTrans(QGroupBox):
    """
    最近交易控件
    """
    def __init__(self, name):
        super().__init__(name)
        self.layout = QHBoxLayout()
        self.table_view = QTableView()
        self.model = MyTableModel(parent=self)

        self.init_ui()
        self.setMaximumSize(600, 277)

    def init_ui(self):
        self.model.setHeaderData(0, Qt.Horizontal, '金额')
        self.model.setHeaderData(1, Qt.Horizontal, '交易类型')
        self.model.setHeaderData(2, Qt.Horizontal, '分类')
        self.model.setHeaderData(3, Qt.Horizontal, '创建日期')

        self.table_view.verticalHeader().hide()
        self.table_view.setModel(self.model)
        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)
