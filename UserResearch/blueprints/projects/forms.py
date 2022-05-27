from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from UserResearch.models import Projects

class CreateProjectForm(FlaskForm):
    project_name        = StringField('Project Name', validators=[DataRequired()])
    project_description = TextAreaField('Project Description', validators=[DataRequired()])
    project_team        = StringField('Project Team', validators=[DataRequired()])
    submit  = SubmitField('Post')