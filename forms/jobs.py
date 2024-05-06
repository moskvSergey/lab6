from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Название')
    work_size = StringField('Объем работы')
    collaborators = StringField('Участники')
    submit = SubmitField('Применить')