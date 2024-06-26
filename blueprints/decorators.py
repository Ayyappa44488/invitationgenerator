from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect('/user/login')  # Redirect to the login page if not logged in
        return f(*args, **kwargs)

    return decorated_function
