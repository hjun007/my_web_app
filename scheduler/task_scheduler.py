import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from datetime import datetime, timedelta
import configparser
from mailer.email_sender import send_community_updates
from flask import current_app
import pytz
from globals import globals
# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

def job():
    print(f"开始执行邮件发送任务: {datetime.now()}")
    # 获取昨天的日期作为查询范围
    # yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    # 发送昨天到今天的更新报告
    send_community_updates(today, today)

def run_scheduler():
    china_tz = pytz.timezone('Asia/Shanghai')
    
    current_app.logger.info(f"定时任务已启动，将在每天 {globals.push_time['hour']}:{globals.push_time['minute']} 发送邮件")

    while True:
        try:
            send_hour, send_minute = globals.push_time['hour'], globals.push_time['minute']
            current_hour, current_minute = datetime.now(china_tz).hour, datetime.now(china_tz).minute
            if current_hour == send_hour and current_minute == send_minute:
                job()
                time.sleep(30)
            else:
                time.sleep(30)
            
        except Exception as e:
            print(f"定时任务运行出错: {e}")
            time.sleep(60)

if __name__ == '__main__':
    # 运行定时任务
    print("开始运行定时任务...")
    #run_scheduler() 
    print("定时任务运行完毕。")

    