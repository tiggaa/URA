from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from UserResearch import db, bcrypt
from UserResearch.util import accounts_forbidden
from UserResearch.models import Project
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
    print(Projects)
    return render_template('project/list.html', title='Projects', Projects=Projects)
