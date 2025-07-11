"""Stocks application."""

from flask import Flask, redirect, render_template, url_for, session, request, flash
from models import db, connect_db, User, Company, Watchlist, WatchlistCompany
from forms import LoginForm, RegisterForm, SearchForm, SearchByTickerForm, WatchlistForm, AddToWatchlistForm, ChangeEmailForm, ChangeUsernameForm, ChangePasswordForm
from sqlalchemy.exc import IntegrityError
from functools import wraps
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///stocks').replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mostsecret')

# Only use debug toolbar if enabled
if os.environ.get('USE_DEBUG_TOOLBAR') == '1':
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    from flask_debugtoolbar import DebugToolbarExtension
    debug = DebugToolbarExtension(app)

connect_db(app)


# HELPER FUNCTIONS
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        """Retrict access to logged in users."""

        if 'username' not in session:
            flash('You need to log in to do that!')
            return redirect(url_for('show_home'))
        return f(*args, **kwargs)
    return wrapper 


def check_username(f):
    @wraps(f)
    def wrapper(username, *args, **kwargs):
        """Prevent users from accessing other users' views."""

        if username != session['username']:
            flash('Action not permitted!')
            return redirect(url_for('show_home'))
        return f(username, *args, **kwargs)
    return wrapper


@app.template_filter('eg_trend')
def eg_trend(egs):
    """Return EPS growth trend direction (up, down, flat) as string, or False if inadequate data."""

    if None in egs:
        if egs[0] is None or len(set(egs)) == 1 or egs[1:3].count(None) == 2:
            return False
        elif egs[1] is not None:
            if egs[0] > egs[1]:
                return 'trending_up'
            elif egs[0] < egs[1]:
                return 'trending_down'
            else:
                return 'trending_flat'
        else:
            if egs[0] > egs[2]:
                return 'trending_up'
            elif egs[0] < egs[2]:
                return 'trending_down'
            else:
                return 'trending_flat'
    else:
        if egs[0] > egs[1] and egs[0] > egs[2]:
            return 'trending_up'
        elif egs[0] < egs[1] and egs[0] < egs[2]:
            return 'trending_down'
        else:
            return 'trending_flat'


@app.template_filter('format_dt')
def format_dt(dt):
    """Return string representation of date and time from datetime object."""

    return dt.strftime('%b %d, %Y %I:%M:%S %p')


def time_greet(local_time):
    """Return time-based greeting as string."""

    hour = int(local_time)
    if hour >= 0 and hour < 12:
        return 'Good morning'
    elif hour >=12 and hour < 17:
        return 'Good afternoon'
    else:
        return 'Good evening'


# VIEW FUNCTIONS
@app.route('/')
def redirect_to_home():
    """Redirect to /home."""

    return redirect(url_for('show_home'))


@app.route('/home', methods=['GET', 'POST'])
def show_home():
    """Display home page."""

    if 'username' not in session:
        login_form = LoginForm(prefix='login')
        register_form = RegisterForm(prefix='register')
        if login_form.login.data and login_form.validate_on_submit():
            local_time = login_form.local_time.data
            username = login_form.username.data
            password = login_form.password.data
            user = User.authenticate(username, password)
            if user:
                session['username'] = user.username
                greeting = time_greet(local_time)
                flash(f'{greeting}, {user.username}!')
                return redirect(url_for('show_home'))
            else:
                login_form.username.errors = ['Username or password is invalid.']
        if register_form.register.data and register_form.validate_on_submit():
            email = register_form.email.data
            username = register_form.username.data
            password = register_form.password.data
            new_user = User.register(email, username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            flash(f'Welcome, {new_user.username}!')
            return redirect(url_for('show_home'))
        return render_template('logged-out-home.html', login_form=login_form, register_form=register_form)
    else:
        search_form = SearchForm(meta={'csrf': False})
        search_by_ticker_form = SearchByTickerForm(meta={'csrf': False})
        return render_template('logged-in-home.html', search_form=search_form, search_by_ticker_form=search_by_ticker_form)


@app.route('/companies/search-results', methods=['GET', 'POST'])
@login_required
def show_results():
    """Display results of search."""

    watchlist_form = WatchlistForm()
    if watchlist_form.validate_on_submit():
        title = watchlist_form.title.data
        description = watchlist_form.description.data
        user = User.query.filter_by(username=session['username']).first_or_404()
        new_watchlist = Watchlist(title=title, description=description, user_id=user.id)
        db.session.add(new_watchlist)
        db.session.flush()
        company_ids = [int(company_id) for company_id in watchlist_form.company_ids.data.split(',')]
        for company_id in company_ids:
            db.session.add(WatchlistCompany(watchlist_id=new_watchlist.id, company_id=company_id))
        db.session.commit()
        flash(f"'{new_watchlist.title}' added to your watchlists.")
        return redirect(url_for('show_watchlists', username=session['username']))
    # TICKER SEARCH
    if 'ticker' in request.args:
        ticker = request.args['ticker']
        companies = Company.search_by_ticker(ticker.upper())
    # MULTIPLE CONDITIONS SEARCH
    else:
        form_values = list(request.args.to_dict().values())
        query_elements = [(form_values[i], form_values[i+1], form_values[i+2]) for i in range(0, len(form_values), 3)]
        companies = Company.search(query_elements)
    company_ids = ','.join([str(company.id) for company in companies])
    watchlist_form.company_ids.data = company_ids
    return render_template('search-results.html', companies=companies, watchlist_form=watchlist_form)


@app.route('/companies/<ticker>', methods=['GET', 'POST'])
@login_required
def show_company_info(ticker):
    """Display company info."""

    user = User.query.filter_by(username=session['username']).first_or_404()
    watchlists = user.watchlists
    company = Company.query.filter_by(ticker=ticker).first_or_404()
    add_to_watchlist_form = AddToWatchlistForm()
    add_to_watchlist_form.watchlist.choices = [(wl.id, wl.title) for wl in watchlists]
    add_to_watchlist_form.watchlist.choices.insert(0, ('', 'Choose a watchlist'))
    if add_to_watchlist_form.validate_on_submit():
        watchlist_id = add_to_watchlist_form.watchlist.data
        watchlist_company = WatchlistCompany(watchlist_id=watchlist_id, company_id=company.id)
        watchlist = Watchlist.query.get_or_404(watchlist_id)
        db.session.add(watchlist_company)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(f"Error: {company.name} already in '{watchlist.title}'!")
            return redirect(url_for('show_company_info', ticker=ticker))
        flash(f"{company.name} ({company.ticker}) added to '{watchlist.title}'!")
        return redirect(url_for('show_company_info', ticker=ticker))
    return render_template('company-info.html', company=company, watchlists=watchlists, add_to_watchlist_form=add_to_watchlist_form)


@app.route('/users/<username>', methods=['GET', 'POST'])
@login_required
@check_username
def show_user_info(username):
    """Display current user info."""

    change_email_form = ChangeEmailForm(prefix='change-email')
    change_username_form = ChangeUsernameForm(prefix='change-username')
    change_password_form = ChangePasswordForm(prefix='change-password')
    pwd_error_msg = ['Invalid password. Try again.']
    if change_email_form.change_email.data and change_email_form.validate_on_submit():
        password = change_email_form.password.data
        new_email = change_email_form.new_email.data
        user = User.change_email(username, password, new_email)
        if user:
            db.session.add(user)
            db.session.commit()
            flash('Email changed!')
            return redirect(url_for('show_user_info', username=username))
        else:
            change_email_form.password.errors = pwd_error_msg
    if change_username_form.change_username.data and change_username_form.validate_on_submit():
        password = change_username_form.password.data
        new_username = change_username_form.new_username.data
        user = User.change_username(username, password, new_username)
        if user:
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
            flash('Username changed!')
            return redirect(url_for('show_user_info', username=user.username))
        else:
            change_username_form.password.errors = pwd_error_msg
    if change_password_form.change_password.data and change_password_form.validate_on_submit():
        current_password = change_password_form.current_password.data
        new_password = change_password_form.new_password.data
        user = User.change_password(username, current_password, new_password)
        if user:
            db.session.add(user)
            db.session.commit()
            flash('Password changed!')
            return redirect(url_for('show_user_info', username=username))
        else:
            change_password_form.current_password.errors = pwd_error_msg
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user-info.html', user=user, change_email_form=change_email_form, change_username_form=change_username_form, change_password_form=change_password_form)


@app.route('/users/<username>/logout', methods=['POST'])
@login_required
@check_username
def logout_user(username):

    """Log out current user."""
    session.pop('username')
    flash("You've logged out!")
    return redirect(url_for('show_home'))


@app.route('/users/<username>/delete', methods=['POST'])
@login_required
@check_username
def delete_user(username):
    """Delete user's account."""

    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    flash('Account deleted!')
    return redirect(url_for('show_home'))


@app.route('/users/<username>/watchlists', methods=['GET', 'POST'])
@login_required
@check_username
def show_watchlists(username):
    """Display current user's saved watchlists."""

    user = User.query.filter_by(username=username).first_or_404()
    watchlist_form = WatchlistForm()
    if watchlist_form.validate_on_submit():
        title = watchlist_form.title.data
        description = watchlist_form.description.data
        new_watchlist = Watchlist(title=title, description=description, user_id=user.id)
        db.session.add(new_watchlist)
        db.session.commit()
        flash(f"'{new_watchlist.title}' created!")
        return redirect(url_for('show_watchlists', username=username))
    user = User.query.filter_by(username=username).first_or_404()
    watchlists = user.watchlists
    return render_template('user-watchlists.html', watchlists=watchlists, watchlist_form=watchlist_form)


@app.route('/users/<username>/watchlists/<int:watchlist_id>', methods=['GET', 'POST'])
@login_required
@check_username
def show_watchlist(username, watchlist_id):
    """Display contents of a single watchlist."""

    watchlist = Watchlist.query.get_or_404(watchlist_id)
    watchlist_form = WatchlistForm(obj=watchlist)
    if watchlist_form.validate_on_submit():
        watchlist.title = watchlist_form.title.data
        watchlist.description = watchlist_form.description.data
        db.session.commit()
        flash('Watchlist changes saved!')
        return redirect(url_for('show_watchlist', username=username, watchlist_id=watchlist_id))
    return render_template('single-watchlist.html', watchlist=watchlist, watchlist_form=watchlist_form)


@app.route('/users/<username>/watchlists/<int:watchlist_id>/delete', methods=['POST'])
@login_required
@check_username
def delete_watchlist(username, watchlist_id):
    """Delete a watchlist."""

    watchlist = Watchlist.query.get_or_404(watchlist_id)
    db.session.delete(watchlist)
    db.session.commit()
    flash('Watchlist deleted!')
    return redirect(url_for('show_watchlists', username=username))


@app.route('/users/<username>/watchlists/<int:watchlist_id>-<int:company_id>/delete', methods=['POST'])
@login_required
@check_username
def remove_company(username, watchlist_id, company_id):
    """Remove company from a watchlist."""

    watchlist_company = WatchlistCompany.query.filter_by(watchlist_id=watchlist_id, company_id=company_id).first_or_404()
    db.session.delete(watchlist_company)
    db.session.commit()
    flash('Company removed!')
    return redirect(url_for('show_watchlist', username=username, watchlist_id=watchlist_id))
