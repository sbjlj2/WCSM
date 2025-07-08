# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/27 14:55
@Auth ： lujiejiang
@File ：send_email.py
@IDE ：PyCharm

"""
import smtplib
import logger
from email.mime.text import MIMEText
from email.utils import formataddr

# 设置日志记录器
logger = logger.setup_logger()

def send_email(content):
    # 邮件配置信息
    from_name = "xxxx@qq.com"
    from_addr = "xxxx@qq.com"
    from_pwd = "xxxxi"
    to_addr = "xxxx@qq.com"
    subject = "网站内容安全监控系统告警"#邮件主题

    # 构造邮件内容
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr([from_name, from_addr])
    msg['Subject'] = subject

    # SMTP服务器地址，QQ邮箱的SMTP地址是"smtp.qq.com"
    smtp_srv = "smtp.qq.com"

    try:
        srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465)
        srv.login(from_addr, from_pwd)
        srv.sendmail(from_addr, [to_addr], msg.as_string())
        logger.info('告警邮件发送成功')
    except Exception as e:
        logger.error('邮件发送失败: %s', str(e))
    finally:
        srv.quit()


# email_content = "Hello World"
# # 调用发送邮件函数
# send_email(email_content)
