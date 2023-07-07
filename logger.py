# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/27 09:32
@Auth ： lujiejiang
@File ：logger.py
@IDE ：PyCharm

"""
import logging

def setup_logger():
    # 创建日志记录器
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # 设置日志文件路径
    log_file = 'log/app.log'

    # 检查是否已经添加处理程序
    if not logger.handlers:
        # 创建文件处理程序
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # 创建控制台处理程序
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 定义日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 将处理程序添加到日志记录器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


if __name__ == '__main__':
    # 初始化日志记录器
    logger = setup_logger()

    # 记录日志消息
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
