import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import schedule
import time
from datetime import datetime, timedelta
import configparser
from mailer.email_sender import send_community_updates

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

def job():
    print(f"开始执行邮件发送任务: {datetime.now()}")
    # 获取昨天的日期作为查询范围
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    # 发送昨天到今天的更新报告
    send_community_updates(yesterday, today)

def run_scheduler():
    # 获取配置的发送时间
    send_hour = config.getint('scheduler', 'send_hour')
    send_minute = config.getint('scheduler', 'send_minute')
    
    # 设置每天固定时间运行
    schedule.every().day.at(f"{send_hour:02d}:{send_minute:02d}").do(job)
    
    print(f"定时任务已启动，将在每天 {send_hour:02d}:{send_minute:02d} 发送邮件")

    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

if __name__ == '__main__':
    # run_scheduler() 
    job()
    