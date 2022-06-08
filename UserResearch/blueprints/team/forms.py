from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from UserResearch.models import Team, TeamMembers

class CreateTeam_Form(FlaskForm):
    team        = StringField('Team', validators=[DataRequired()])
    team_desc   = TextAreaField('Team Description', validators=[DataRequired()])
    submit      = SubmitField('Save')

class AddTeamMembers_Form(FlaskForm):
    member     = SelectField('Member', coerce=int)
    submit      = SubmitField('Add Member')

class UpdateTeamMembers_Form(FlaskForm):
    team        = SelectField('Team', coerce=int)
    members     = SelectField('Member', coerce=int)
    submit      = SubmitField('Save')
