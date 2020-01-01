# -*- coding: utf-8 -*-
from PySide2.QtCore import QSortFilterProxyModel, QRegExp, Qt, Signal, QItemSelection, QModelIndex
from PySide2.QtWidgets import QTabWidget, QTableView, QAbstractItemView, QMessageBox

from address.add_dialog_widget import AddDialogWidget
from address.new_address_tab import NewAddressTab
from address.table_model import TableModel


class AddressWidget(QTabWidget):
    selection_changed = Signal(QItemSelection)

    def __init__(self, parent=None):
        super(AddressWidget, self).__init__(parent)

        self.table_model = TableModel()
        self.new_address_tab = NewAddressTab()
        self.new_address_tab.send_details.connect(self.add_entry)

        self.addTab(self.new_address_tab, "Address Book")
        self.setup_tabs()

    def setup_tabs(self):
        groups = ["ABC", "DEF", "GHI", "JKL", "MNO", "PQR", "STU", "VW", "XYZ"]

        for group in groups:
            proxy_model = QSortFilterProxyModel()
            proxy_model.setSourceModel(self.table_model)
            proxy_model.setDynamicSortFilter(True)

            table_view = QTableView()
            table_view.setModel(proxy_model)
            table_view.setSortingEnabled(True)
            # 单元格选择模式，默认选中单元格
            # QAbstractItemView.SelectItems    Selecting single items. 选取item
            # QAbstractItemView.SelectRows     Selecting only rows.    选取行
            # QAbstractItemView.SelectColumns  Selecting only columns. 选取列
            table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
            # 自动填充列头，表现形式为，列头的空余部分用最后一列来填充
            table_view.horizontalHeader().setStretchLastSection(True)
            table_view.verticalHeader().hide()
            # 对于表格中的数据，默认只要双击就可以修改其中的数据。
            # 如果文档是处于预览状态或者不可编辑状态，那就需要对表格设定为不可编辑模式。
            # QTableWidget.NoEditTriggers 0 No editing possible. 不能对表格内容进行修改
            # QTableWidget.CurrentChanged 1 Editing start whenever current item changes.任何时候都能对单元格修改
            # QTableWidget.DoubleClicked 2 Editing starts when an item is double clicked.双击单元格
            # QTableWidget.SelectedClicked 4 Editing starts when clicking on an already selected item.单击已选中的内容
            # QTableWidget.EditKeyPressed 8 Editing starts when the platform edit key has been pressed over an item.
            # QTableWidget.AnyKeyPressed 16 Editing starts when any key is pressed over an item.按下任意键就能修改
            # QTableWidget.AllEditTriggers 31 Editing starts for all above actions.以上条件全包括
            table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # 行选择模式
            # QTableWidget.NoSelection 不能选择
            # QTableWidget.SingleSelection 选中单个目标
            # QTableWidget.MultiSelection 选中多个目标
            # QTableWidget.ExtendedSelection shift键的连续选择
            # QTableWidget.ContiguousSelection ctrl键的不连续的多个选择
            table_view.setSelectionMode(QAbstractItemView.SingleSelection)

            re_filter = "^[%s].*" % group
            proxy_model.setFilterRegExp(QRegExp(re_filter, Qt.CaseInsensitive))
            proxy_model.setFilterKeyColumn(0)
            proxy_model.sort(0, Qt.AscendingOrder)

            view_select_model = table_view.selectionModel()
            view_select_model.selectionChanged.connect(self.selection_changed)

            self.addTab(table_view, group)

    def add_entry(self, name=None, address=None):
        """ Add an entry to the addressbook. """
        if name is None and address is None:
            add_dialog = AddDialogWidget()

            if add_dialog.exec_():
                name = add_dialog.name
                address = add_dialog.address

        address = {"name": name, "address": address}
        addresses = self.table_model.addresses[:]

        # The QT docs for this example state that what we're doing here
        # is checking if the entered name already exists. What they
        # (and we here) are actually doing is checking if the whole
        # name/address pair exists already - ok for the purposes of this
        # example, but obviously not how a real addressbook application
        # should behave.
        try:
            addresses.remove(address)
            QMessageBox.information(self, "Duplicate Name",
                                    "The name \"%s\" already exists." % name)
        except ValueError:
            # The address didn't already exist, so let's add it to the model.

            # Step 1: create the  row
            self.table_model.insertRows(0)

            # Step 2: get the index of the newly created row and use it.
            # to set the name
            ix = self.table_model.index(0, 0, QModelIndex())
            self.table_model.setData(ix, address["name"], Qt.EditRole)

            # Step 3: lather, rinse, repeat for the address.
            ix = self.table_model.index(0, 1, QModelIndex())
            self.table_model.setData(ix, address["address"], Qt.EditRole)

            # Remove the newAddressTab, as we now have at least one
            # address in the model.
            self.removeTab(self.indexOf(self.new_address_tab))

            # The screenshot for the QT example shows nicely formatted
            # multiline cells, but the actual application doesn't behave
            # quite so nicely, at least on Ubuntu. Here we resize the newly
            # created row so that multiline addresses look reasonable.
            table_view = self.currentWidget()
            table_view.resizeRowToContents(ix.row())