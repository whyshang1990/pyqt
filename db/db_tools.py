# -*- coding: UTF-8 -*-
"""数据库工具类"""
import os

import yaml
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from utils import loggers
from utils.constants import Constants

LOGGER = loggers.get_logger("conn_db")


def create_db():
    """
    创建数据库
    """
    # 读取配置文件
    LOGGER.debug(os.environ[Constants.BASE_DIR])
    with open(os.environ["BASE_DIR"] + "/conf/settings.yml", "r", encoding="utf-8") as file:
        c = yaml.full_load(file.read())
    database_conf = c.get("database")
    # 连接sqlite3数据库
    database = QSqlDatabase.addDatabase(database_conf.get("driver"))
    database.setDatabaseName(database_conf.get("name"))
    database.open()
    init_db()
    LOGGER.debug("数据初始化完成")


def init_db():
    sql_query = QSqlQuery()
    LOGGER.debug(os.environ[Constants.BASE_DIR])
    # 读取init_db.sql，并执行其中的建表语句
    with open(os.environ[Constants.BASE_DIR] + "/db/init_db.sql", "r", encoding="utf-8") as file:
        for sql in file.read().split(";")[:-1]:
            sql_query.exec_(sql)


def insert_into(tb_name, params_dict):
    """
    通用的函数，向数据库插入数据
    :param tb_name: 插入表名称
    :param params_dict: 插入数据字典，键为数据库列名，值为插入数据
    :return:
    """
    param_names = ",".join(params_dict.keys())
    values_format = []
    for value in params_dict.values():
        if isinstance(value, str):
            values_format.append("'" + value + "'")
        else:
            values_format.append(str(value))
    param_values = ",".join(values_format)
    # logger.debug("param_names: %s", param_names)
    # logger.debug("param_values: %s", param_values)
    try:
        q = QSqlQuery()
        sql = "INSERT INTO {} ({}) VALUES ({})".format(tb_name, param_names, param_values)
        r = q.exec_(sql)
        if not r:
            LOGGER.debug("数据库插入错误")
    except Exception as exp:
        LOGGER.error("插入数据异常:%s", exp)


if __name__ == '__main__':
    create_db()
