import os

import yaml
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from utils import loggers
from utils.constants import Constants

logger = loggers.get_logger("conn_db")


def create_db():
    """
    创建数据库
    """
    # 读取配置文件
    logger.debug(os.environ["BASE_DIR"])
    with open(os.environ["BASE_DIR"] + "/conf/settings.yml", "r", encoding="utf-8") as f:
        c = yaml.full_load(f.read())
    database_conf = c.get("database")
    # 连接sqlite3数据库
    database = QSqlDatabase.addDatabase(database_conf.get("driver"))
    database.setDatabaseName(database_conf.get("name"))
    database.open()
    init_db()
    logger.debug("数据初始化完成")


def init_db():
    q = QSqlQuery()
    # 创建表
    q.exec_(Constants.SQL)


if __name__ == '__main__':
    create_db()
