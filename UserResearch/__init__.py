import os
import click
from flask import Flask
from flask.cli import AppGroup
from UserResearch.login import login_init_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from UserResearch.models import db, create_db

app = Flask(__name__)
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate(app, db)

def config_db(db_uri='sqlite:///db/site.db'):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True # uncomment for SQL debug
    # app.config['PROFILE'] = True # uncomment for profiling
    if app.config.get('PROFILE', False): # pragma: no cover
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.secret_key = "2d9246a23f9992d46a24ee2b8feb73b1"
    db.init_app(app)
    db.create_all(app=app)
    # create_db()

def config_sass():
    #Converting Sass file to Css
    scss = Bundle('scss/main.scss', filters='pyscss', output='styles/css/main.css')
    #SCSS Connection
    assets = Environment(app)
    assets.url= app.static_url_path
    assets.debug=True
    assets.register('scss_main', scss)

def config_mailserver():
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'tiggaa.wilkinson@gmail.com'
    MAIL_PASSWORD = 'sqnaiejvhfkveesn'

def config_other():
    app.config['RAPID_REFRESH'] = os.environ.get('RAPID_REFRESH', 30)
    app.config['RAPID_GRID_SYSTEM'] = os.environ.get('RAPID_GRID_SYSTEM', 'MGRS')

def config_login():
    login_init_app(app)

config_db()
config_mailserver()
config_other()
config_login()
from UserResearch import routes

db_cli = AppGroup('db')

@db_cli.command('init')
def db_init(): # pragma: no cover
    try: os.mkdir('UserResearch/db')
    except: pass
    from UserResearch.models import create_db
    create_db()

@db_cli.command('demo')
def db_demo(): # pragma: no cover
    from UserResearch.models import create_demo_data
    create_demo_data()

@db_cli.command('save')
@click.argument('dir')
def db_save(dir): # pragma: no cover
    from UserResearch.models import TABLES_TO_SAVE, table_to_csv_file
    for table in TABLES_TO_SAVE:
        filename = table.__name__ + '.csv'
        filename = os.path.join(dir, filename)
        with open(filename, 'w', newline='') as file:
            table_to_csv_file(table, file)

app.cli.add_command(db_cli)
