from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from UserResearch import db, bcrypt
from UserResearch.util import accounts_forbidden
from UserResearch.models import Persona, Project, Rank, Service, Service_type, Worker_type
from .forms import AddPersonaForm

personas = Blueprint('personas', __name__)

@personas.route("/add_persona", methods=['GET', 'POST'])
@accounts_forbidden([1, 2])
def add():
    # Search for dynamic Choices
    projects = Project.query.all()
    project_list = [(i.id, str(i.id) + " - " + i.project_name) for i in projects]
    ranks = Rank.query.all()
    rank_list = [(i.id, i.nato_rank + ' - ' + i.description) for i in ranks]
    services = Service.query.all()
    service_list = [(i.id, i.service) for i in services]
    service_types = Service_type.query.all()
    service_types_list = [(i.id, i.service_type) for i in service_types]
    worker_types = Worker_type.query.all()
    worker_type_list = [(i.id, i.worker_type) for i in worker_types]
    form = AddPersonaForm()
    form.project_id.choices = project_list
    form.lower_rank.choices = rank_list
    form.higher_rank.choices = rank_list
    form.service.choices = service_list
    form.service_type.choices = service_types_list
    form.worker_type.choices = worker_type_list
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = 'default.jpeg'
        persona = Persona(
            project_id                  = form.project_id.data,
            image_file                  = picture_file,
            job_title                   = form.job_title.data,
            job_role                    = form.job_role.data,
            lower_rank                  = form.lower_rank.data,
            higher_rank                 = form.higher_rank.data,
            profile_narrative           = form.profile_narrative.data,
            name                        = form.name.data,
            age                         = form.age.data,
            service                     = form.service.data,
            service_type                = form.service_type.data,
            worker_type                 = form.worker_type.data,
            length_of_service           = form.length_of_service.data,
            location                    = form.location.data,
            hobbies                     = form.hobbies.data,
            personality                 = form.personality.data,
            internet_primary_use        = form.internet_primary_use.data,
            internet_favourite_sites    = form.internet_favourite_sites.data,
            internet_computer           = form.internet_computer.data,
            tool_req_scalable_training  = form.tool_req_scalable_training.data,
            tool_req_tool_training      = form.tool_req_tool_training.data,
            tool_req_tool_awareness     = form.tool_req_tool_awareness.data,
            tool_req_tool_knowledge     = form.tool_req_tool_knowledge.data,
            tool_req_data_input_req     = form.tool_req_data_input_req.data,
            user_goals                  = form.user_goals.data,
            business_goals              = form.business_goals.data,
            )
        db.session.add(persona)
        db.session.commit()
        flash(f'Your persona has been created!', 'success')
        return redirect(url_for('personas.list'))
    return render_template('personas/add.html', title='Create Persona', form=form)

@personas.route("/personas", methods=['GET'])
@accounts_forbidden([1, 2])
def list():
    personas = Persona.query.all()
    return render_template('personas/list.html', title='Personas', personas=personas)

@personas.route("/<int:id>/view_persona", methods=['GET'])
@accounts_forbidden([1, 2])
def view_persona(id):
    persona = Persona.query.get_or_404(id)
    image_file = url_for('static', filename='persona_pics/' + persona.image_file)
    lower = Rank.query.get_or_404(persona.lower_rank)
    upper = Rank.query.get_or_404(persona.higher_rank)
    return render_template('personas/view.html', title='Personas', image_file=image_file, lower=lower, upper=upper, persona=persona)

@personas.route("/<int:id>/edit_persona", methods=['GET', 'POST'])
@accounts_forbidden([1, 2])
def edit_persona(id):
    persona = Persona.query.get_or_404(id)
    # Search for dynamic Choices
    projects = Project.query.all()
    project_list = [(i.id, str(i.id) + " - " + i.project_name) for i in projects]
    ranks = Rank.query.all()
    rank_list = [(i.id, i.nato_rank + ' - ' + i.description) for i in ranks]
    services = Service.query.all()
    service_list = [(i.id, i.service) for i in services]
    service_types = Service_type.query.all()
    service_types_list = [(i.id, i.service_type) for i in service_types]
    worker_types = Worker_type.query.all()
    worker_type_list = [(i.id, i.worker_type) for i in worker_types]
    # Setup forms
    form = AddPersonaForm()
    form.project_id.choices = project_list
    form.lower_rank.choices = rank_list
    form.higher_rank.choices = rank_list
    form.service.choices = service_list
    form.service_type.choices = service_types_list
    form.worker_type.choices = worker_type_list
    # POST
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = 'default.jpeg'
        persona.project_id                  = form.project_id.data
        persona.image_file                  = picture_file
        persona.job_title                   = form.job_title.data
        persona.job_role                    = form.job_role.data
        persona.lower_rank                  = form.lower_rank.data
        persona.higher_rank                 = form.higher_rank.data
        persona.profile_narrative           = form.profile_narrative.data
        persona.name                        = form.name.data
        persona.age                         = form.age.data
        persona.service                     = form.service.data
        persona.service_type                = form.service_type.data
        persona.worker_type                 = form.worker_type.data
        persona.length_of_service           = form.length_of_service.data
        persona.location                    = form.location.data
        persona.hobbies                     = form.hobbies.data
        persona.personality                 = form.personality.data
        persona.internet_primary_use        = form.internet_primary_use.data
        persona.internet_favourite_sites    = form.internet_favourite_sites.data
        persona.internet_computer           = form.internet_computer.data
        persona.tool_req_scalable_training  = form.tool_req_scalable_training.data
        persona.tool_req_tool_training      = form.tool_req_tool_training.data
        persona.tool_req_tool_awareness     = form.tool_req_tool_awareness.data
        persona.tool_req_tool_knowledge     = form.tool_req_tool_knowledge.data
        persona.tool_req_data_input_req     = form.tool_req_data_input_req.data
        persona.user_goals                  = form.user_goals.data
        persona.business_goals              = form.business_goals.data

        db.session.commit()
        flash(f'Your persona has been updated!', 'success')
        return redirect(url_for('personas.list'))
    # GET
    elif request.method == 'GET':
        form.project_id.data                = persona.project_id
        form.picture.data                   = persona.image_file
        form.job_title.data                 = persona.job_title
        form.job_role.data                  = persona.job_role
        form.lower_rank.data                = persona.lower_rank
        form.higher_rank.data               = persona.higher_rank
        form.profile_narrative.data         = persona.profile_narrative
        form.name.data                      = persona.name
        form.age.data                       = int(persona.age)
        form.service.data                   = persona.service
        form.service_type.data              = persona.service_type
        form.worker_type.data               = persona.worker_type
        form.length_of_service.data         = int(persona.length_of_service)
        form.location.data                  = persona.location
        form.hobbies.data                   = persona.hobbies
        form.personality.data               = persona.personality
        form.internet_primary_use.data      = persona.internet_primary_use
        form.internet_favourite_sites.data  = persona.internet_favourite_sites
        form.internet_computer.data         = persona.internet_computer
        form.tool_req_scalable_training.data = persona.tool_req_scalable_training
        form.tool_req_tool_training.data    = persona.tool_req_tool_training
        form.tool_req_tool_awareness.data   = persona.tool_req_tool_awareness
        form.tool_req_tool_knowledge.data   = persona.tool_req_tool_knowledge
        form.tool_req_data_input_req.data   = persona.tool_req_data_input_req
        form.user_goals.data                = persona.user_goals
        form.business_goals.data            = persona.business_goals
    return render_template('personas/add.html', title='Edit Persona', form=form)

@personas.route("/<int:id>/delete_persona", methods=['GET'])
@accounts_forbidden([1, 2])
def delete_persona(id):
    persona = Persona.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    flash(f'Your persona has been deleted!', 'success')
    return redirect(url_for('personas.list'))
