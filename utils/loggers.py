# -*- coding:utf-8 -*-
import os
import logging


def get_logger(logfile):
    """
    format：指定输出的格式和内容
    %(levelname)s：打印日志级别的名称
    %(filename)s：打印当前执行程序名
    %(funcName)s：打印日志的当前函数
    %(lineno)d：打印日志的当前行号
    %(asctime)s：打印日志的时间
    %(thread)d：打印线程ID
    %(threadName)s：打印线程名称
    %(process)d：打印进程ID
    %(message)s：打印日志信息
    """
    logger = logging.getLogger(logfile)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]-[%(filename)s]-[%(thread)d] '
                                  '%(funcName)s():%(lineno)d - %(message)s')
    log_root = os.getcwd()
    if not os.path.exists(log_root + "/" + "logs"):
        os.mkdir(log_root + "/" + "logs")

    # logger中添加FileHandler，可以将日志输出到日志文件
    file_handler = logging.FileHandler(log_root + "/logs/%s.log" % logfile)
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # logger中添加StreamHandler，可以将日志输出到屏幕上
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
