from UserResearch import db, app
from UserResearch.models import (User_type, User, Post, Rank, Service,
                                Service_type, Worker_type, Team, Project,
                                TeamMembers )

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

def create_UserType():
    with app.app_context():
        NYA = User_type(acctType='Not Yet Authorised')
        VO = User_type(acctType='View Only')
        SU = User_type(acctType='Standard User')
        A = User_type(acctType='Administrator')
        db.session.add_all([NYA, VO, SU, A])
        db.session.commit()

def create_Users():
    with app.app_context():
        U1 = User(username='Tiggaa', email='tiggaa.wilkinson@gmail.com', image_file='cc2ebda55a3bfbef.jpeg', password='$2b$12$JQITd7koKi7z/aXbG4gQf.lfD0V.Xwmd7oxleIfvaq7/zwUXoJfWm', acctType_id=4)
        U2 = User(username='Tiggaa3', email='tig.gaawilkinson@gmail.com', image_file='cc2ebda55a3bfbef.jpeg', password='$2b$12$JQITd7koKi7z/aXbG4gQf.lfD0V.Xwmd7oxleIfvaq7/zwUXoJfWm', acctType_id=3)
        U3 = User(username='Tiggaa2', email='tigg.aawilkinson@gmail.com', image_file='cc2ebda55a3bfbef.jpeg', password='$2b$12$JQITd7koKi7z/aXbG4gQf.lfD0V.Xwmd7oxleIfvaq7/zwUXoJfWm', acctType_id=2)
        U4 = User(username='Tiggaa1', email='tiggaawilkinson@gmail.com', image_file='cc2ebda55a3bfbef.jpeg', password='$2b$12$JQITd7koKi7z/aXbG4gQf.lfD0V.Xwmd7oxleIfvaq7/zwUXoJfWm', acctType_id=1)
        db.session.add_all([U1, U2, U3, U4])
        db.session.commit()

def create_ranks():
    with app.app_context():
        OR1 = Rank(nato_rank='OR1', description='Recruit' )
        OR2 = Rank(nato_rank='OR2', description='Pte, Cfn, Kgn' )
        OR3 = Rank(nato_rank='OR3', description='LCpl, LBdr' )
        OR4 = Rank(nato_rank='OR4', description='Cpl' )
        OR6 = Rank(nato_rank='OR6', description='Sgt' )
        OR7 = Rank(nato_rank='OR7', description='SSgt, CSgt, FSgt' )
        OR8 = Rank(nato_rank='OR8', description='WO2' )
        OR9 = Rank(nato_rank='OR9', description='WO1' )
        OF1 = Rank(nato_rank='OF1', description='Lt' )
        OF2 = Rank(nato_rank='OF2', description='Capt, Flt Lt' )
        OF3 = Rank(nato_rank='OF3', description='Maj, Sqn Ldr' )
        OF4 = Rank(nato_rank='OF4', description='Lt Col, Wg Cmdr' )
        OF5 = Rank(nato_rank='OF5', description='Col, Gp Capt' )
        OF6 = Rank(nato_rank='OF6', description='Brig' )
        OF7 = Rank(nato_rank='OF7', description='Maj Gen' )
        OF8 = Rank(nato_rank='OF8', description='Lt Gen' )
        OF9 = Rank(nato_rank='OF9', description='Gen' )
        db.session.add_all([OR1, OR2, OR3, OR4, OR6, OR7, OR8, OR9, OF1, OF2, OF3, OF4, OF5, OF6, OF7, OF8, OF9])
        db.session.commit()

def create_service():
    with app.app_context():
        RN = Service(service='Royal Navy')
        RM = Service(service='Royal Marine')
        A = Service(service='Army')
        RAF = Service(service='RAF')
        CS = Service(service='Civil Service')
        db.session.add_all([ RN, RM, A, RAF, CS ])
        db.session.commit()

def create_service_type():
    with app.app_context():
        S1 = Service_type(service_type='Regular')
        S2 = Service_type(service_type='Reserve')
        S3 = Service_type(service_type='FTRS(FC)')
        S4 = Service_type(service_type='FTRS(LC)')
        S5 = Service_type(service_type='Called Out Reserve')
        S6 = Service_type(service_type='Civil Service')
        db.session.add_all([ S1, S2, S3, S4, S5, S6 ])
        db.session.commit()

def create_worker_type():
    with app.app_context():
        W1 = Worker_type(worker_type='Office Worker')
        W2 = Worker_type(worker_type='Occasional Access to ModNet')
        W3 = Worker_type(worker_type='Limited Access to ModNet')
        db.session.add_all([ W1, W2, W3 ])
        db.session.commit()


config_db()
create_UserType()
create_Users()
create_ranks()
create_service()
create_service_type()
create_worker_type()
