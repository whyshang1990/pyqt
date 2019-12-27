# -*- coding: UTF-8 -*-
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlQueryModel

from utils import loggers

LOGGER = loggers.get_logger("re_models")


class MyTableModel(QStandardItemModel):
    """
    继承QStandardItemModel，初始化为表格
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderData(0, Qt.Horizontal, '金额')
        self.init_model()

    def init_model(self):
        h = self.headerData(0, Qt.Horizontal)
        LOGGER.debug(h)
        self.refresh_model()

    def data(self, index, role=None):
        """重写data()方法,实现单元格内容居中显示"""
        # 设置居中显示
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return QStandardItemModel.data(self, index, role)

    @pyqtSlot()
    def refresh_model(self):
        """从QSqlQueryModel获取数据并重新格式化后放入表格"""
        query_model = QSqlQueryModel()
        query_model.setQuery("select cost,trans_type,category,create_date from tb_transactions LIMIT 7")
        row_count, column_count = query_model.rowCount(), query_model.columnCount()
        if row_count == 0:
            return
        LOGGER.debug("表格刷新")
        LOGGER.debug("row: %s, column: %s", row_count, column_count)
        for row in range(row_count):
            for column in range(column_count):
                if column == 1:
                    r = query_model.data(query_model.index(row, column))
                    if r == 1:
                        item = QStandardItem("收入")
                    else:
                        item = QStandardItem("支出")
                else:
                    item = QStandardItem(str(query_model.data(query_model.index(row, column))))
                self.setItem(row, column, item)
