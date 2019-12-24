import os

import yaml
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from utils import loggers

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
    database = QSqlDatabase(database_conf.get("driver"))
    database.setDatabaseName(database_conf.get("name"))
    database.open()


def create_table(tb_name):
    """
    创建通用数据表，
    默认第一列为主键，名称:ID，类型:INTEGER, 自增
    """
    q = QSqlQuery()
    sql = "CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT);".format(tb_name)
    q.exec_(sql)


if __name__ == '__main__':
    create_db()
