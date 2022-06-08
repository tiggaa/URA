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
    persona     = db.relationship('Persona', backref='projectList', lazy=True)

class Team(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    team        = db.Column(db.String(100), nullable=False)
    team_desc   = db.Column(db.Text, nullable=False)
    TeamMembers = db.relationship('TeamMembers', backref='teamlink', lazy=True)

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
    persona     = db.relationship('Persona', backref='serviceList', lazy=True)

class Service_type(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(5), nullable=False)
    persona     = db.relationship('Persona', backref='serviceTypeList', lazy=True)

class Worker_type(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    worker_type = db.Column(db.String(5), nullable=False)
    persona     = db.relationship('Persona', backref='workerType', lazy=True)

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
    UserStorey    = db.relationship('User_storey', backref='persona', lazy=True)

    def __repr__(self):
        return f"Persona('{self.id}', '{self.job_title}', '{self.job_role}')"


class User_storey(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    who         = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)
    what        = db.Column(db.Text, nullable=False)
    in_order    = db.Column(db.Text, nullable=False)
    acceptance  = db.relationship('Acceptance', backref='criteria', lazy=True)


    def __repr__(self):
        return f"UserStorey('{self.who}', '{self.what}', '{self.in_order}')"

class Acceptance(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    given       = db.Column(db.Text, nullable=False)
    when        = db.Column(db.Text, nullable=False)
    then        = db.Column(db.Text, nullable=False)
    ur_id       = db.Column(db.Integer, db.ForeignKey('user_storey.id'), nullable=False)
