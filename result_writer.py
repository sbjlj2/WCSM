# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/27 13:51
@Auth ： lujiejiang
@File ：result_writer.py
@IDE ：PyCharm

"""
def write_results_to_file(url, sensitive_words_result, dark_links_result, filename):

    with open(filename, 'w') as file:
        file.write(f"当前检测网站: {url}\n\n")

        if sensitive_words_result:
            file.write("敏感词检测结果如下:\n")
            for word, count in sensitive_words_result.items():
                file.write(f"{word}: {count} 次\n")
            file.write("\n")
        else:
            file.write("敏感词检测结果如下:\n")
            file.write("未发现敏感词")

        if dark_links_result:
            file.write("暗链检测结果如下：\n")
            result_string = "\n".join(dark_links_result)
            file.write(f"{result_string}\n")
            file.write("\n")
        else:
            file.write("暗链检测结果如下：\n")
            file.write("未发现暗链")
