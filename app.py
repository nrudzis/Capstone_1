"""Stocks application."""

from flask import Flask, redirect, render_template, url_for, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Company
from forms import LoginForm, RegisterForm, SearchForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stocks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def redirect_to_home():
    """Redirect to /home."""
    return redirect('/home')


@app.route('/home', methods=['GET', 'POST'])
def show_home():
    """Display home page."""

    if 'username' not in session:
        login_form = LoginForm()
        register_form = RegisterForm()
        if login_form.validate_on_submit() and login_form.login_submit.data:
            username = login_form.username.data
            password = login_form.password.data
            user = User.authenticate(username, password)
            if user:
                session['username'] = user.username
                return redirect('/home')
            else:
                login_form.username.errors = ['Username or password is invalid.']
        elif register_form.validate_on_submit() and register_form.register_submit.data:
            email = register_form.email.data
            username = register_form.username.data
            password = register_form.password.data
            new_user = User.register(email, username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            return redirect('/home')
        else:
            return render_template('logged-out-home.html', login_form=login_form, register_form=register_form)
    else:
        search_form = SearchForm()
        if search_form.validate_on_submit():
            return redirect('/companies/search-results')
        return render_template('logged-in-home.html', search_form=search_form)


@app.route('/companies/search-results', methods=['POST'])
def show_results():
    """Display results of search."""

    form_values = list(request.form.to_dict().values())
    query_elements = [(form_values[i], form_values[i+1], form_values[i+2]) for i in range(1, len(form_values), 3)]
    companies = Company.search(query_elements)
    return render_template('search-results.html', companies=companies)
