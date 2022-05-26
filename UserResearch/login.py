from flask_login import LoginManager
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
bcrypt = Bcrypt()

_generate = bcrypt.generate_password_hash
_check = bcrypt.check_password_hash

def _generate_quick(pwd):
    return pwd

def _check_quick(hashed, pwd):
    return hashed == _generate_quick(pwd)

def hash_generate(pwd):
    return _generate(pwd)

def hash_check(hashed, pwd):
    return _check(hashed, pwd)

def use_quick_functions():
    global _generate, _check
    _generate = _generate_quick
    _check = _check_quick

def login_init_app(app):
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
