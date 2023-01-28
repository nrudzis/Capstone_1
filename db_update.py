"""Add/update companies in database from APIs."""

from app import app
from models import Company, EnqueuedTicker
from db_functions import update_db, get_tickers, reconcile_tickers, update_ticker_queue

with app.app_context():

    #get first 250 tickers in the queue
    enqueued_tickers = EnqueuedTicker.query.limit(250).all()

    if enqueued_tickers:

        #update the database
        update_db([et.ticker for et in enqueued_tickers])

    else:

        #get all tickers from api
        api_tickers = get_tickers()

        #get all Company model tickers
        db_tickers = [company.ticker for company in Company.query.all()]

        #remove any company whose ticker isn't in the api tickers
        reconcile_tickers(api_tickers, db_tickers)

        #add all the api tickers to the ticker queue
        update_ticker_queue(api_tickers)

        #get first 248 tickers in the queue
        enqueued_tickers = EnqueuedTicker.query.limit(248).all()

        #update the database
        update_db([et.ticker for et in enqueued_tickers])
