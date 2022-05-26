from flask import render_template, request, Blueprint
from UserResearch.models import Post, User
from UserResearch.login import login_manager, hash_generate, hash_check
from UserResearch.util import accounts_forbidden

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@main.route("/")
@main.route("/home")
@accounts_forbidden([1, 2])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)

@main.route("/about")
@accounts_forbidden([1, 2])
def about():
    return render_template('about.html', title='About')
