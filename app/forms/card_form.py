from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CardForm(FlaskForm):
    topic = StringField('Topic', validators=[DataRequired()])
    question = StringField('Question', validators=[DataRequired()])
    submit = SubmitField('submit')