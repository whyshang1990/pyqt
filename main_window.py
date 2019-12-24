from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget

from central_widget import CentralWidget
from utils import loggers

logger = loggers.get_logger("MainWindow")


class MainWindow(QMainWindow):
    """应用程序主窗口"""
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_menubar()
        # self.setCentralWidget(self.init_centeral_widgat())
        self.setCentralWidget(CentralWidget())

    def init_ui(self):
        self.setWindowTitle("记账日志")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumWidth(300)
        self.center()

    def center(self):
        """
        使用自身和桌面屏幕的geometry，使mainWindow移动到屏幕中心
        """
        s_size = self.geometry()
        logger.debug("s_size")
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - s_size.width()) / 2, (screen.height() - s_size.height()) / 2)

    def init_menubar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("New File")
