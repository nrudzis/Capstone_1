"""Stocks application."""

from flask import Flask, redirect, render_template, url_for, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Company, Watchlist, WatchlistCompany
from forms import LoginForm, RegisterForm, SearchForm, WatchlistForm
#from company_info_seed import company_info, seed_companies

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stocks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
#seed_companies(company_info)

def add_companies_to_session(companies):
    session['companies'] = {}
    for company in companies:
        session['companies'][company.ticker] = company.id


@app.route('/')
def redirect_to_home():
    """Redirect to /home."""
    return redirect(url_for('show_home'))


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
                return redirect(url_for('show_home'))
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
            return redirect(url_for('show_home'))
        else:
            return render_template('logged-out-home.html', login_form=login_form, register_form=register_form)
    else:
        search_form = SearchForm(meta={'csrf': False})
        if search_form.validate_on_submit():
            return redirect(url_for('show_results'))
        return render_template('logged-in-home.html', search_form=search_form)


@app.route('/companies/search-results', methods=['GET', 'POST'])
def show_results():
    """Display results of search."""

    watchlist_form = WatchlistForm()
    if watchlist_form.validate_on_submit():
        title = watchlist_form.title.data
        user = User.query.filter_by(username=session['username']).first_or_404()
        new_watchlist = Watchlist(title=title, user_id=user.id)
        db.session.add(new_watchlist)
        if 'companies' in session:
            db.session.flush()
            for company_id in session['companies'].values():
                db.session.add(WatchlistCompany(watchlist_id=new_watchlist.id, company_id=company_id))
        db.session.commit()
        return redirect(url_for('show_watchlists', username=session['username']))
    form_values = list(request.args.to_dict().values())
    query_elements = [(form_values[i], form_values[i+1], form_values[i+2]) for i in range(0, len(form_values), 3)]
    companies = Company.search(query_elements)
    add_companies_to_session(companies)
    return render_template('search-results.html', companies=companies, watchlist_form=watchlist_form)


@app.route('/companies/<ticker>')
def show_company_info(ticker):
    """Display company info."""

    company_id = session['companies'][ticker] if 'companies' in session else None
    company = Company.query.get_or_404(company_id)
    return render_template('company-info.html', company=company)


@app.route('/users/<username>/watchlists')
def show_watchlists(username):
    """Display current user's saved watchlists."""

    user = User.query.filter_by(username=username).first_or_404()
    watchlists = user.watchlists
    return render_template('user-watchlists.html', watchlists=watchlists)

@app.route('/users/<username>/watchlists/<int:watchlist_id>')
def show_watchlist(username, watchlist_id):
    """Display contents of a single watchlist."""

    watchlist = Watchlist.query.get_or_404(watchlist_id)
    session['companies'] = {}
    add_companies_to_session(watchlist.companies)
    return render_template('single-watchlist.html', watchlist=watchlist)
