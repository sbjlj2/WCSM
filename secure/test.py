# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/26 15:52
@Auth ： lujiejiang
@File ：test.py
@IDE ：PyCharm

"""
import Sensitive_Checker as Sensitive

link_file_path = "120.76.55.186_w/20230626170920_a12555d017d20159e1e164249cbe41c8/20230626170921_text.txt"

found_words = Sensitive.check_text_for_sensitive_words(link_file_path)
if found_words:
    print("文本中包含以下敏感词:")
    for word, count in found_words.items():
        print(f"{word}: {count} 次")
else:
    print("文本中未包含敏感词")
