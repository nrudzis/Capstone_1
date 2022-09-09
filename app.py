"""Stocks application."""

from flask import Flask, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm, RegisterForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stocks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#connect_db(app)


@app.route('/')
def redirect_to_home():
    """Redirect to /home."""
    return redirect('/home')


@app.route('/home')
def show_home():
    """Show home page."""

    login_form = LoginForm()
    register_form = RegisterForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        return redirect('/home')
    elif register_form.validate_on_submit():
        email = register_form.email.data
        username = register_form.username.data
        password = register_form.password.data
        return redirect('/home')
    else:
        return render_template('home.html', login_form=login_form, register_form=register_form)
