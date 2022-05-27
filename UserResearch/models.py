from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (func, CheckConstraint, and_)
from flask import current_app
from flask_login import UserMixin

db=SQLAlchemy()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class User_type(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    acctType    = db.Column(db.String(10), unique=True, nullable=False)
    UserType    = db.relationship('User', backref='acctType', lazy=True)

    def __repr__(self): # pragma: no cover
        return f"Account_Type('{self.id}','{self.acctType}')"

class User(db.Model, UserMixin):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(20), unique=True, nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    image_file  = db.Column(db.String(20), nullable=False, default='default.jpg')
    password    = db.Column(db.String(60), nullable=False)
    posts       = db.relationship('Post', backref='author', lazy=True)
    acctType_id = db.Column(db.Integer, db.ForeignKey('user_type.id'))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.acctType}')"

class Post(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content     = db.Column(db.Text, nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    project_name= db.Column(db.String(100), nullable=False)
    project_description= db.Column(db.Text, nullable=False)
    project_team= db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

class Team(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    team        = db.Column(db.String(100), nullable=False)
    team_desc   = db.Column(db.Text, nullable=False)

class TeamMembers(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    team        = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    members     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Rank(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    nato_rank   = db.Column(db.String(5), nullable=False)
    description = db.Column(db.String(20), nullable=False)

class Service(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    service     = db.Column(db.String(5), nullable=False)

class Service_type(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(5), nullable=False)

class Worker_type(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    worker_type = db.Column(db.String(5), nullable=False)

class Persona(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    project_id  = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    image_file  = db.Column(db.String(20), nullable=False, default='default.jpg')
    job_title   = db.Column(db.String(100), nullable=False)
    job_role    = db.Column(db.String(100), nullable=False)
    lower_rank  = db.Column(db.Integer, db.ForeignKey('rank.id'), nullable=False)
    higher_rank = db.Column(db.Integer, db.ForeignKey('rank.id'), nullable=False)
    profile_narrative = db.Column(db.Text, nullable=False)
    name        = db.Column(db.String(100), nullable=False)
    age         = db.Column(db.Float)
    service     = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    service_type= db.Column(db.Integer, db.ForeignKey('service_type.id'), nullable=False)
    worker_type = db.Column(db.Integer, db.ForeignKey('worker_type.id'), nullable=False)
    length_of_service = db.Column(db.Float)
    location    = db.Column(db.String(100), nullable=False)
    hobbies     = db.Column(db.String(100), nullable=False)
    personality = db.Column(db.String(100), nullable=False)
    internet_primary_use = db.Column(db.String(100), nullable=False)
    internet_favourite_sites = db.Column(db.String(100), nullable=False)
    internet_computer = db.Column(db.String(100), nullable=False)
    tool_req_scalable_training = db.Column(db.Float)
    tool_req_tool_training = db.Column(db.Float)
    tool_req_tool_awareness = db.Column(db.Float)
    tool_req_tool_knowledge = db.Column(db.Float)
    tool_req_data_input_req = db.Column(db.Float)
    user_goals  = db.Column(db.String(100), nullable=False)
    business_goals = db.Column(db.String(100), nullable=False)




"""
Assumes is already within app context.
"""
INIT_TABLES = [
    User_type,
    # User,
    # Post
]

INIT_DIRECTORY_NAME = "UserResearch/db/initial"

def create_db():
    try: db.drop_all()
    except: pass # pragma: no cover
    from UserResearch import app
    db.create_all(app=app)
    import csv
    import os
    with app.app_context():
        for table in INIT_TABLES:
            filename = table.__name__ + '.csv'
            filename = os.path.join(INIT_DIRECTORY_NAME, filename)
            with open(filename, newline='') as file:
                for row in csv.DictReader(file):
                    db.session.add(table(**row))
        db.session.commit()

DIRECTORY_NAME = "test/data"

def create_demo_data():
    import os
    for table in TABLES_TO_SAVE:
        filename = table.__name__ + '.csv'
        filename = os.path.join(DIRECTORY_NAME, filename)
        with open(filename, newline='') as file:
            csv_file_to_table(table, file, True)
