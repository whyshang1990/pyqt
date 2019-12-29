# -*- coding: utf-8 -*-
"""交易总计控件"""
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QGridLayout, QGroupBox

from utils import loggers
from utils.constants import Constants
from widgets.general_widgets import BaseWidget

LOGGER = loggers.get_logger("total_trans")


class TotalTrans(QGroupBox):
    """交易总计控件"""
    def __init__(self, name):
        super().__init__(name)
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
        self.today_widget = BaseWidget("今日", "总收入：{:.2f}".format(today_income),
                                       self.today.toString(date_format), "总支出： {:.2f}".format(today_expend))
        self.week_widget = BaseWidget("本周", "总收入：{:.2f}".format(week_income),
                                      self.first_day_of_week.toString(date_format) + " - " +
                                      self.last_day_of_week.toString(date_format),
                                      "总支出： {:.2f}".format(week_expand))
        self.month_widget = BaseWidget("本月", "总收入：{:.2f}".format(month_income),
                                       self.first_day_of_month.toString(date_format) + " - " +
                                       self.last_day_of_month.toString(date_format),
                                       "总支出： {:.2f}".format(month_expand))
        self.year_widget = BaseWidget("本年", "总收入：{:.2f}".format(year_income),
                                      self.first_day_of_year.toString(date_format) + " - " +
                                      self.last_day_of_year.toString(date_format),
                                      "总支出： {:.2f}".format(year_expand))

        self.layout = QGridLayout()
        self.init_ui()

    def init_ui(self):
        self.layout.setSpacing(1)
        self.layout.addWidget(self.today_widget, 1, 0)
        self.layout.addWidget(self.week_widget, 1, 1)
        self.layout.addWidget(self.month_widget, 2, 0)
        self.layout.addWidget(self.year_widget, 2, 1)

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
