from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, optional

from app.user.model import User

class OrganizationForm(FlaskForm):
    title = TextField(
        'title',
        validators=[DataRequired(), Length(min=3, max=120)])
    
    description = TextField(
        'description',
        validators=[DataRequired(), Length(min=6, max=200)])
    
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    
    address = TextField(
        'address',
        validators=[DataRequired(), Length(min=6, max=200)])

    website = TextField('website', validators=[optional()])

class ProjectForm(FlaskForm):
    title = TextField(
        'title',
        validators=[DataRequired(), Length(min=6, max=120)])
    
    description = TextAreaField(
        'description',
        validators=[DataRequired(), Length(min=6, max=200)])

    organization = SelectField(
        'organization',
        coerce=int,
        validators=[DataRequired()]
    )
