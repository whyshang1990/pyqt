# -*- coding: utf-8 -*-
"""交易总计控件"""
from PyQt5.QtCore import QDate, Qt, pyqtSlot, pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QLabel, QHBoxLayout, QListView, QGroupBox, QTableView, \
    QMessageBox, QFormLayout, QLineEdit, QWidget, QComboBox, QRadioButton, QCalendarWidget, QPushButton, QButtonGroup

from db import db_tools
from models.custom_models import RecentTransTableModel
from utils import loggers
from utils.constants import Constants

LOGGER = loggers.get_logger("total_trans")
# 日期格式
DATE_FORMAT = "M月d日"


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

        self.create_layout = QHBoxLayout()
        self.create_layout.addStretch(1)
        self.create_layout.addWidget(self.create_btn)

        self.top_layout = self.init_top_layout()

        self.setLayout(self.top_layout)

        self.create_btn.clicked.connect(self.cw_widget.show)
        # 绑定保存按钮信号到槽（刷新页面）
        self.cw_widget.save_signal.connect(self.update_data)

    @pyqtSlot()
    def init_top_layout(self):
        top_layout = QVBoxLayout()
        top_layout.addLayout(self.create_layout)
        top_layout.addWidget(self.rt_widget)
        top_layout.addWidget(self.tt_widget_title)
        top_layout.addWidget(self.tt_widget)
        return top_layout

    @pyqtSlot()
    def update_data(self):
        """更新控件显示内容"""
        self.rt_widget.model.refresh_model()
        self.tt_widget.update_cost()


class TotalTrans(QListView):
    """交易总计控件，显示今日，本周，本月，本年的总收入，总支出"""
    def __init__(self):
        super().__init__()
        # 根据今天日期获取本周，本月，本年的日期范围
        date_params = self._DateParams()
        self.today_widget = self._RowWidget("本日", date_params.today.toString(DATE_FORMAT), date_params.today_income,
                                            date_params.today_expend)
        self.week_widget = self._RowWidget("本周", date_params.first_day_of_week.toString(DATE_FORMAT) + " - " +
                                           date_params.last_day_of_week.toString(DATE_FORMAT), date_params.week_income,
                                           date_params.week_expand)
        self.month_widget = self._RowWidget("本月", date_params.first_day_of_month.toString(DATE_FORMAT) + " - " +
                                            date_params.last_day_of_month.toString(DATE_FORMAT), date_params.month_income,
                                            date_params.month_expand)
        self.year_widget = self._RowWidget("本年", date_params.first_day_of_year.toString(DATE_FORMAT) + " - " +
                                           date_params.last_day_of_year.toString(DATE_FORMAT), date_params.year_income,
                                           date_params.year_expand)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.today_widget)
        self.layout.addWidget(self.week_widget)
        self.layout.addWidget(self.month_widget)
        self.layout.addWidget(self.year_widget)
        self.setLayout(self.layout)

    @pyqtSlot()
    def update_cost(self):
        """刷新页面cost数据"""
        LOGGER.debug("总计页面费用刷新")
        date_params = self._DateParams()
        self.today_widget.update_cost(date_params.today_income, date_params.today_expend)
        self.week_widget.update_cost(date_params.week_income, date_params.week_expand)
        self.month_widget.update_cost(date_params.month_income, date_params.month_expand)
        self.year_widget.update_cost(date_params.year_income, date_params.year_expand)

    class _RowWidget(QListWidget):
        """总计页面子控件，包括3个Label控件用于显示总收入总支出"""
        def __init__(self, summary, details, income, expend):
            super().__init__()
            income = income if income else 0
            expend = expend if expend else 0
            self.summary_label = QLabel(summary + "(" + details + ")", self)
            self.income_label = QLabel("总收入：{:.2f}".format(income), self)
            self.expend_label = QLabel("总支出：{:.2f}".format(expend), self)

            self.layout = QHBoxLayout()
            self.layout.addWidget(self.summary_label)
            self.layout.addWidget(self.income_label)
            self.layout.addWidget(self.expend_label)
            self.setLayout(self.layout)

        def update_cost(self, income, expend):
            """更新控件cost文本信息"""
            self.income_label.setText("总收入：{:.2f}".format(income))
            self.expend_label.setText("总支出：{:.2f}".format(expend))

    class _DateParams(object):
        """日期参数，根据当前日期获取TotalTrans所需的各种参数"""
        def __init__(self):
            self.today = QDate().currentDate()
            self.first_day_of_week = QDate(self.today.addDays(1 - self.today.dayOfWeek()))
            self.last_day_of_week = QDate(self.today.addDays(7 - self.today.dayOfWeek()))
            self.first_day_of_month = QDate(self.today.year(), self.today.month(), 1)
            self.last_day_of_month = QDate(self.today.year(), self.today.month(), self.today.daysInMonth())
            self.first_day_of_year = QDate(self.today.year(), 1, 1)
            self.last_day_of_year = QDate(self.today.year(), 12, 31)

            self.today_income = self.__get_total("today", Constants.TRANS_TYPE["income"])
            self.today_expend = self.__get_total("today", Constants.TRANS_TYPE["expand"])
            self.week_income = self.__get_total("week", Constants.TRANS_TYPE["income"])
            self.week_expand = self.__get_total("week", Constants.TRANS_TYPE["expand"])
            self.month_income = self.__get_total("month", Constants.TRANS_TYPE["income"])
            self.month_expand = self.__get_total("month", Constants.TRANS_TYPE["expand"])
            self.year_income = self.__get_total("year", Constants.TRANS_TYPE["income"])
            self.year_expand = self.__get_total("year", Constants.TRANS_TYPE["expand"])

        def __get_total(self, time_type, trans_type):
            """
            根据传入参数，查询数据库获取总计的收入或者支出
            :param time_type: 时间类型，包括today, week, month, year
            :param trans_type: 交易类型，收入(1)，支出(-1)
            """
            choice = {
                "today": (self.today, self.today),
                "week": (self.first_day_of_week, self.last_day_of_week),
                "month": (self.first_day_of_month, self.last_day_of_month),
                "year": (self.first_day_of_year, self.last_day_of_year)
            }
            start_day, end_day = choice.get(time_type)
            sql = "select sum(cost) as sum from tb_transaction where create_date >= '{}' and create_date <= '{}' " \
                  "and trans_type = {};".format(start_day.toString(Qt.ISODate), end_day.toString(Qt.ISODate),
                                                trans_type)
            # LOGGER.debug("sql: %s", sql)
            query = QSqlQuery(sql)
            # 获取名称为sum列的索引
            rec = query.record().indexOf("sum")
            # QSqlQuery只能获取当前记录区域中的数据，使用next()移动区域
            if query.next():
                # 根据索引获取对应值
                if query.value(rec):
                    return query.value(rec)
                else:
                    return 0


class RecentTrans(QGroupBox):
    """
    最近交易控件
    """
    def __init__(self, name):
        super().__init__(name)
        self.table_view = QTableView()
        self.model = RecentTransTableModel(parent=self)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)

        self.init_ui()


    def init_ui(self):
        self.model.setHeaderData(0, Qt.Horizontal, '金额')
        self.model.setHeaderData(1, Qt.Horizontal, '交易类型')
        self.model.setHeaderData(2, Qt.Horizontal, '分类')
        self.model.setHeaderData(3, Qt.Horizontal, '创建日期')

        self.table_view.verticalHeader().hide()
        self.table_view.setModel(self.model)

        self.setMaximumHeight(277)


class CreateWidget(QWidget):
    """
    创建控件界面
    """
    # save按钮的刷新信号
    save_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # 初始化所有子控件
        self.amount_edit = QLineEdit()
        self.income_r_btn = QRadioButton("收入", self)
        self.expense_r_btn = QRadioButton("支出", self)
        self.category_edit = QComboBox()
        self.date_edit = QCalendarWidget()
        self.remarks_edit = QLineEdit()
        self.save_btn = QPushButton("Save")

        # 初始化样式
        self.set_ui_style()

        # 初始化收入/支出组合按钮
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.expense_r_btn, 1)
        self.button_group.addButton(self.income_r_btn, 2)
        self.init_type()

        self.setLayout(self.init_top_layout())
        self.signal_conn_slot()

    def init_top_layout(self):
        top_layout = QVBoxLayout()
        # 创建子布局1
        form_layout = QFormLayout()
        form_layout.addRow("Amount", self.amount_edit)
        # 类型设置单选按钮
        r_btn_layout = QHBoxLayout()
        r_btn_layout.addWidget(self.income_r_btn)
        r_btn_layout.addWidget(self.expense_r_btn)
        form_layout.addRow("Type", r_btn_layout)

        form_layout.addRow("Category", self.category_edit)
        form_layout.addRow("date", self.date_edit)
        form_layout.addRow("Remarks", self.remarks_edit)

        # 创建子布局2
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.save_btn)

        top_layout.addLayout(form_layout)
        top_layout.addLayout(btn_layout)
        return top_layout

    def set_ui_style(self):
        """
        设置CreateWidget页面样式
        """
        # logger.debug("设置CreateWidget页面样式")
        self.expense_r_btn.setChecked(True)
        self.remarks_edit.setPlaceholderText("添加备注信息")
        self.save_btn.setEnabled(False)

        self.resize(300, 400)
        self.setWindowTitle("创建交易")

    def signal_conn_slot(self):
        """
        连接信号与槽
        """
        # save按钮
        self.save_btn.clicked.connect(self.save)
        # save按钮是否激活
        self.amount_edit.textChanged.connect(self.check_save_disable)
        self.button_group.buttonClicked.connect(self.init_type)

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
            db_tools.insert_into("tb_transaction", params_dict)
            self.save_signal.emit()
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
            return 2
        else:
            return 1

    @pyqtSlot()
    def init_type(self):
        """初始化分类下拉控件，控件显示内容由数据库获取"""
        self.category_edit.clear()
        checked_id = self.button_group.checkedId()
        LOGGER.debug("trans_type: %s", checked_id)
        query_model = QSqlQueryModel()
        query_model.setQuery("select name from tb_category where level=0 and trans_type={};".format(checked_id))
        categories = [query_model.record(row).value("name") for row in range(query_model.rowCount())]
        LOGGER.debug("categories: %s", categories)
        # for category in categories:
        self.category_edit.addItems(categories)
