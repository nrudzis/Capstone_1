from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, Form, SelectField, DecimalField, FieldList, FormField, HiddenField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from validators import Unique
from models import User


class LoginForm(FlaskForm):
    """Form to log in an existing user."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    login = SubmitField('Log In')


class RegisterForm(FlaskForm):
    """Form to register a new user."""

    email = EmailField('Your email', validators=[
            InputRequired(),
            Length(max=30, message='Cannot be greater than %(max)d characters.'),
            Email()
        ])
    username = StringField('Create a username', validators=[
            InputRequired(),
            Length(max=30, message='Cannot be greater than %(max)d characters.'),
            Unique(model=User, field=User.username, message='Username unavailable. Please choose a different username.')
        ])
    password = PasswordField('Create a password', validators=[InputRequired()])
    verify_password = PasswordField('Verify password', validators=[
            InputRequired(),
            EqualTo('password', message='Passwords do not match.')
        ])
    register = SubmitField('Register')


class SearchSubform(Form):
    """Subform to search for companies by multiple conditions."""

    attribute = SelectField(choices=[
            ('q_eps_growth_first', 'Latest Quarterly EPS Growth'),
            ('q_eps_growth_next', '1 Quarter Ago Quarterly EPS Growth'),
            ('q_eps_growth_last', '2 Quarters Ago Quarterly EPS Growth'),
            ('a_eps_growth_first', 'Latest Annual EPS Growth'),
            ('a_eps_growth_next', '1 Year Ago Annual EPS Growth'),
            ('a_eps_growth_last', '2 Years Ago Annual EPS Growth'),
            ('institutional_holders', 'Institutional Holders')
        ])
    relation = SelectField(choices=[
            ('greater', '>'),
            ('less', '<'),
            ('equal', '=')
        ])
    amount = DecimalField(validators=[InputRequired()])


class SearchForm(FlaskForm):
    """Main form to search for companies by multiple conditions."""

    searchfield = FieldList(FormField(SearchSubform), min_entries=1)


class SearchByTickerForm(FlaskForm):
    """Form to search for a company by ticker."""

    ticker = StringField('Ticker', validators=[InputRequired()])


class WatchlistForm(FlaskForm):
    """Form to create a new watchlist."""

    company_ids = HiddenField()
    title = StringField('New Watchlist Title', validators=[
            InputRequired(),
            Length(max=100, message='Cannot be greater than %(max)d characters.')
        ])
    save = SubmitField('Save')


class AddToWatchlistForm(FlaskForm):
    """Form to add a company to an existing watchlist."""

    watchlist = SelectField(choices=[])
    add = SubmitField('Add')


class ChangeEmailForm(FlaskForm):
    """Form to change a user's email."""

    new_email = EmailField('New email', validators=[
            InputRequired(),
            Length(max=30, message='Cannot be greater than %(max)d characters.'),
            Email()
        ])
    password = PasswordField('Password', validators=[InputRequired()])
    change_email = SubmitField('Change Email')


class ChangeUsernameForm(FlaskForm):
    """Form to change a user's username."""

    new_username = StringField('New username', validators=[
            InputRequired(),
            Length(max=30, message='Cannot be greater than %(max)d characters.'),
            Unique(model=User, field=User.username, message='Username unavailable. Please choose a different username.')
        ])
    password = PasswordField('Password', validators=[InputRequired()])
    change_username = SubmitField('Change Username')


class ChangePasswordForm(FlaskForm):
    """Form to change a user's password."""

    current_password = PasswordField('Current Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired()])
    change_password = SubmitField('Change Password')
