from functools import wraps
from flask import session, redirect, url_for, flash
from blueprints.users.models import User
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect('/user/login')  # Redirect to the login page if not logged in
        return f(*args, **kwargs)

    return decorated_function

def subscription_plan(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user=User.query.filter_by(id=session['user_id']).first()
        value=user.subscription
        langcode = kwargs.get('langcode', '') 
        if value == 0 and langcode == 'te':
            flash('Please subscribe to avail feature', 'error')
            return redirect('/#pricing')
        return f(value,*args, **kwargs)
    return decorated_function
