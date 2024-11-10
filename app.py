from flask import Flask
from routes import main
import configparser
from models import db
import os

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///communities.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 确保数据库文件存在
with app.app_context():
    db.create_all()

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(
        debug=config.getboolean('flask', 'debug'),
        host=config.get('flask', 'host'),
        port=config.getint('flask', 'port')
    ) 