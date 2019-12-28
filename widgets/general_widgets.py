# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel


class BaseWidget(QWidget):
    """本应用基础的展示控件，由4个Label控件组成，负责同时展示相关信息的4个属性"""
    def __init__(self, summary, value, details, remarks):
        super().__init__()
        self.summary = QLabel(summary)
        self.value = QLabel(value)
        self.details = QLabel(details)
        self.remarks = QLabel(remarks)

        self.layout = QGridLayout()

        self.init_ui()

    def init_ui(self):
        self.layout.addWidget(self.summary, 1, 0)
        self.layout.addWidget(self.value, 1, 1)
        self.layout.addWidget(self.details, 2, 0)
        self.layout.addWidget(self.remarks, 2, 1)

        self.setLayout(self.layout)
