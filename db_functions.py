"""Functions to add/update companies in the database."""

from app import app
import requests
from datetime import date, datetime
from time import sleep
import yfinance
from models import db, Company, EnqueuedTicker
import os


FMP_KEY = os.environ.get('FMP_KEY')
P_KEY = os.environ.get('P_KEY')
if not (FMP_KEY and P_KEY):
    from keys import fmp_key, p_key
    FMP_KEY = fmp_key
    P_KEY = p_key
SEASONS = [('09-01', '11-30'), ('06-01', '08-31'), ('03-01', '05-31'), ('12-01', '02-28')]
CURRENT_DATE = str(date.today())
p_calls = 0


def check_p_calls():
    """Polygon free API permits 5 calls/min. Pauses execution for a minute if 5 calls made."""

    global p_calls
    p_calls += 1
    if p_calls == 5:
        p_calls = 0
        sleep(60)


def get_tickers():
    """Returns list of tickers."""

    tickers = []
    for exchange in ('NASDAQ', 'NYSE'):
        resp = requests.get('https://financialmodelingprep.com/stable/company-screener',
            params={'volumeMoreThan': '10000', #reduces tickers of illiquid stocks and various non-ETF funds
                    'isEtf': 'false',
                    'isActivelyTrading': 'true',
                    'exchange': exchange,
                    'country': 'US',
                    'limit': '10000',
                    'apikey': FMP_KEY})
        data = resp.json()
        for i in range(len(data)):
            tickers.append(data[i]['symbol'])
    return tickers


def get_a_eps_list(ticker):
    """Returns list of tuples with annual filing date and annual EPS, or False if less then four years of data."""

    resp = requests.get('https://financialmodelingprep.com/stable/income-statement',
        params={'symbol': ticker,
                'apikey': FMP_KEY})
    data = resp.json()
    if len(data) < 4:
        return False
    return [(data[i]['filingDate'], data[i]['epsDiluted']) for i in range(4)]


def get_current_season():
    """Returns tuple with current earnings season month-day date range."""

    curr_month = int(CURRENT_DATE[5:7])
    curr_season = ('12-01', '02-28')
    for season in SEASONS[0:3]:
        if curr_month >= int(season[0][:2]) and curr_month <= int(season[1][:2]):
            curr_season = season
    return curr_season


def insert_years(cycle):
    """Inserts years into earnings season date ranges."""

    year = int(CURRENT_DATE[0:4])
    month = int(CURRENT_DATE[5:7])
    if cycle[0] == ('12-01', '02-28'):
        if month != 12:
            for i, season in enumerate(cycle):
                if season[0][:2] != '12':
                    cycle[i] = (f'{year}-{season[0]}', f'{year}-{season[1]}')
                else:
                    cycle[i] = (f'{year-1}-{season[0]}', f'{year}-{season[1]}')
                    year = year - 1
        else:
            for i, season in enumerate(cycle):
                if season[0][:2] != '12':
                    cycle[i] = (f'{year+1}-{season[0]}', f'{year+1}-{season[1]}')
                else:
                    cycle[i] = (f'{year}-{season[0]}', f'{year+1}-{season[1]}')
                    year = year - 1
    else:
        for i, season in enumerate(cycle):
            if season[0][:2] != '12':
                cycle[i] = (f'{year}-{season[0]}', f'{year}-{season[1]}')
            else:
                year = year - 1
                cycle[i] = (f'{year}-{season[0]}', f'{year+1}-{season[1]}')
    return cycle


def generate_current_cycle():
    """Generates last twelve earnings season date ranges as list of tuples, starting with the current season."""

    curr_season = get_current_season()
    for i, season in enumerate(SEASONS):
        if season == curr_season:
            seasons_ordered = SEASONS[i:] + SEASONS[:i]
    cycle = seasons_ordered * 3
    curr_cycle = insert_years(cycle)
    return curr_cycle


def get_q_eps_single(ticker, season):
    """Returns tuple with quarterly filing date and quarterly EPS, or empty tuple if not available."""

    check_p_calls()
    resp = requests.get('https://api.polygon.io/vX/reference/financials',
        params={'ticker': ticker,
                'filing_date.gte': season[0],
                'filing_date.lte': season[1],
                'apiKey': P_KEY})
    data = resp.json()
    if not data['results']:
        return ()
    q_date = data['results'][0]['filing_date']
    q_eps = data['results'][0]['financials']['income_statement']['diluted_earnings_per_share']['value']
    return (q_date, q_eps)


def validate_first_to_third_list(q_eps_list):
    """Returns False if there's more than two ()s, or if there's not three items after each (), each of which is also not (), otherwise returns True."""

    #if there are more than two ()s, return False
    if q_eps_list.count(()) > 2:
        return False

    #if there are not three items after each (), or if any of the three is also a (), return False
    for i, q_eps in enumerate(q_eps_list):
        if q_eps_list[i] == ():
            if len(q_eps_list) < i+4:
                return False
            else:
                if q_eps_list[i+1] == () or q_eps_list[i+2] == () or q_eps_list[i+3] == ():
                    return False
    return True


def get_first_to_third_list(ticker, current_cycle, a_eps_list):
    """
    Returns list of tuples with quarterly filing date and quarterly EPS for first, second and third quarters, and empty tuples for fourth quarter.
    Returns False if an unexpected pattern is encountered.
    """

    q_eps_list = []
    for i, season in enumerate(current_cycle):
        q_eps = get_q_eps_single(ticker, season)

        #if there is more than one item, and the last two items are sequential ()s, return False
        if len(q_eps_list) > 1 and q_eps_list[-1] == () and q_eps == ():
            return False

        #if there are two, and only two items, and they are sequential ()s, and the next item is not a (), remove one ()
        if len(q_eps_list) == 2 and len(set(q_eps_list)) == 1 and q_eps != ():
            del q_eps_list[0]
        q_eps_list.append(q_eps)

        #if there is a () at the first index, and fourth quarter data won't be going here, then remove it
        if len(q_eps_list) == 2 and len(set(q_eps_list)) > 1 and q_eps_list[0] == () and datetime.strptime(q_eps_list[1][0], '%Y-%m-%d') > datetime.strptime(a_eps_list[0][0], '%Y-%m-%d'):
            del q_eps_list[0]

        #if there are two, and only two ()s, and there are three items after the second (), then there is enough data
        if q_eps_list.count(()) == 2 and len(q_eps_list) - len(q_eps_list[:[i for i, q_eps in enumerate(q_eps_list) if q_eps == ()][1]]) == 4:
            break

        #if there are seven, and only seven items, including one (), then there is enough data
        if len(q_eps_list) == 7 and q_eps_list.count(()) == 1:
            break
    valid = validate_first_to_third_list(q_eps_list)
    if not valid:
        return False
    return q_eps_list


def get_split_data(ticker):
    """Returns list of tuples containing stock split date and split factor, or False if not available."""

    check_p_calls()
    resp = requests.get('https://api.polygon.io/v3/reference/splits',
        params={'ticker': ticker,
                'apiKey': P_KEY})
    data = resp.json()
    if not data['results']:
        return False
    return [(i['execution_date'], int(i['split_from'])/int(i['split_to'])) for i in data['results']]


def adjust_if_split(split_data, q_eps_list):
    """Adjusts EPS by split factor, if stock splits occurred after quarterly filing dates."""

    for split_date, split_factor in split_data:
        for i, q_eps in enumerate(q_eps_list):
            if len(q_eps) == 2 and datetime.strptime(split_date, '%Y-%m-%d') > datetime.strptime(q_eps[0], '%Y-%m-%d'):
                q_eps_list[i] = list(q_eps_list[i])
                q_eps_list[i][1] = q_eps_list[i][1] * split_factor
                q_eps_list[i] = tuple(q_eps_list[i])
    return q_eps_list


def add_fourth_q_eps(q_eps_list, a_eps_list):
    """Replaces empty tuples with tuple containing fourth quarter filing date and calculated fourth quarter EPS."""

    for i, q_eps in enumerate(q_eps_list):
        if q_eps == () and i < 4:
            q_eps_list[i] = (
                a_eps_list[0][0], 
                a_eps_list[0][1] - (float(q_eps_list[i+1][1]) + float(q_eps_list[i+2][1]) + float(q_eps_list[i+3][1]))
        )
        if q_eps == () and i > 3:
            q_eps_list[i] = (
                a_eps_list[1][0], 
                a_eps_list[1][1] - (float(q_eps_list[i+1][1]) + float(q_eps_list[i+2][1]) + float(q_eps_list[i+3][1]))
        )
    return q_eps_list


def get_q_eps_list(ticker, a_eps_list):
    """Returns list of tuples with quarterly filing date and complete and adjusted quarterly EPS, or False if not available."""

    current_cycle = generate_current_cycle()
    first_to_third_list = get_first_to_third_list(ticker, current_cycle, a_eps_list)
    if not first_to_third_list:
        return False
    split_data = get_split_data(ticker)
    if split_data:
        splits_checked_list = adjust_if_split(split_data, first_to_third_list)
        q_eps_list = add_fourth_q_eps(splits_checked_list, a_eps_list)
        return q_eps_list
    q_eps_list = add_fourth_q_eps(first_to_third_list, a_eps_list)
    return q_eps_list


def get_company_details(ticker):
    """Returns dictionary with name and description, or 'unavailable' in place of name and description if not available."""

    check_p_calls()
    resp = requests.get(f'https://api.polygon.io/v3/reference/tickers/{ticker}',
        params={'apiKey': P_KEY})
    data = resp.json()
    if data['status'] != 'OK':
        return {
            'name': 'unavailable',
            'description': 'unavailable'
        }
    return {
        'name': data['results']['name'],
        'description': data['results']['description']
    }


def get_institutional_holders(ticker):
    """Returns number of institutional holders, using yfinance package, or None if not available."""

    company = yfinance.Ticker(ticker)
    m_holders = company.major_holders
    if m_holders is None:
        return None
    return int(m_holders.iloc[3,0])


def rate_of_change(final, initial):
    """Returns % growth, given final and initial values, or None if unable to be calculated."""

    if final <= 0 or initial <= 0:
        return None
    return ((final-initial)/initial)*100


def make_company_dict(ticker, a_eps_list, q_eps_list):
    """Returns dictionary with company information."""

    company_details = get_company_details(ticker)
    institutional_holders = get_institutional_holders(ticker)
    company_dict = {}
    company_dict['ticker'] = ticker
    company_dict['name'] = company_details['name']
    company_dict['description'] = company_details['description']
    company_dict['q_eps_growth_first'] = rate_of_change(
        q_eps_list[0][1],
        q_eps_list[4][1]
    )
    company_dict['q_eps_growth_next'] = rate_of_change(
        q_eps_list[1][1],
        q_eps_list[5][1]
    )
    company_dict['q_eps_growth_last'] = rate_of_change(
        q_eps_list[2][1],
        q_eps_list[6][1]
    )
    company_dict['a_eps_growth_first'] = rate_of_change(
        a_eps_list[0][1],
        a_eps_list[1][1]
    )
    company_dict['a_eps_growth_next'] = rate_of_change(
        a_eps_list[1][1],
        a_eps_list[2][1]
    )
    company_dict['a_eps_growth_last'] = rate_of_change(
        a_eps_list[2][1],
        a_eps_list[3][1],
    )
    company_dict['institutional_holders'] = institutional_holders
    return company_dict


def update_company(company, company_dict):
    """Updates a company that is already in the database."""

    company.name=company_dict['name'],
    company.description=company_dict['description'],
    company.q_eps_growth_first=company_dict['q_eps_growth_first'],
    company.q_eps_growth_next=company_dict['q_eps_growth_next'],
    company.q_eps_growth_last=company_dict['q_eps_growth_last'],
    company.a_eps_growth_first=company_dict['a_eps_growth_first'],
    company.a_eps_growth_next=company_dict['a_eps_growth_next'],
    company.a_eps_growth_last=company_dict['a_eps_growth_last'],
    company.institutional_holders=company_dict['institutional_holders']
    db.session.commit()


def add_new_company(company_dict):
    """Creates a new company and adds it to the database."""

    company = Company(
        ticker=company_dict['ticker'],
        name=company_dict['name'],
        description=company_dict['description'],
        q_eps_growth_first=company_dict['q_eps_growth_first'],
        q_eps_growth_next=company_dict['q_eps_growth_next'],
        q_eps_growth_last=company_dict['q_eps_growth_last'],
        a_eps_growth_first=company_dict['a_eps_growth_first'],
        a_eps_growth_next=company_dict['a_eps_growth_next'],
        a_eps_growth_last=company_dict['a_eps_growth_last'],
        institutional_holders=company_dict['institutional_holders']
    )
    db.session.add(company)
    db.session.commit()


def delete_enqueued_ticker(ticker):
    """Delete enqueued ticker from the database."""

    et = EnqueuedTicker.query.filter_by(ticker=ticker).first()
    db.session.delete(et)
    db.session.commit()


def reconcile_tickers(api_tickers, db_tickers):
    """Delete company from the database if not in the list of tickers from the API."""

    for ticker in db_tickers:
        if ticker not in api_tickers:
            company = Company.query.filter_by(ticker=ticker).first()
            db.session.delete(company)
            db.session.commit()


def update_ticker_queue(tickers):
    """Update ticker queue."""

    for ticker in tickers:
        et = EnqueuedTicker(
            ticker=ticker
        )
        db.session.add(et)
        db.session.commit()


def update_db(tickers):
    """Update the database."""

    for ticker in tickers:

        #remove ticker from the queue
        delete_enqueued_ticker(ticker)
        try:

            #get list with annual data
            a_eps_list = get_a_eps_list(ticker)

            #if there's a problem with the annual data, move on to the next ticker
            if not a_eps_list:
                continue

            #get list with quarterly data
            q_eps_list = get_q_eps_list(ticker, a_eps_list)

            #if there's a problem with the quarterly data, move on to the next ticker
            if not q_eps_list:
                continue

            #store all company info in a dictionary
            company_dict = make_company_dict(ticker, a_eps_list, q_eps_list)

            #check if this company is already in the database
            company = Company.query.filter_by(ticker=ticker).first()

            #if it is in the database, update it
            if company:
                update_company(company, company_dict)

            #if not, add it
            else:
                add_new_company(company_dict)

        #for anything else unexpected, move on to the next ticker
        except:
            continue
