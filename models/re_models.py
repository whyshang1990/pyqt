# -*- coding: UTF-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQueryModel


class MSqlQueryModel(QSqlQueryModel):
    """
    继承QSqlQueryModel，重写data()方法
    实现单元格内容居中显示
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def data(self, index, role=None):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return QSqlQueryModel.data(self, index, role)
