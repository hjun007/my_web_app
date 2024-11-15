from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from crawler.simple_crawler import scrape_data
from models import db, Community, EmailSubscription
import configparser
from datetime import datetime
from scheduler.task_scheduler import job
from globals import globals

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

main = Blueprint('main', __name__)

@main.route('/')
def hello_world():
    communities = Community.query.order_by(Community.created_at.desc()).all()
    emails = EmailSubscription.query.order_by(EmailSubscription.created_at.desc()).all()
    return render_template('index.html', 
                         communities=[{'id': c.id, 'name': c.name} for c in communities],
                         emails=[{'id': e.id, 'email': e.email} for e in emails])

@main.route('/delete-subscription/<int:community_id>', methods=['POST'])
def delete_subscription(community_id):
    community = Community.query.get_or_404(community_id)
    db.session.delete(community)
    db.session.commit()
    current_app.logger.info(f"删除小区订阅: {community_id}")
    return jsonify({'success': True})

@main.route('/community-details')
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

@main.route('/add-subscription', methods=['GET', 'POST'])
def add_subscription():
    if request.method == 'POST':
        community_name = request.form.get('community')
        if community_name:
            # 检查是否已存在
            existing = Community.query.filter_by(name=community_name).first()
            if not existing:
                new_community = Community(name=community_name)
                db.session.add(new_community)
                db.session.commit()
                current_app.logger.info(f"添加小区订阅: {community_name}")
            return redirect(url_for('main.hello_world'))
    return render_template('add_subscription.html')

@main.route('/scraped-data')
def scraped_data():
    url = config.get('crawler', 'url')
    page = request.args.get('page', 1, type=int)
    data = {
        "keywords": config.get('crawler', 'keywords'),
        "page": page,
        "xqid": 0
    }
    response_data = scrape_data(url, data)
    return render_template('scraped_data.html', data=response_data, page=page)

@main.route('/add-email', methods=['POST'])
def add_email():
    email = request.form.get('email')
    if email:
        existing = EmailSubscription.query.filter_by(email=email).first()
        if not existing:
            new_subscription = EmailSubscription(email=email)
            db.session.add(new_subscription)
            db.session.commit()
            current_app.logger.info(f"添加邮箱订阅: {email}")
            return jsonify({'success': True})
    current_app.logger.info(f"添加邮箱订阅失败: {email}")
    return jsonify({'success': False})

@main.route('/delete-email/<int:email_id>', methods=['POST'])
def delete_email(email_id):
    email_sub = EmailSubscription.query.get_or_404(email_id)
    db.session.delete(email_sub)
    db.session.commit()
    current_app.logger.info(f"删除邮箱订阅: {email_id}")
    return jsonify({'success': True})

@main.route('/trigger-job')
def trigger_job():
    print("开始手动触发任务...")
    with current_app.app_context():
        job()
    print("任务已触发")
    return "任务已触发"

@main.route('/update-push-time', methods=['POST'])
def update_push_time():
    try:
        push_hour = int(request.form.get('push_hour', 22))
        push_minute = int(request.form.get('push_minute', 0))
        
        # 验证输入
        if not (0 <= push_hour <= 23 and 0 <= push_minute <= 59):
            raise ValueError('无效的时间值')
            
        globals.update_push_time(push_hour, push_minute)
        
        current_app.logger.info(f"推送时间已更新为: {push_hour}:{push_minute}")
        return jsonify({
            'success': True,
            'hour': push_hour,
            'minute': push_minute
        })
    except Exception as e:
        current_app.logger.error(f"更新推送时间失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@main.route('/get-push-time')
def get_push_time():
    try:
        current_app.logger.info(f"获取推送时间: {globals.push_time['hour']}:{globals.push_time['minute']}")
        return jsonify({
            'success': True,
            'hour': globals.push_time['hour'],
            'minute': globals.push_time['minute']
        })
    except Exception as e:
        current_app.logger.error(f"获取推送时间失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })
