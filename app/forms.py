from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, MultipleFileField

class PhotoForm(FlaskForm):
    photo = MultipleFileField()
    submit = SubmitField('Upload')
