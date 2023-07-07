import re
import logger

# 初始化日志记录器
logger = logger.setup_logger()

def check_text_for_sensitive_words(text_file):
    sensitive_file = "db/Sensitive.ini"

    logger.info('加载敏感词列表')
    def read_sensitive_file(sensitive_file):
        # 读取敏感词文件，生成敏感词列表
        sensitive_list = []
        with open(sensitive_file, 'r') as file:
            for line in file:
                word = line.strip()
                sensitive_list.append(word)
        return sensitive_list

    logger.info('开始检测敏感词')
    def check_text(text_content, sensitive_list):
        # 检查文本内容是否包含敏感词，并返回包含的敏感词及其出现次数的字典
        found_sensitive_words = {}
        for word in sensitive_list:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            matches = re.findall(pattern, text_content)
            if matches:
                found_sensitive_words[word] = len(matches)
        return found_sensitive_words

    # 读取敏感词文件
    sensitive_list = read_sensitive_file(sensitive_file)

    # 检查文本文件中是否包含敏感词，并返回结果
    with open(text_file, 'r', encoding='utf-8') as file:
        text_content = file.read()

    found_words = check_text(text_content, sensitive_list)
    return found_words

# text文件路径（外部传参）
# text_file = "120.76.55.186_w/20230626170920_a12555d017d20159e1e164249cbe41c8/20230626170921_text.txt"
# 检查文本文件中是否包含敏感词，并获取结果
# found_words = check_text_for_sensitive_words(text_file)
# if found_words:
#     print("文本中包含以下敏感词:")
#     for word, count in found_words.items():
#         print(f"{word}: {count} 次")
# else:
#     print("文本中未包含敏感词")





