from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.user import User


class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password Verify', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('E-mail already in use')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('submit')
