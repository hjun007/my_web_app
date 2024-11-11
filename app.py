from flask import Flask
from flask_login import LoginManager
from models import db, User
from routes import main, auth, admin, user
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.config['SECRET_KEY'] = config['flask']['secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 注册所有蓝图
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=config['flask']['debug'],
            host=config['flask']['host'],
            port=config['flask']['port'])

