"""Stocks application."""

from flask import Flask, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension

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
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    """Log user in."""


@app.route('/register', methods=['POST'])
def register():
    """Register new user."""
