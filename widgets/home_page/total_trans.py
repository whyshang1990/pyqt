# -*- coding: utf-8 -*-
"""交易总计控件"""
import calendar
from datetime import datetime, date

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QGridLayout, QGroupBox

from utils import loggers
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
        self.today_widget = BaseWidget("今日", "2", self.today.toString(date_format), "4")
        self.week_widget = BaseWidget("本周", "100", self.first_day_of_week.toString(date_format) + " - " +
                                      self.last_day_of_week.toString(date_format), "总计")
        self.month_widget = BaseWidget("本月", "200", self.first_day_of_month.toString(date_format) + " - " +
                                       self.last_day_of_month.toString(date_format), "总计")
        self.year_widget = BaseWidget("本年", "300",  self.first_day_of_year.toString(date_format) + " - " +
                                      self.last_day_of_year.toString(date_format), "总计")

        self.layout = QGridLayout()
        self.init_ui()

    def init_ui(self):
        self.layout.setSpacing(1)
        self.layout.addWidget(self.today_widget, 1, 0)
        self.layout.addWidget(self.week_widget, 1, 1)
        self.layout.addWidget(self.month_widget, 2, 0)
        self.layout.addWidget(self.year_widget, 2, 1)

        self.setLayout(self.layout)
