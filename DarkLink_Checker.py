import logger
from urllib.parse import urlparse

# 初始化日志记录器
logger = logger.setup_logger()

def read_dark_file(dark_file):
    domain_list = []
    with open(dark_file, 'r') as file:
        for line in file:
            domain = line.strip()
            domain_list.append(domain)
    return domain_list

def read_link_file(link_file):
    url_domain_mapping = {}
    with open(link_file, 'r') as file:
        for line in file:
            url = line.strip()
            domain = extract_domain(url)
            url_domain_mapping[url] = domain
    return url_domain_mapping

def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

def compare_domains(dark_list, url_domain_mapping):
    result = [url for url, domain in url_domain_mapping.items() if domain not in dark_list]
    return result

def check_dark_links(link_file):
    dark_file = "db/Dark_white.ini"
    logger.info('开始检测暗链')
    dark_list = read_dark_file(dark_file)
    logger.info('读取暗链白名单列表')
    url_domain_mapping = read_link_file(link_file)
    result = compare_domains(dark_list, url_domain_mapping)
    return result

# link_file_path = "120.76.55.186_w/20230626113605_73a3f4b17d4d5dddb65a302a4cf7532f/20230626113605_link.txt"
# result = check_dark_links(link_file_path)
# if result:
#     result_string = "\n".join(result)
#     print(result_string)
# else:
#     print("无")