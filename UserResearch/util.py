from flask_login import current_user, login_required
from flask import (
    request,
    redirect,
    flash,
    url_for,
)
from functools import wraps
from UserResearch import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def accounts_forbidden(disallowed):
    def _inner(func):
        @login_required
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.accountType_id in disallowed:
                requestedPage = request.url
                flash(f'ACCESS DENIED! You do not have the correct permissions to access: {requestedPage}', 'danger')
                return redirect(url_for('user.splash'))
            return func(*args, **kwargs)
        return decorated_view
    return _inner
