from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired

class AddPersonaForm(FlaskForm):
    project_id                  = SelectField('Project', coerce=int)
    picture                     = FileField('Persona Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    job_title                   = StringField('Job Title', validators=[DataRequired()])
    job_role                    = StringField('Job Role', validators=[DataRequired()])
    lower_rank                  = SelectField('Lower Rank', coerce=int)
    higher_rank                 = SelectField('Lower Rank', coerce=int)
    profile_narrative           = TextAreaField('Narative', validators=[DataRequired()])
    name                        = StringField('Name', validators=[DataRequired()])
    age                         = IntegerField('Age')
    service                     = SelectField('Service', coerce=int)
    service_type                = SelectField('Service Type', coerce=int)
    worker_type                 = SelectField('Worker Type', coerce=int)
    length_of_service           = IntegerField('Length of Service')
    location                    = StringField('Location', validators=[DataRequired()])
    hobbies                     = StringField('Hobbies', validators=[DataRequired()])
    personality                 = StringField('Personality', validators=[DataRequired()])
    internet_primary_use        = StringField('Internet Primary Use', validators=[DataRequired()])
    internet_favourite_sites    = StringField('Internet Favourite Sites', validators=[DataRequired()])
    internet_computer           = StringField('Internet Computer', validators=[DataRequired()])
    tool_req_scalable_training  = IntegerField('Scalable Training')
    tool_req_tool_training      = IntegerField('Tool Training')
    tool_req_tool_awareness     = IntegerField('Tool Awareness')
    tool_req_tool_knowledge     = IntegerField('Tool Knowledge')
    tool_req_data_input_req     = IntegerField('Data Input Requirements')
    user_goals                  = StringField('User Goals', validators=[DataRequired()])
    business_goals              = StringField('Business Goals', validators=[DataRequired()])
    submit                      = SubmitField('Save')
