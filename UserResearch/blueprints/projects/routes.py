from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from UserResearch import db, bcrypt
from UserResearch.util import accounts_forbidden
from UserResearch.models import Project, Persona
from .forms import CreateProjectForm

projects = Blueprint('projects', __name__)

@projects.route("/add_project", methods=['GET', 'POST'])
@accounts_forbidden([1, 2])
def add():
    form = CreateProjectForm()
    if form.validate_on_submit():
        project = Project(project_name=form.project_name.data, project_description=form.project_description.data, project_team=form.project_team.data)
        db.session.add(project)
        db.session.commit()
        flash(f'Your project has been created!', 'success')
        return redirect(url_for('projects.list'))
    return render_template('project/add.html', title='Add Project', form=form)

@projects.route("/projects", methods=['GET'])
@accounts_forbidden([1, 2])
def list():
    Projects = Project.query.all()
    return render_template('project/list.html', title='Projects', Projects=Projects)

@projects.route("/project/<int:project_id>/edit", methods=['GET', 'POST'])
@accounts_forbidden([1, 2])
def edit(project_id):
    project = Project.query.get_or_404(project_id)
    form = CreateProjectForm()
    if form.validate_on_submit():
        project.project_name            =form.project_name.data
        project.project_description     =form.project_description.data
        project.project_team            =form.project_team.data
        db.session.commit()
        flash(f'Your project has been updated!', 'success')
        return redirect(url_for('projects.list'))
    elif request.method == 'GET':
        form.project_name.data          =project.project_name
        form.project_description.data   =project.project_description
        form.project_team.data          =project.project_team
    return render_template('project/add.html', title='Update Project', project=project, form=form)

@projects.route("/project/<int:project_id>/view", methods=['GET', 'POST'])
@accounts_forbidden([1, 2])
def view(project_id):
    project = Project.query.get_or_404(project_id)
    form = CreateProjectForm()
    if form.validate_on_submit():
        project.project_name            =form.project_name.data
        project.project_description     =form.project_description.data
        project.project_team            =form.project_team.data
        db.session.commit()
        flash(f'Your project has been updated!', 'success')
        return redirect(url_for('projects.list'))
    elif request.method == 'GET':
        form.project_name.data          =project.project_name
        form.project_description.data   =project.project_description
        form.project_team.data          =project.project_team
    return render_template('project/add.html', title='Edit Project', form=form)

@projects.route("/project/<int:id>/delete", methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    if (project.persona != []):
        flash(f'You cannot delete the project whilst personas are allocated!', 'danger')
        return redirect(url_for('projects.edit', project_id=id))
    else:
        db.session.delete(project)
        db.session.commit()
        flash(f'Your project has been deleted!', 'success')
        return redirect(url_for('projects.list'))
