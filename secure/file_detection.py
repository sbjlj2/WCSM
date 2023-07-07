# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/27 15:18
@Auth ： lujiejiang
@File ：file_detection.py
@IDE ：PyCharm

"""
import os
import send_email
import logger

# 文件夹路径
folder_path = "report"

# 记录最新文件的日期时间
record_file_path = "report/record.txt"

# 日志配置
logger = logger.setup_logger()

def detect_new_files():
    # 获取上次记录的最新文件的日期时间
    def get_last_file_datetime():
        if os.path.exists(record_file_path):
            with open(record_file_path, 'r') as file:
                last_file = file.read().strip()
                return last_file.split("_", 1)[-1]  # 提取日期时间部分
        else:
            return ""

    # 记录最新文件的日期时间到文件
    def record_last_file_datetime(file_datetime):
        with open(record_file_path, 'w') as file:
            file.write(file_datetime)

    # 上次检测的最新文件的日期时间
    last_file_datetime = get_last_file_datetime()

    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)

    # 检查是否有新文件产生
    new_files = []
    for file in files:
        if file.startswith("report_") and file.endswith(".txt"):
            file_datetime = file.split("_", 1)[-1].split(".", 1)[0]  # 提取日期时间部分
            if file_datetime > last_file_datetime:
                new_files.append(file)

    if new_files:
        # 存在新文件，获取最新文件的内容
        new_files.sort()  # 按日期时间排序
        new_file = new_files[-1]
        file_path = os.path.join(folder_path, new_file)
        with open(file_path, 'r') as file:
            content = file.read()

        # 更新最新文件的日期时间并记录到文件
        last_file_datetime = new_file.split("_", 1)[-1].split(".", 1)[0]  # 提取日期时间部分
        record_last_file_datetime(last_file_datetime)

        # 日志记录新文件信息
        logger.info(f"检测到新文件: {new_file}")

        # 发送邮件
        send_email.send_email(content)

# 在其他脚本中调用 detect_new_files() 函数来检测新文件并发送邮件
