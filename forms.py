from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, Form, SelectField, DecimalField, FieldList, FormField


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

class SearchSubform(Form):
    data_select = SelectField(choices=[
            ('q_eps_growth_first', 'Latest Quarterly EPS Growth'),
            ('q_eps_growth_next', '1 Quarter Ago Quarterly EPS Growth'),
            ('q_eps_growth_last', '2 Quarters Ago Quarterly EPS Growth'),
            ('a_eps_growth_first', 'Latest Annual EPS Growth'),
            ('a_eps_growth_next', '1 Year Ago Annual EPS Growth'),
            ('a_eps_growth_last', '2 Years Ago Annual EPS Growth'),
            ('institutional_holders', 'Institutional Holders')
        ])
    relation_select = SelectField(choices=[
            ('greater', '>'),
            ('less', '<'),
            ('equal', '=')
        ])
    amount = DecimalField()

class SearchForm(FlaskForm):
    search = FieldList(FormField(SearchSubform), min_entries=1)
