from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.user import User


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[Email(), DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('Password Verify', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')

    def validate_email(self, email):
        is_exist = User.query.filter_by(email=email)
        if is_exist:
            return ValidationError('Email already in use.')
        return True


class LoginForm(FlaskForm):
    email = StringField('email', validators=[Email(), DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')
