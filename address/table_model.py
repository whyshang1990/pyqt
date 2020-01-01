# -*- coding: utf-8 -*-
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt


class TableModel(QAbstractTableModel):
    def __init__(self, addresses=None, parent=None):
        super(TableModel, self).__init__(parent)

        self.addresses = [] if addresses is None else addresses

    def rowCount(self, index=QModelIndex()):
        return len(self.addresses)

    def columnCount(self, index=QModelIndex()) -> int:
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if not 0 <= index.row() < len(self.addresses):
            return None

        if role == Qt.DisplayRole:
            name = self.addresses[index.row()]["name"]
            address = self.addresses[index.row()]["address"]

            if index.column() == 0:
                return name
            elif index.column() == 1:
                return address

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Address"

        return None

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)

        for row in range(rows):
            self.addresses.insert(position + row, {"name":"", "address":""})

        self.endInsertRows()
        return True
