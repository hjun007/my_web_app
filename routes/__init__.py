from flask import Blueprint

# 创建蓝图
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)
user = Blueprint('user', __name__)

# 导入路由定义
from . import auth_routes, admin_routes, user_routes, main_routes
