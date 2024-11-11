from flask import render_template, jsonify
from flask_login import login_required, current_user
from models import User, CommunitySubscription, EmailSubscription, db
from . import admin
from functools import wraps
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'success': False, 'message': '无权限访问'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def admin_index():
    users = User.query.all()
    community_subscriptions = CommunitySubscription.query.all()
    email_subscriptions = EmailSubscription.query.all()
    return render_template('admin.html',
                         users=users,
                         community_subscriptions=community_subscriptions,
                         email_subscriptions=email_subscriptions)

@admin.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': '不能删除当前登录的管理员账号'})
    
    try:
        # 删除用户的所有订阅
        CommunitySubscription.query.filter_by(user_id=user.id).delete()
        EmailSubscription.query.filter_by(user_id=user.id).delete()
        # 删除用户
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@admin.route('/delete-community/<int:sub_id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_community(sub_id):
    subscription = CommunitySubscription.query.get_or_404(sub_id)
    try:
        db.session.delete(subscription)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@admin.route('/delete-email/<int:email_id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_email(email_id):
    email = EmailSubscription.query.get_or_404(email_id)
    db.session.delete(email)  
    db.session.commit()
    return jsonify({'success': True})