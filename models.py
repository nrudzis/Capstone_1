"""Models for Stocks."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    watchlists = db.relationship('Watchlist', backref='user', cascade='all, delete, delete-orphan', passive_deletes=True)

    @classmethod
    def authenticate(cls, username, pwd):
        """Return user if exists, else return false."""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

    @classmethod
    def register(cls, email, username, pwd):
        """Register and return new user."""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')
        return cls(email=email, username=username, password=hashed_utf8)

    @classmethod
    def change_email(cls, username, password, new_email):
        """Update user's email and return user."""
        user = User.authenticate(username, password)
        if user: 
            user.email = new_email
        return user

    @classmethod
    def change_username(cls, current_username, password, new_username):
        """Update user's username and return user."""
        user = User.authenticate(current_username, password)
        if user:
            user.username = new_username
        return user

    @classmethod
    def change_password(cls, username, current_password, new_password):
        """Update user's password and return user."""
        hashed = bcrypt.generate_password_hash(new_password)
        hashed_utf8 = hashed.decode('utf8')
        user = User.authenticate(username, current_password)
        if user:
            user.password = hashed_utf8
        return user


class Company(db.Model):
    """Company model."""

    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    q_eps_growth_first = db.Column(db.Numeric)
    q_eps_growth_next = db.Column(db.Numeric)
    q_eps_growth_last = db.Column(db.Numeric)
    a_eps_growth_first = db.Column(db.Numeric)
    a_eps_growth_next = db.Column(db.Numeric)
    a_eps_growth_last = db.Column(db.Numeric)
    institutional_holders = db.Column(db.Integer)

    @classmethod
    def search(cls, elements):
        query = Company.query
        for attr, rel, amt in elements:
            if rel == 'greater':
                query = query.filter(getattr(Company, attr) > amt)
            elif rel == 'less':
                query = query.filter(getattr(Company, attr) < amt)
            else:
                query = query.filter(getattr(Company, attr) == amt)
        return query.all()

    @classmethod
    def search_by_ticker(cls, ticker):
        return Company.query.filter_by(ticker=ticker).all()

    company_watchlists = db.relationship('WatchlistCompany', backref='company', cascade='all, delete, delete-orphan', passive_deletes=True)


class Watchlist(db.Model):
    """Watchlist model."""

    __tablename__ = 'watchlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), default=f'{ datetime.now() } Watchlist', nullable=False)
    description = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    companies = db.relationship('Company', secondary='watchlists_companies', backref='watchlists')
    watchlist_companies = db.relationship('WatchlistCompany', backref='watchlist', cascade='all, delete, delete-orphan', passive_deletes=True)


class WatchlistCompany(db.Model):
    """WatchlistCompany model."""

    __tablename__ = 'watchlists_companies'

    watchlist_id = db.Column(db.Integer, db.ForeignKey('watchlists.id', ondelete='CASCADE'), primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='CASCADE'), primary_key=True)
