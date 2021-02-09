from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app.models.card import Cards


class CardForm(FlaskForm):
    topic = StringField('Topic',validators=[DataRequired()])
    question = StringField('Question',validators=[DataRequired()])
    submit = SubmitField('submit')