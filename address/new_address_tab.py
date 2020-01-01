# -*- coding: utf-8 -*-
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout

from address.add_dialog_widget import AddDialogWidget


class NewAddressTab(QWidget):
    send_details = Signal(str, str)

    def __init__(self, parent=None):
        super(NewAddressTab, self).__init__()

        description_label = QLabel("There are no contacts in your address book."
                                   "\nClick Add to add new contacts.")
        add_button = QPushButton("Add")

        layout = QVBoxLayout()
        layout.addWidget(description_label)
        layout.addWidget(add_button, 0, Qt.AlignCenter)
        self.setLayout(layout)

        add_button.clicked.connect(self.add_entry)

    def add_entry(self):
        add_dialog = AddDialogWidget()

        if add_dialog.exec_():
            name = add_dialog.name
            address = add_dialog.address
            self.send_details.emit(name, address)