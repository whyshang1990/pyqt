from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel


class CentralWidget(QWidget):
    """主窗口中心控件"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        left = NavigateWidget()
        right = DisplayWidget()
        layout.addWidget(left)
        layout.addWidget(right)

        # 设置两个控件的拉伸系数
        layout.setStretchFactor(left, 1)
        layout.setStretchFactor(right, 4)

        self.setLayout(layout)


class NavigateWidget(QWidget):
    """导航控件"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        home = QPushButton("主页")
        acct_book = QPushButton("账本")
        statistics = QPushButton("统计")
        layout.addWidget(home)
        layout.addWidget(acct_book)
        layout.addWidget(statistics)
        layout.addStretch(1)

        self.setLayout(layout)


class DisplayWidget(QWidget):
    """展示控件"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        show = QLabel("show")
        layout.addWidget(show)
        self.setLayout(layout)
