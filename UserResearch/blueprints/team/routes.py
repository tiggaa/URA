from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from UserResearch import db, bcrypt
from UserResearch.util import accounts_forbidden
from UserResearch.models import Team, TeamMembers, User
from .forms import CreateTeam_Form, AddTeamMembers_Form

team = Blueprint('team', __name__)

@team.route("/team/add", methods=['GET', 'POST'])
@accounts_forbidden([1, 2, 3])
def add():
    form = CreateTeam_Form()
    if form.validate_on_submit():
        team = Team(
                team        =form.team.data,
                team_desc   =form.team_desc.data)
        db.session.add(team)
        db.session.commit()
        flash(f'The team has been created!', 'success')
        return redirect(url_for('team.list'))
    return render_template('team/add.html', title='Add Team', form=form)

@team.route("/teams", methods=['GET'])
@accounts_forbidden([1, 2, 3])
def list():
    teams = Team.query.all()
    return render_template('team/list.html', title='Teams', teams=teams)

@team.route("/team/<int:id>/update", methods=['GET', 'POST'])
@accounts_forbidden([1, 2, 3])
def edit(id):
    team = Team.query.get_or_404(id)

    members = []
    member_IDs = []
    member_IDs = TeamMembers.query.filter_by(team=id)

    for member_ID in member_IDs:
        member = User.query.get_or_404(member_ID.members)
        members.append(member)

    form =  CreateTeam_Form()
    if form.validate_on_submit():
        team.team      =form.team.data
        team.team_desc =form.team_desc.data
        db.session.commit()
        flash(f'Your Team has been updated!', 'success')
        return redirect(url_for('team.list'))
    elif request.method == 'GET':
        form.team.data       =team.team
        form.team_desc.data  =team.team_desc

    # Add New Team Member
    users = User.query.all()
    user_list = [(i.id, i.username) for i in users]
    form2 = AddTeamMembers_Form()
    form2.member.choices = user_list
    if form2.validate_on_submit():
        new_member = User.query.get_or_404(form2.member.data)
        members = []
        member_IDs = []
        member_IDs = TeamMembers.query.filter_by(team=id)
        for member_ID in member_IDs:
            member = User.query.get_or_404(member_ID.members)
            members.append(member)
        if (new_member not in members):
            member = TeamMembers(
                team = id,
                members = form2.member.data)
            db.session.add(member)
            db.session.commit()
            flash(f'Member has been added!', 'success')
        else:
            flash(f'User is already a member!', 'danger')
        return redirect(url_for('team.edit', id=id))
    return render_template('team/add.html', title='Update Team', members=members, team=team, form2=form2, form=form)

@team.route("/team/<int:id>/<int:team>/remove_member", methods=['GET'])
@accounts_forbidden([1, 2, 3])
def remove_member(id, team):
    members = TeamMembers.query.filter_by(members=id).first()
    print(members)
    db.session.delete(members)
    db.session.commit()
    flash(f'The Team Member has been removed!', 'success')
    return redirect(url_for('team.edit', id=team))

@team.route("/team/<int:id>/view", methods=['GET'])
@accounts_forbidden([1, 2, 3])
def view(id):
    team = Team.query.get_or_404(id)

    members = []
    member_IDs = []
    member_IDs = TeamMembers.query.filter_by(team=id)

    for member_ID in member_IDs:
        member = User.query.get_or_404(member_ID.members)
        members.append(member)

    form = CreateTeam_Form()
    if request.method == 'GET':
        form.team.data       =team.team
        form.team_desc.data  =team.team_desc
    return render_template('team/view.html', title='View Team', members=members, team=team, form=form)

@team.route("/team/<int:id>/delete", methods=['POST'])
@accounts_forbidden([1, 2, 3])
def delete_team(id):
    team = Team.query.get_or_404(id)
    if (team.TeamMembers != []):
        flash(f'You cannot delete a Team whilst Members are allocated!', 'danger')
        return redirect(url_for('team.edit', id=id))
    else:
        db.session.delete(team)
        db.session.commit()
        flash(f'Your Team has been deleted!', 'success')
        return redirect(url_for('team.list'))
