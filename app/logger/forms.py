from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, optional
from flask_wtf.file import FileField, FileAllowed, FileRequired

from app.user.model import User
class XformUploadForm(FlaskForm):
    title = TextField(
        'title',
        validators=[DataRequired(), Length(min=6, max=120)])
    
    description = TextAreaField(
        'description',
        validators=[DataRequired(), Length(min=6, max=200)])

    file = FileField(
		'file', 
		validators=[FileRequired()])
