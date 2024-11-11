from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db
from werkzeug.security import generate_password_hash
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.verify_password(password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('邮箱或密码错误')
            
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('auth.register'))
            
        # 检查邮箱是否已被注册
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册')
            return redirect(url_for('auth.register'))
            
        user = User(
            username=username,
            email=email
        )
        # user.password = password  # 使用属性设置器
        user.password_hash = generate_password_hash(password)
        
        # 检查是否是第一个用户
        if User.query.count() == 0:
            user.is_admin = True
            
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('注册失败，请重试')
            print(f"注册错误: {e}")
            return redirect(url_for('auth.register'))
        
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))