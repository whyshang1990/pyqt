# -*- coding: UTF-8 -*-
import os
import sys

from PyQt5.QtWidgets import QApplication

from db import db_tools
from main_window import MainWindow
from utils import loggers

LOGGER = loggers.get_logger("app")


def main():
    app = QApplication(sys.argv)
    init_settings()

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())


def init_settings():
    os.environ["BASE_DIR"] = os.getcwd()
    db_tools.create_db()


if __name__ == '__main__':
    main()
