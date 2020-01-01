# -*- coding: utf-8 -*-
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QLabel, QDialogButtonBox, QLineEdit, QTextEdit, QGridLayout, QVBoxLayout


class AddDialogWidget(QDialog):
    def __init__(self, parent=None):
        super(AddDialogWidget, self).__init__(parent)

        name_label = QLabel("name")
        address_label = QLabel("address")
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.name_text = QLineEdit()
        self.address_text = QTextEdit()

        grid = QGridLayout()
        grid.setColumnStretch(1, 2)
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_text, 0, 1)
        grid.addWidget(address_label, 1, 0, Qt.AlignLeft | Qt.AlignTop)
        grid.addWidget(self.address_text, 1, 1, Qt.AlignLeft)

        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setWindowTitle("Add a Contact")

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    @property
    def name(self):
        return self.name_text.text()

    @property
    def address(self):
        return self.address_text.toPlainText()

