from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField


class LoginForm(FlaskForm):
    """Form to log in an existing user."""

    username = StringField('Username', validators=[])
    password = PasswordField('Password', validators=[])


class RegisterForm(FlaskForm):
    """Form to register a new user."""

    email = EmailField('Email', validators=[])
    username = StringField('Username', validators=[])
    password = PasswordField('Password', validators=[])
