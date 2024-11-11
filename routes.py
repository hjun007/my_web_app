# from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app, flash
# from crawler.simple_crawler import scrape_data
# from models import db, CommunitySubscription, EmailSubscription, User
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user, logout_user, login_required, current_user
# import json
# import configparser
# from datetime import datetime
# from scheduler.task_scheduler import job
# from functools import wraps

# # 读取配置文件
# config = configparser.ConfigParser()
# config.read('config.ini')

# main = Blueprint('main', __name__)

# # 管理员权限装饰器
# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or not current_user.is_admin:
#             return jsonify({'success': False, 'message': '无权限访问'}), 403
#         return f(*args, **kwargs)
#     return decorated_function

# @main.route('/')
# def index():
#     if current_user.is_authenticated:
#         communities = CommunitySubscription.query.filter_by(user_id=current_user.id).order_by(CommunitySubscription.created_at.desc()).all()
#         emails = EmailSubscription.query.filter_by(user_id=current_user.id).order_by(EmailSubscription.created_at.desc()).all()
#     else:
#         communities = []
#         emails = []
#     return render_template('index.html', 
#                          communities=[{'id': c.id, 'name': c.name} for c in communities],
#                          emails=[{'id': e.id, 'email': e.email} for e in emails])

# @main.route('/add-community', methods=['GET'])
# def add_community_form():
#     return render_template('add_community.html')

# @main.route('/add-community', methods=['POST'])
# @login_required
# def add_community_subscription():
#     community_name = request.form.get('community')
#     # print(f"接收到的表单数据: {request.form}")
#     if community_name:
#         subscription = CommunitySubscription(
#             name=community_name,
#             user_id=current_user.id
#         )
#         db.session.add(subscription)
#         db.session.commit()
#         return redirect(url_for('main.index'))
#     return jsonify({'success': False, 'message': '小区名称不能为空'})

# @main.route('/delete-community/<int:subscription_id>', methods=['POST'])
# @login_required
# def delete_community_subscription(subscription_id):
#     subscription = CommunitySubscription.query.get_or_404(subscription_id)
#     if subscription.user_id != current_user.id and not current_user.is_admin:
#         return jsonify({'success': False, 'message': '无权限删除此订阅'})
    
#     db.session.delete(subscription)
#     db.session.commit()
#     return jsonify({'success': True})

# @main.route('/community-details')
# @login_required
# def community_details():
#     keywords = request.args.get('keywords', '')
#     page = request.args.get('page', 1, type=int)
#     starttime = request.args.get('starttime', '')
#     endtime = request.args.get('endtime', '')
    
#     url = config.get('crawler', 'url')
#     data = {
#         "keywords": keywords,
#         "page": page,
#         "xqid": 0,
#         "starttime": starttime,
#         "endtime": endtime
#     }
#     response_data = scrape_data(url, data)
    
#     return render_template('community_details.html', 
#                          data=response_data, 
#                          page=page,
#                          keywords=keywords,
#                          starttime=starttime,
#                          endtime=endtime)

# @main.route('/add-email', methods=['POST'])
# @login_required
# def add_email_subscription():
#     email = request.form.get('email')
#     if not email:
#         return jsonify({'status': 'error', 'message': '邮箱不能为空'}), 400
        
#     # 检查当前用户是否已订阅该邮箱
#     if EmailSubscription.query.filter_by(
#         email=email,
#         user_id=current_user.id
#     ).first():
#         return jsonify({'status': 'error', 'message': '您已订阅该邮箱'}), 400
        
#     try:
#         # 创建新的订阅，设置当前用户ID
#         subscription = EmailSubscription(
#             email=email,
#             user_id=current_user.id  # 设置当前登录用户的ID
#         )
#         db.session.add(subscription)
#         db.session.commit()
#         return jsonify({
#             'status': 'success',
#             'message': '添加成功',
#             'data': {'id': subscription.id, 'email': subscription.email}
#         })
#     except Exception as e:
#         db.session.rollback()
#         print(f"添加邮箱错误: {e}")
#         return jsonify({'status': 'error', 'message': '添加失败，请重试'}), 500

# @main.route('/delete-email/<int:email_id>', methods=['POST'])
# @login_required
# def delete_email(email_id):
#     email_sub = EmailSubscription.query.get_or_404(email_id)
#     db.session.delete(email_sub)
#     db.session.commit()
#     return jsonify({'success': True})

# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
        
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
        
#         user = User.query.filter_by(email=email).first()
        
#         if user and user.verify_password(password):
#             login_user(user)
#             next_page = request.args.get('next')
#             if next_page:
#                 return redirect(next_page)
#             return redirect(url_for('main.index'))
#         else:
#             flash('邮箱或密码错误')
            
#     return render_template('login.html')

# @main.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
        
#         # 检查用户名是否已存在
#         if User.query.filter_by(username=username).first():
#             flash('用户名已存在')
#             return redirect(url_for('main.register'))
            
#         # 检查邮箱是否已被注册
#         if User.query.filter_by(email=email).first():
#             flash('邮箱已被注册')
#             return redirect(url_for('main.register'))
            
#         user = User(
#             username=username,
#             email=email
#         )
#         # user.password = password  # 使用属性设置器
#         user.password_hash = generate_password_hash(password)
        
#         # 检查是否是第一个用户
#         if User.query.count() == 0:
#             user.is_admin = True
            
#         try:
#             db.session.add(user)
#             db.session.commit()
#             login_user(user)
#             return redirect(url_for('main.index'))
#         except Exception as e:
#             db.session.rollback()
#             flash('注册失败，请重试')
#             print(f"注册错误: {e}")
#             return redirect(url_for('main.register'))
        
#     return render_template('register.html')

# @main.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('main.index'))

# @main.route('/admin')
# @login_required
# @admin_required
# def admin():
#     users = User.query.all()
#     community_subscriptions = CommunitySubscription.query.all()
#     email_subscriptions = EmailSubscription.query.all()
#     return render_template('admin.html',
#                          users=users,
#                          community_subscriptions=community_subscriptions,
#                          email_subscriptions=email_subscriptions)

# @main.route('/admin/delete-user/<int:user_id>', methods=['POST'])
# @login_required
# @admin_required
# def admin_delete_user(user_id):
#     user = User.query.get_or_404(user_id)
#     if user.id == current_user.id:
#         return jsonify({'success': False, 'message': '不能删除当前登录的管理员账号'})
    
#     try:
#         # 删除用户的所有订阅
#         CommunitySubscription.query.filter_by(user_id=user.id).delete()
#         EmailSubscription.query.filter_by(user_id=user.id).delete()
#         # 删除用户
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({'success': True})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'success': False, 'message': str(e)})

# @main.route('/admin/delete-community/<int:sub_id>', methods=['POST'])
# @login_required
# @admin_required
# def admin_delete_community(sub_id):
#     subscription = CommunitySubscription.query.get_or_404(sub_id)
#     try:
#         db.session.delete(subscription)
#         db.session.commit()
#         return jsonify({'success': True})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'success': False, 'message': str(e)})


# @main.route('/admin/delete-email/<int:email_id>', methods=['POST'])
# @login_required
# @admin_required
# def admin_delete_email(email_id):
#     email = EmailSubscription.query.get_or_404(email_id)
#     db.session.delete(email)  
#     db.session.commit()
#     return jsonify({'success': True})