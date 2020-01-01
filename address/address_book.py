# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QMainWindow, QApplication

from address.address_widget import AddressWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.address_widget = AddressWidget()
        self.setCentralWidget(self.address_widget)
        # self.createMenus()
        self.setWindowTitle("Address Book")


if __name__ == "__main__":
    """ Run the application. """
    import sys
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
