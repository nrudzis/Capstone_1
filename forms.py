from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    """Form to log in an existing user."""

    username = StringField('Username', validators=[])
    password = PasswordField('Password', validators=[])
    login_submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    """Form to register a new user."""

    email = EmailField('Your email', validators=[])
    username = StringField('Create a username', validators=[])
    password = PasswordField('Create a password', validators=[])
    #verify_password = PasswordField('Verify password', validators=[])
    register_submit = SubmitField('Register')
