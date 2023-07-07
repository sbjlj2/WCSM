import requests
import hashlib
import os
import time
import datetime
import logger
import file_detection
from urllib.parse import urlparse
from Get_Source import save_content


def create_domain_folder(url):
    # 提取URL中的域名作为文件夹名称
    domain = urlparse(url).netloc

    # 提取URL中域名后面的内容作为文件夹名称
    folder_name = domain
    path = urlparse(url).path
    if path:
        folder_name += path.replace('/', '_')
        logger.info('提取URL中的域名作为文件夹名称')

    # 创建域名文件夹
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        logger.info('创建域名文件夹')
    return folder_name

def get_hash(url):
    response = requests.get(url)
    content = response.content
    hash_value = hashlib.md5(content).hexdigest()
    return hash_value

def check_hash(folder_name, current_hash):
    # 获取上次保存的HASH值
    hash_file = os.path.join(folder_name, 'hash.txt')
    previous_hash = ''

    if os.path.exists(hash_file):
        with open(hash_file, 'r') as file:
            previous_hash = file.read()

    if current_hash != previous_hash:
        # 保存当前的HASH值到文件
        with open(hash_file, 'w') as file:
            file.write(current_hash)
        logger.info('保存当前的HASH值到文件')

        # 创建时间和HASH值命名的文件夹
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_folder = os.path.join(folder_name, f"{current_time}_{current_hash}")
        os.makedirs(new_folder)
        logger.info('创建时间和HASH值命名的文件夹')

        # 调用Get_Source.py并传递URL和新文件夹的名称
        save_content(url, new_folder)
        logger.info('开始获取网页内容')
    else:
        logger.info('网站未变更，等待下次检测')

# 监控URL
url = 'test.com'

# 调用日志
logger = logger.setup_logger()
logger.info('启动网站内容安全智能监控系统')
logger.info(f'开始监控{url}')

# 创建域名文件夹
domain_folder = create_domain_folder(url)

while True:
    # 获取HASH值
    hash_value = get_hash(url)
    logger.info('获取网页HASH值')

    logger.info('检查HASH值并处理')
    # 检查HASH值并处理
    check_hash(domain_folder, hash_value)

    # 读取报告
    file_detection.detect_new_files()

    # 等待5分钟
    time.sleep(300)
