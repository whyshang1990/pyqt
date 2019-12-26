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


def insert_into(tb_name, params_dict):
    """
    通用的函数，向数据库插入数据
    :param tb_name: 插入表名称
    :param params_dict: 插入数据字典，键为数据库列名，值为插入数据
    :return:
    """
    param_names = ",".join(params_dict.keys())
    param_values = ",".join(params_dict.values())
    logger.debug("param_names: %s", param_names)
    logger.debug("param_values: %s", param_values)
    try:
        q = QSqlQuery()
        sql = "INSERT INTO {} ({}) VALUES ({})".format(tb_name, param_names, param_values)
        q.exec_(sql)
    except Exception as e:
        logger.error("插入数据异常:%s", e)


if __name__ == '__main__':
    create_db()
