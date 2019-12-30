# -*- coding: utf-8 -*-
"""交易总计控件"""
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QLabel, QHBoxLayout

from utils import loggers
from utils.constants import Constants

LOGGER = loggers.get_logger("total_trans")


class TotalTrans(QListWidget):
    """交易总计控件"""
    def __init__(self):
        super().__init__()
        # 根据今天日期获取本周，本月，本年的日期范围
        self.today = QDate().currentDate()
        self.first_day_of_week = QDate(self.today.addDays(1 - self.today.dayOfWeek()))
        self.last_day_of_week = QDate(self.today.addDays(7 - self.today.dayOfWeek()))
        self.first_day_of_month = QDate(self.today.year(), self.today.month(), 1)
        self.last_day_of_month = QDate(self.today.year(), self.today.month(), self.today.daysInMonth())
        self.first_day_of_year = QDate(self.today.year(), 1, 1)
        self.last_day_of_year = QDate(self.today.year(), 12, 31)

        date_format = "M月d日"
        today_income = self.__get_total("today", Constants.TRANS_TYPE["income"])
        today_expend = self.__get_total("today", Constants.TRANS_TYPE["expand"])
        week_income = self.__get_total("week", Constants.TRANS_TYPE["income"])
        week_expand = self.__get_total("week", Constants.TRANS_TYPE["expand"])
        month_income = self.__get_total("month", Constants.TRANS_TYPE["income"])
        month_expand = self.__get_total("month", Constants.TRANS_TYPE["expand"])
        year_income = self.__get_total("year", Constants.TRANS_TYPE["income"])
        year_expand = self.__get_total("year", Constants.TRANS_TYPE["expand"])
        self.today_widget = self._RowWidget("本日", self.today.toString(date_format), today_income, today_expend)
        self.week_widget = self._RowWidget("本周", self.first_day_of_week.toString(date_format) + " - " +
                                           self.last_day_of_week.toString(date_format), week_income, week_expand)
        self.month_widget = self._RowWidget("本月", self.first_day_of_month.toString(date_format) + " - " +
                                            self.last_day_of_month.toString(date_format), month_income, month_expand)
        self.year_widget = self._RowWidget("本年", self.first_day_of_year.toString(date_format) + " - " +
                                           self.last_day_of_year.toString(date_format), year_income, year_expand)

        self.layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.layout.addWidget(self.today_widget)
        self.layout.addWidget(self.week_widget)
        self.layout.addWidget(self.month_widget)
        self.layout.addWidget(self.year_widget)

        self.setLayout(self.layout)

    def __get_total(self, time_type, trans_type):
        choice = {
            "today": (self.today, self.today),
            "week": (self.first_day_of_week, self.last_day_of_week),
            "month": (self.first_day_of_month, self.last_day_of_month),
            "year": (self.first_day_of_year, self.last_day_of_year)
        }
        start_day, end_day = choice.get(time_type)
        sql = "select sum(cost) as sum from tb_transactions where create_date >= '{}' and create_date <= '{}' " \
              "and trans_type = {};".format(start_day.toString(Qt.ISODate), end_day.toString(Qt.ISODate), trans_type)
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

    class _RowWidget(QListWidget):
        def __init__(self, summary, details, income, expend):
            super().__init__()
            self.layout = QHBoxLayout()
            self.summary_label = QLabel(summary + "(" + details + ")", self)
            self.income_label = QLabel("总收入：{:.2f}".format(income), self)
            self.expend_label = QLabel("总支出：{:.2f}".format(expend), self)

            self.init_ui()

        def init_ui(self):
            self.layout.addWidget(self.summary_label)
            self.layout.addWidget(self.income_label)
            self.layout.addWidget(self.expend_label)

            self.setLayout(self.layout)
