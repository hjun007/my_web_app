from flask import render_template
from flask_login import current_user
from models import CommunitySubscription, EmailSubscription
from . import main

@main.route('/')
def index():
    if current_user.is_authenticated:
        communities = CommunitySubscription.query.filter_by(user_id=current_user.id).order_by(CommunitySubscription.created_at.desc()).all()
        emails = EmailSubscription.query.filter_by(user_id=current_user.id).order_by(EmailSubscription.created_at.desc()).all()
    else:
        communities = []
        emails = []
    return render_template('index.html', 
                         communities=[{'id': c.id, 'name': c.name} for c in communities],
                         emails=[{'id': e.id, 'email': e.email} for e in emails])

