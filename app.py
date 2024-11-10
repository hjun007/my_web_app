from flask import Flask
from flask_login import LoginManager
from models import db, User

import configparser

config = configparser.ConfigParser()
config.read('config.ini')   

app = Flask(__name__)
app.config['SECRET_KEY'] = config['flask']['secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 注册蓝图
from routes import main
app.register_blueprint(main)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=config['flask']['debug'],
            host=config['flask']['host'],
            port=config['flask']['port'])

