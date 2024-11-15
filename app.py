from flask import Flask
from models import db
from routes import main
from scheduler.task_scheduler import run_scheduler
import threading
import configparser
import os
import sys

import logging
from globals import GlobalVars
logging.basicConfig(level=logging.DEBUG)

import logging
import sys
from flask import Flask

# 配置日志
def setup_logging():
    # 创建日志处理器，输出到标准输出
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # 设置 Flask 应用的日志
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    
    # 设置 Werkzeug 的日志
    logging.getLogger('werkzeug').addHandler(handler)
    
    # 设置 SQLAlchemy 的日志
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').addHandler(handler)

app = Flask(__name__)
globals = GlobalVars()
setup_logging()

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///communities.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_DEBUG'] = False


# 初始化数据库
db.init_app(app)

# 注册蓝图
app.register_blueprint(main)

# 添加一个标志来防止重复启动
scheduler_started = False

# 在新线程中启动定时任务
def start_scheduler():
    global scheduler_started
    if scheduler_started:
        return
    
    with app.app_context():
        scheduler_started = True
        run_scheduler()

def init_db():
    with app.app_context():
        db.create_all()

# 在应用启动时初始化数据库
init_db()

# 只在主进程中启动调度器
if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    app.logger.info("定时任务已启动")

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    with app.app_context():
        db.create_all()
    app.run(
        debug=config.getboolean('flask', 'debug'),
        host=config.get('flask', 'host'),
        port=config.getint('flask', 'port')
    )

