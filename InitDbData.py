from UserResearch import db, app
from UserResearch.models import (User_type, User, Post, Rank, Service,
                                Service_type, Worker_type, Team, Project,
                                TeamMembers, User_storey, Acceptance )

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
        P2 = TeamMembers(team=1, members=2)
        db.session.add_all([ P1, P2 ])
        db.session.commit()

def create_persona():
    with app.app_context:
        P1 = Persona(project_id=1,
                    job_title='Application Developer',
                    job_role='Develope Applications',
                    lower_rank=7,
                    higher_rank=8,
                    profile_narrative='Creation of applications with the user at the centre',
                    name='Stan Lee',
                    age=98,
                    service=2,
                    service_type=1,
                    worker_type=1,
                    length_of_service=30,
                    location='Gosport',
                    hobbies='Coding',
                    personality='Intervert',
                    internet_primary_use='Research',
                    internet_favourite_sites='Google',
                    internet_computer='MacBookPro',
                    tool_req_scalable_training = 80,
                    tool_req_tool_training = 60,
                    tool_req_tool_awareness = 40,
                    tool_req_tool_knowledge = 30,
                    tool_req_data_input_req = 45,
                    user_goals='Make it easy to follow agile process',
                    business_goals='Transition to a agile methodology' )
        db.session.add_all([ P1 ])
        db.session.commit()

def create_user_storey():
    with app.app_context():
        P1 = User_storey(who=1, what='test the user storey create function', in_order='make sure it works')
        P2 = User_storey(who=1, what='test all DbData create functions', in_order='make sure they work')
        db.session.add_all([ P1, P2 ])
        db.session.commit()

def create_Acceptance():
    with app.app_context():
        P1 = Acceptance(given='a new instance', when='I run python InitDbData.py', then='the new user stories are created', ur_id=1)
        P2 = Acceptance(given='a new instance', when='I run python InitDbData.py', then='the new user stories are created', ur_id=1)
        P3 = Acceptance(given='a new instance', when='I run python InitDbData.py', then='the new user stories are created', ur_id=2)
        db.session.add_all([ P1, P2, P3 ])
        db.session.commit()


create_posts()
create_team()
create_team_members()
create_project()
create_persona()
create_user_storey()
create_Acceptance()
