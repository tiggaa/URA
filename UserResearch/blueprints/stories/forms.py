from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from UserResearch.models import User_storey

class CreateStorey_Form(FlaskForm):
    who = SelectField('As a', coerce=int)
    what = TextAreaField('I want to', validators=[DataRequired()])
    in_order = TextAreaField('In order to', validators=[DataRequired()])
    submit  = SubmitField('Save')
