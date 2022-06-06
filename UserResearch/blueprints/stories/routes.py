from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from UserResearch import db, bcrypt
from UserResearch.util import accounts_forbidden
from UserResearch.models import User_storey, Persona
from .forms import CreateStorey_Form

stories = Blueprint('stories', __name__)

@stories.route("/stories/add", methods=['GET', 'POST'])
@accounts_forbidden([1, 2])
def add():
    personas = Persona.query.all()
    persona_list = [(i.id, i.job_title) for i in personas]
    form = CreateStorey_Form()
    form.who.choices = persona_list
    if form.validate_on_submit():
        storey = User_storey(
                    who         =form.who.data,
                    what        =form.what.data,
                    in_order    =form.in_order.data)
        db.session.add(storey)
        db.session.commit()
        flash(f'Your storey has been created!', 'success')
        return redirect(url_for('stories.list'))
    return render_template('stories/add.html', title='Add Storey', form=form)

@stories.route("/stories", methods=['GET'])
@accounts_forbidden([1, 2])
def list():
    stories = User_storey.query.all()
    return render_template('stories/list.html', title='User Stories', stories=stories)

@stories.route("/stories/<int:id>/update", methods=['GET', 'POST'])
@accounts_forbidden([1, 2])
def edit(id):
    stories = User_storey.query.get_or_404(id)
    personas = Persona.query.all()
    persona_list = [(i.id, i.job_title) for i in personas]
    form = CreateStorey_Form()
    form.who.choices = persona_list
    if form.validate_on_submit():
        stories.who      =form.who.data
        stories.what     =form.what.data
        stories.in_order =form.in_order.data
        db.session.commit()
        flash(f'Your User Storey has been updated!', 'success')
        return redirect(url_for('stories.list'))
    elif request.method == 'GET':
        form.who.data       =stories.who
        form.what.data      =stories.what
        form.in_order.data  =stories.in_order
    return render_template('stories/add.html', title='Update User Storey', stories=stories, form=form)

@stories.route("/stories/<int:id>/view", methods=['GET'])
@accounts_forbidden([1, 2])
def view(id):
    stories = User_storey.query.get_or_404(id)
    personas = Persona.query.all()
    persona_list = [(i.id, str(i.id) + " - " + i.job_title) for i in personas]
    form = CreateStorey_Form()
    form.who.choices = persona_list
    if request.method == 'GET':
        form.who.data       =stories.who
        form.what.data      =stories.what
        form.in_order.data  =stories.in_order
    return render_template('stories/view.html', title='View User Storey', stories=stories, form=form)

@stories.route("/stories/<int:id>/delete", methods=['POST'])
@login_required
def delete_storey(id):
    stories = User_storey.query.get_or_404(id)
    print("Acceptance: " + str(stories.acceptance))
    if (stories.acceptance != []):
        flash(f'You cannot delete the User storey whilst acceptance creatia is allocated!', 'danger')
        return redirect(url_for('stories.edit', id=id))
    else:
        db.session.delete(stories)
        db.session.commit()
        flash(f'Your User Storey has been deleted!', 'success')
        return redirect(url_for('stories.list'))
