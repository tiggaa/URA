from UserResearch import db, app
from UserResearch.models import (User_type, User, Post, Rank, Service,
                                Service_type, Worker_type, Team, Project,
                                TeamMembers )

def create_posts():
    with app.app_context():
        P1 = Post(title='Imported Title 1', content='Imported Content', user_id=1 )
        P2 = Post(title='Imported Title 2', content='Imported Content', user_id=1 )
        P3 = Post(title='Imported Title 3', content='Imported Content', user_id=1 )
        P4 = Post(title='Imported Title 4', content='Imported Content', user_id=1 )
        db.session.add_all([P1, P2, P3, P4])
        db.session.commit()

def create_team():
    with app.app_context():
        P1 = Team(team='Admin', team_desc='Admin Team')
        db.session.add_all([ P1 ])
        db.session.commit()

def create_project():
    with app.app_context():
        P1 = Project(project_name='Admin Project', project_description='Starter Admin Project', project_team=1)
        db.session.add_all([ P1 ])
        db.session.commit()

def create_team_members():
    with app.app_context():
        P1 = TeamMembers(team=1, members=1)
        db.session.add_all([ P1 ])
        db.session.commit()


create_posts()
create_team()
create_team_members()
create_project()
