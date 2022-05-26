from flask_login import current_user, login_required
from flask import (
    request,
    redirect,
    flash,
    url_for,
)
from functools import wraps
from UserResearch import login_manager, app

"""
CUSTOM TEMPLATE FILTERS
"""
@app.template_filter('dtg_format')
def dtg_format(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%d%H%MZ%b%y').upper()
    else:
        return obj

@app.template_filter('iso_8601_format')
def iso_8601_format(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M').upper()
    else:
        return obj

@app.template_filter('dict_but')
def dict_but(d, **kwargs):
    return { **d, **kwargs }

@app.template_filter('dict_except')
def dict_except(d, excepting):
    return { k: d[k] for k in d if k not in excepting }

"""
CUSTOM FORM FUNCTIONS (NOT DECORATORS)
"""

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def accounts_forbidden(disallowed):
    def _inner(func):
        @login_required
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.acctType_id in disallowed:
                requestedPage = request.url
                flash(f'ACCESS DENIED! You do not have the correct permissions to access: {requestedPage}', 'danger')
                return redirect(url_for('users.splash'))
            return func(*args, **kwargs)
        return decorated_view
    return _inner
