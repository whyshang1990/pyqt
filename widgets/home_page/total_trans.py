# -*- coding: utf-8 -*-
"""交易总计控件"""
from PyQt5.QtCore import QDate, Qt, pyqtSlot
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QLabel, QHBoxLayout, QListView

from utils import loggers
from utils.constants import Constants

LOGGER = loggers.get_logger("total_trans")
# 日期格式
DATE_FORMAT = "M月d日"


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
            self.layout = QHBoxLayout()
            self.summary_label = QLabel(summary + "(" + details + ")", self)
            self.income_label = QLabel("总收入：{:.2f}".format(income), self)
            self.expend_label = QLabel("总支出：{:.2f}".format(expend), self)

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
            sql = "select sum(cost) as sum from tb_transactions where create_date >= '{}' and create_date <= '{}' " \
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
