from flask import render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from models import CommunitySubscription, EmailSubscription, db
from . import user
import configparser
from crawler.simple_crawler import scrape_data
# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

@user.route('/add-community', methods=['GET'])
def add_community_form():
    return render_template('add_community.html')

@user.route('/add-community', methods=['POST'])
@login_required
def add_community_subscription():
    community_name = request.form.get('community')
    # print(f"接收到的表单数据: {request.form}")
    if community_name:
        subscription = CommunitySubscription(
            name=community_name,
            user_id=current_user.id
        )
        db.session.add(subscription)
        db.session.commit()
        return redirect(url_for('main.index'))
    return jsonify({'success': False, 'message': '小区名称不能为空'})

@user.route('/delete-community/<int:subscription_id>', methods=['POST'])
@login_required
def delete_community_subscription(subscription_id):
    subscription = CommunitySubscription.query.get_or_404(subscription_id)
    if subscription.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'success': False, 'message': '无权限删除此订阅'})
    
    db.session.delete(subscription)
    db.session.commit()
    return jsonify({'success': True})

@user.route('/community-details')
@login_required
def community_details():
    keywords = request.args.get('keywords', '')
    page = request.args.get('page', 1, type=int)
    starttime = request.args.get('starttime', '')
    endtime = request.args.get('endtime', '')
    
    url = config.get('crawler', 'url')
    data = {
        "keywords": keywords,
        "page": page,
        "xqid": 0,
        "starttime": starttime,
        "endtime": endtime
    }
    response_data = scrape_data(url, data)
    
    return render_template('community_details.html', 
                         data=response_data, 
                         page=page,
                         keywords=keywords,
                         starttime=starttime,
                         endtime=endtime)

@user.route('/add-email', methods=['POST'])
@login_required
def add_email_subscription():
    email = request.form.get('email')
    if not email:
        return jsonify({'status': 'error', 'message': '邮箱不能为空'}), 400
        
    # 检查当前用户是否已订阅该邮箱
    if EmailSubscription.query.filter_by(
        email=email,
        user_id=current_user.id
    ).first():
        return jsonify({'status': 'error', 'message': '您已订阅该邮箱'}), 400
        
    try:
        # 创建新的订阅，设置当前用户ID
        subscription = EmailSubscription(
            email=email,
            user_id=current_user.id  # 设置当前登录用户的ID
        )
        db.session.add(subscription)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '添加成功',
            'data': {'id': subscription.id, 'email': subscription.email}
        })
    except Exception as e:
        db.session.rollback()
        print(f"添加邮箱错误: {e}")
        return jsonify({'status': 'error', 'message': '添加失败，请重试'}), 500

@user.route('/delete-email/<int:email_id>', methods=['POST'])
@login_required
def delete_email(email_id):
    email_sub = EmailSubscription.query.get_or_404(email_id)
    db.session.delete(email_sub)
    db.session.commit()
    return jsonify({'success': True})