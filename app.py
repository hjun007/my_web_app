from flask import Flask
from models import db, User
from routes import main
from flask_login import LoginManager
import threading
import os
import configparser
# from scheduler.task_scheduler import run_scheduler

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///communities.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# 初始化数据库
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    # 使用新的 Session.get() 方法替代 Query.get()
    return db.session.get(User, int(user_id))

# 注册蓝图
app.register_blueprint(main)

# # 添加一个标志来防止重复启动
# scheduler_started = False

# 在新线程中启动定时任务
# def start_scheduler():
#     global scheduler_started
#     if scheduler_started:
#         return
    
#     with app.app_context():
#         scheduler_started = True
#         run_scheduler()

# 只在主进程中启动调度器
# if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
#     scheduler_thread = threading.Thread(target=start_scheduler)
#     scheduler_thread.daemon = True
#     scheduler_thread.start()

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

