from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired


class CardForm(FlaskForm):
    topic = StringField('Topic', validators=[DataRequired()])
    question = StringField('Question', validators=[DataRequired()], widget=TextArea())
    typ = RadioField('Type', choices=[('general', 'General'), ('code', 'Code')], validators=[DataRequired()],\
                     default='general')
    submit = SubmitField('submit')
