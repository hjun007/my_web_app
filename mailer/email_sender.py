from flask_mail import Mail, Message
from flask import Flask, render_template_string
import configparser
import socket
from models import EmailSubscription, Community
from crawler.simple_crawler import scrape_data
import json
from datetime import datetime

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

# 配置Flask-Mail
app.config['MAIL_SERVER'] = config.get('email', 'server')
app.config['MAIL_PORT'] = config.getint('email', 'port')
app.config['MAIL_USE_TLS'] = config.getboolean('email', 'use_tls')
app.config['MAIL_USE_SSL'] = config.getboolean('email', 'use_ssl')
app.config['MAIL_USERNAME'] = config.get('email', 'username')
app.config['MAIL_PASSWORD'] = config.get('email', 'password')
app.config['MAIL_DEFAULT_SENDER'] = config.get('email', 'default_sender')
app.config['MAIL_DEBUG'] = True

mail = Mail(app)

def send_email(subject, recipients, body):
    with app.app_context():
        msg = Message(subject, recipients=recipients, body=body)
        mail.send(msg)
        print(f"邮件已发送到: {recipients}")

def send_community_updates(starttime, endtime):
    """
    发送指定时间范围内的小区更新信息给所有订阅者
    
    参数:
    starttime (str): 开始时间，格式：YYYY-MM-DD
    endtime (str): 结束时间，格式：YYYY-MM-DD
    """
    with app.app_context():
        # 获取所有邮箱订阅者
        subscribers = EmailSubscription.query.all()
        if not subscribers:
            print("没有邮箱订阅者")
            return

        # 获取所有订阅的小区
        communities = Community.query.all()
        if not communities:
            print("没有订阅的小区")
            return

        # 构建邮件内容
        email_content = f"房源监控系统更新报告 ({starttime} 至 {endtime})\n\n"
        
        # 获取每个小区的数据
        url = config.get('crawler', 'url')
        for community in communities:
            data = {
                "keywords": community.name,
                "page": 1,
                "xqid": 0,
                "starttime": starttime,
                "endtime": endtime
            }
            
            try:
                response_data = scrape_data(url, data)
                email_content += f"\n{community.name} 的更新：\n"
                email_content += json.dumps(json.loads(response_data), 
                                         ensure_ascii=False, 
                                         indent=2)
                email_content += "\n" + "-"*50 + "\n"
            except Exception as e:
                print(f"获取 {community.name} 的数据时出错: {e}")
                continue

        # 发送邮件给所有订阅者
        recipients = [sub.email for sub in subscribers]
        subject = f"房源监控系统更新报告 ({starttime} 至 {endtime})"
        
        try:
            send_email(subject, recipients, email_content)
            print(f"更新报告已发送给 {len(recipients)} 个订阅者")
        except Exception as e:
            print(f"发送邮件时出错: {e}")

if __name__ == '__main__':
    try:
        # 检查SMTP服务器是否可达
        socket.getaddrinfo(app.config['MAIL_SERVER'], 'smtp', 0, socket.SOCK_STREAM)
        print("SMTP服务器可达")
        
        # 测试发送更新报告
        today = datetime.now().strftime("%Y-%m-%d")
        send_community_updates(today, today)
    except socket.gaierror as e:
        print(f"DNS解析错误: {e}")

    