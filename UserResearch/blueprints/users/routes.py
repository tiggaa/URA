from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from UserResearch import db, bcrypt
from UserResearch.util import accounts_forbidden
from UserResearch.models import User, Post
from .forms import (RegistrationForm, LoginForm,
                    UpdateAccountForm, RequestResetForm, ResetPasswordForm,
                    AdminEdit_Form, ResetPassword_Form)
from .utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/splash")
def splash():
    return render_template('user/splash.html', title='Not Logged In')

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                acctType_id=1)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/register.html', title='Register', form=form)

@users.route("/user/add", methods=['GET', 'POST'])
@accounts_forbidden([1, 2, 3])
def add():
    form = RegistrationForm()
    if request.method == 'GET':
        pass
    elif form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                acctType_id=1)
        db.session.add(user)
        db.session.commit()
        flash('The account has been created! Please inform the user of their account details', 'success')
        return redirect(url_for('users.list'))
    return render_template('user/add.html', title='Add User', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome back {form.username.data}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login Unsuccessful! Please check your username and password', 'danger')
    return render_template('user/login.html', title='Login', form=form)

@users.route("/account", methods=['GET', 'POST'])
@accounts_forbidden([5])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.acctType.data = current_user.acctType.acctType
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user/account.html', title='Account',
                           image_file=image_file, form=form)

@users.route("/user/<string:username>")
@accounts_forbidden([1])
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user/user_posts.html', posts=posts, user=user)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.splash'))

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('user/reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/reset_token.html', title='Reset Password', form=form)

@users.route("/list", methods=['GET'])
@accounts_forbidden([1, 2])
def list():
    users = User.query.all()
    return render_template('user/list.html', title='User Management', users=users)

@users.route("/<int:user_id>/admin_edit", methods=['GET', 'POST'])
@accounts_forbidden([1, 2, 3])
def admin_edit(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminEdit_Form()
    if request.method == 'GET':
        form.username.default = user.username
        form.old_username.default = user.username
        form.email.default = user.email
        form.old_email.default = user.email
        form.accountType.default = user.acctType_id
        form.process()
    elif form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.acctType_id = form.accountType.data
        db.session.commit()
        flash('Account details have been updated!', 'success')
        return redirect(url_for('users.list'))
    return render_template('user/admin_edit.html', title='Edit User', id=user_id, form=form)

@users.route("/<int:user_id>/reset_password/", methods=['GET', 'POST'])
@login_required
def reset_password(user_id):
    if current_user.id != user_id:
        if current_user.acctType_id != 4:
            flash('ACCESS DENIED! You do not have the correct permissions to update somebody elses Password', 'danger')
            return redirect(url_for('user.splash'))
    user = User.query.get_or_404(user_id)
    form = ResetPassword_Form()
    if request.method == 'GET':
        image_file = url_for('static', filename='profile_pics/' + user.image_file)
        pass
    elif form.validate_on_submit():
        hashed_password = hash_generate(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('The password has been updated!', 'success')
        if current_user.id != user_id:
            return redirect(url_for('user.list'))
        else:
            return redirect(url_for('user.self_edit'))
    return render_template('user/reset_password.html', title='Reset Password', user=user, image_file=image_file, form=form)

@users.route("/user/<int:id>/delete", methods=['GET'])
@accounts_forbidden([1, 2, 3])
def user_delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash(f'The User has been deleted!', 'success')
    return redirect(url_for('users.list'))
