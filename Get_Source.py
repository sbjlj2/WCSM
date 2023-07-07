import requests
from bs4 import BeautifulSoup
import logger
import os
import datetime
from urllib.parse import urljoin, urlparse
import DarkLink_Checker as Dark
import Sensitive_Checker as Sensitive
import result_writer

# 初始化日志记录器
logger = logger.setup_logger()


def save_content(url, folder_name):
    # 发送HTTP GET请求获取网页内容
    response = requests.get(url)
    html_content = response.content

    # 创建文件夹
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # 生成时间戳
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    logger.info('保存源码文件')
    # 保存源码文件
    source_filename = os.path.join(folder_name, f'{current_time}_source.txt')
    with open(source_filename, 'wb') as source_file:
        source_file.write(html_content)

    logger.info('保存文本文件')
    # 保存文本文件
    text_filename = os.path.join(folder_name, f'{current_time}_text.txt')
    with open(text_filename, 'w', encoding='utf-8') as text_file:
        # 使用BeautifulSoup解析网页内容并提取文本
        soup = BeautifulSoup(html_content, 'lxml')
        text_content = soup.get_text()

        # 去除空行并将内容拼接在一起
        text_content_combined = ''.join([line.strip() for line in text_content.splitlines() if line.strip()])
        # 写入文件
        text_file.write(text_content_combined)

    logger.info('进行敏感词检测')
    # 调用敏感词检测
    found_words_result = Sensitive.check_text_for_sensitive_words(text_filename)
    if found_words_result:
        # print("文本中包含以下敏感词:")
        for word, count in found_words_result.items():
            # print(f"{word}: {count} 次")
            logger.info(f"{word}: {count} 次")
    else:
        # print("文本中未包含敏感词")
        logger.info('文本中未包含敏感词')

    logger.info('保存源码中的链接和网页中的所有链接')
    # 保存源码中的链接和网页中的所有链接
    link_filename = os.path.join(folder_name, f'{current_time}_link.txt')
    with open(link_filename, 'w', encoding='utf-8') as link_file:
        # 使用正则表达式提取源码中的链接和网页中的所有链接
        soup = BeautifulSoup(html_content, 'lxml')
        links = soup.find_all('a')
        unique_links = set()

        for link in links:
            href = link.get('href')
            if href:
                absolute_url = urljoin(url, href)
                parsed_url = urlparse(absolute_url)
                if parsed_url.netloc and parsed_url.scheme:
                    unique_links.add(absolute_url)

        for link in unique_links:
            link_file.write(link + '\n')

    logger.info('开始检测暗链')

    # 调用暗链检测功能
    dark_links_result = Dark.check_dark_links(link_filename)
    if dark_links_result:
        result_string = "\n".join(dark_links_result)
        logger.info(f'检测到网站存在以下暗链地址：\n{result_string}')
        # print(f'检测到网站存在以下暗链地址：\n{result_string}')
    else:
        # print("无")
        logger.info('未检测到暗链')

    # 将结果写入到文件中
    if found_words_result or dark_links_result:
        result_writer.write_results_to_file(url, found_words_result, dark_links_result,f'report/report_{current_time}.txt')

# 测试代码
# url = 'http://120.76.55.186/q'
# folder_name="1234"
# save_content(url, folder_name)
