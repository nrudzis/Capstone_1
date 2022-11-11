"""Forms for Stocks."""

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, Form, SelectField, DecimalField, FieldList, FormField, HiddenField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, Optional
from validators import Unique
from models import User


class LoginForm(FlaskForm):
    """Form to log in an existing user."""

    username = StringField(validators=[InputRequired()], render_kw={'placeholder':'Username'})
    password = PasswordField(validators=[InputRequired()], render_kw={'placeholder':'Password'})
    login = SubmitField('Log In')


class RegisterForm(FlaskForm):
    """Form to register a new user."""

    email = EmailField(validators=[
            InputRequired(),
            Length(max=30, message='Cannot be greater than %(max)d characters.'),
            Email()
        ], render_kw={'placeholder':'Your email'})
    username = StringField(validators=[
            InputRequired(),
            Length(max=30, message='Cannot be greater than %(max)d characters.'),
            Unique(model=User, field=User.username, message='Username unavailable. Please choose a different username.')
        ], render_kw={'placeholder':'Create a username'})
    password = PasswordField(validators=[InputRequired()], render_kw={'placeholder':'Create a password'})
    verify_password = PasswordField(validators=[
            InputRequired(),
            EqualTo('password', message='Passwords do not match.')
        ], render_kw={'placeholder':'Verify password'})
    register = SubmitField('Register')


class SearchSubform(Form):
    """Subform to search for companies by multiple conditions."""

    attribute = SelectField(choices=[
            ('', 'Choose a type of data'),
            ('q_eps_growth_first', 'Latest Quarterly YoY EPS Growth'),
            ('q_eps_growth_next', '1 Qtr Ago Qtly YoY EPS Growth'),
            ('q_eps_growth_last', '2 Qtrs Ago Qtly YoY EPS Growth'),
            ('a_eps_growth_first', 'Latest Annual EPS Growth'),
            ('a_eps_growth_next', '1 Year Ago Annual EPS Growth'),
            ('a_eps_growth_last', '2 Years Ago Annual EPS Growth'),
            ('institutional_holders', 'Institutional Holders')
        ], validators=[DataRequired()])
    relation = SelectField(choices=[
            ('', 'Choose a relation'),
            ('greater', '>'),
            ('less', '<'),
            ('equal', '=')
        ], validators=[DataRequired()])
    amount = DecimalField(validators=[InputRequired()], render_kw={'placeholder':'Enter an amount'})


class SearchForm(FlaskForm):
    """Main form to search for companies by multiple conditions."""

    searchfield = FieldList(FormField(SearchSubform), min_entries=1)


class SearchByTickerForm(FlaskForm):
    """Form to search for a company by ticker."""

    ticker = StringField('Ticker', validators=[InputRequired()], render_kw={'placeholder':'Ticker'})


class WatchlistForm(FlaskForm):
    """Form to create a new watchlist."""

    company_ids = HiddenField()
    title = StringField(validators=[
            InputRequired(),
            Length(max=100, message='Cannot be greater than %(max)d characters.')
        ], render_kw={'placeholder':'Title'})
    description = TextAreaField(validators=[
            Optional(),
            Length(max=500, message='Cannot be greater than %(max)d characters.')
        ], render_kw={'placeholder':'About (optional)'})
    save = SubmitField('Save')


class AddToWatchlistForm(FlaskForm):
    """Form to add a company to an existing watchlist."""

    watchlist = SelectField(choices=[], validators=[DataRequired()])
    add = SubmitField('Add')


class ChangeEmailForm(FlaskForm):
    """Form to change a user's email."""

    new_email = EmailField(validators=[
            InputRequired(),
            Length(max=30, message='Cannot be greater than %(max)d characters.'),
            Email()
        ], render_kw={'placeholder':'New email'})
    password = PasswordField(validators=[InputRequired()], render_kw={'placeholder':'Password'})
    change_email = SubmitField('Change Email')


class ChangeUsernameForm(FlaskForm):
    """Form to change a user's username."""

    new_username = StringField(validators=[
            InputRequired(),
            Length(max=30, message='Cannot be greater than %(max)d characters.'),
            Unique(model=User, field=User.username, message='Username unavailable. Please choose a different username.')
        ], render_kw={'placeholder':'New username'})
    password = PasswordField(validators=[InputRequired()], render_kw={'placeholder':'Password'})
    change_username = SubmitField('Change Username')


class ChangePasswordForm(FlaskForm):
    """Form to change a user's password."""

    current_password = PasswordField(validators=[InputRequired()], render_kw={'placeholder':'Current password'})
    new_password = PasswordField(validators=[InputRequired()], render_kw={'placeholder':'New password'})
    change_password = SubmitField('Change Password')
