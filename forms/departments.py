from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class DepsForm(FlaskForm):
    title = StringField('Название')
    members = StringField('Участники')
    email = StringField('Почта')
    submit = SubmitField('Применить')