"""Models for Stocks."""

from flask-sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model."""

     __tablename__ = 'users'

     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     email = db.Column(db.String(30), nullable=False)
     username = db.Column(db.String(30), nullable=False)
     password = db.Column(db.Text, nullable=False)

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

class Watchlist(db.Model):
    """Watchlist model."""

    __tablename__ = 'watchlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), default=f'{ datetime.now() } Watchlist', nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_updated = db.Column(db.DateTime, onupdate=datetime.now, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

class WatchlistCompany(db.Model):
    """WatchlistCompany model."""

    __tablename__ = 'watchlists_companies'

    watchlist_id = db.Column(db.Integer, db.ForeignKey('watchlists.id', ondelete='CASCADE'), primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='CASCADE'), primary_key=True)
