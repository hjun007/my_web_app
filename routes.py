from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from crawler.simple_crawler import scrape_data
from models import db, Community, EmailSubscription
import json
import configparser
from datetime import datetime
from scheduler.task_scheduler import job

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
            return jsonify({'success': True})
    return jsonify({'success': False})

@main.route('/delete-email/<int:email_id>', methods=['POST'])
def delete_email(email_id):
    email_sub = EmailSubscription.query.get_or_404(email_id)
    db.session.delete(email_sub)
    db.session.commit()
    return jsonify({'success': True})

@main.route('/trigger-job')
def trigger_job():
    print("开始手动触发任务...")
    with current_app.app_context():
        job()
    print("任务已触发")
    return "任务已触发"
