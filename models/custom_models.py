# -*- coding: UTF-8 -*-
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtSql import QSqlQueryModel

from utils import loggers

LOGGER = loggers.get_logger("re_models")


class RecentTransTableModel(QStandardItemModel):
    """
    继承QStandardItemModel，初始化为表格
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_model()

    def init_model(self):
        self.headerData(0, Qt.Horizontal)
        self.refresh_model()

    def data(self, index, role=None):
        """重写data()方法,实现单元格内容居中显示"""
        # 设置居中显示
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return QStandardItemModel.data(self, index, role)

    @Slot()
    def refresh_model(self):
        max_rows = 7
        """从QSqlQueryModel获取数据并重新格式化后放入表格"""
        query_model = QSqlQueryModel()
        query_model.setQuery("select cost,trans_type,category,create_date from tb_transaction "
                             "order by create_date desc limit {}".format(max_rows))
        row_count, column_count = query_model.rowCount(), query_model.columnCount()
        if row_count == 0:
            LOGGER.debug("未查询到数据")
            return

        row_count = min(max_rows, row_count)
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
                elif column == 0:
                    item = QStandardItem("{:.2f}".format(query_model.data(query_model.index(row, column))))
                else:
                    item = QStandardItem(str(query_model.data(query_model.index(row, column))))
                self.setItem(row, column, item)
