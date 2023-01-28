"""Tests for app."""

from unittest import TestCase
from app import app, login_required, check_username, eg_trend, format_dt, time_greet
from models import db, User, Company, Watchlist, WatchlistCompany
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stocks_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False #disable CSRF in WTForms
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar'] #don't use Flask DebugToolbar

db.drop_all()
db.create_all()


class TestLoginRequired(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_login_required(self):
        resp = self.client.get('/users/testuser')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, '/home')

    def test_login_required_redirection_followed_and_flash_message(self):
        resp = self.client.get('/users/testuser', follow_redirects=True) #test should pass for any view using the login_required decorator
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="mb-5">Log In</h1>', html)
        self.assertIn('You need to log in to do that!', html)


class TestCheckUsername(TestCase):
    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'

    def test_check_username(self):
        resp = self.client.get('/users/anotheruser')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, '/home')

    def test_check_username_redirection_followed_and_flash_message(self):
        resp = self.client.get('/users/anotheruser', follow_redirects=True) #test should pass for any view using the check_username decorator
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<strong>testuser</strong>', html)
        self.assertIn('Action not permitted!', html)


class TestEg_Trend(TestCase):
    def test_eg_trend_false(self):
        egs_1 = (None, 1.2, 3.4)
        egs_2 = (None, None, None)
        egs_3 = (4.5, None, None)
        egs_1_trend = eg_trend(egs_1)
        egs_2_trend = eg_trend(egs_2)
        egs_3_trend = eg_trend(egs_3)
        self.assertFalse(egs_1_trend)
        self.assertFalse(egs_2_trend)
        self.assertFalse(egs_3_trend)

    def test_eg_trend_third_index_none(self):
        egs_1 = (4.3, 2.1, None)
        egs_2 = (1.2, 3.4, None)
        egs_3 = (1.2, 1.2, None)
        egs_1_trend = eg_trend(egs_1)
        egs_2_trend = eg_trend(egs_2)
        egs_3_trend = eg_trend(egs_3)
        self.assertEqual(egs_1_trend, 'trending_up')
        self.assertEqual(egs_2_trend, 'trending_down')
        self.assertEqual(egs_3_trend, 'trending_flat')

    def test_eg_trend_second_index_none(self):
        egs_1 = (4.3, None, 2.1)
        egs_2 = (1.2, None, 3.4)
        egs_3 = (1.2, None, 1.2)
        egs_1_trend = eg_trend(egs_1)
        egs_2_trend = eg_trend(egs_2)
        egs_3_trend = eg_trend(egs_3)
        self.assertEqual(egs_1_trend, 'trending_up')
        self.assertEqual(egs_2_trend, 'trending_down')
        self.assertEqual(egs_3_trend, 'trending_flat')

    def test_eg_trend_no_nones(self):
        egs_1 = (6.5, 4.3, 2.1)
        egs_2 = (6.5, 2.1, 4.3)
        egs_3 = (1.2, 3.4, 5.6)
        egs_4 = (1.2, 5.6, 4.5)
        egs_5 = (1.2, 1.2, 1.2)
        egs_6 = (1.2, 3.4, 1.2)
        egs_7 = (3.4, 1.2, 3.4)
        egs_8 = (4.3, 6.5, 2.1)
        egs_9 = (4.3, 2.1, 6.5)
        egs_1_trend = eg_trend(egs_1)
        egs_2_trend = eg_trend(egs_2)
        egs_3_trend = eg_trend(egs_3)
        egs_4_trend = eg_trend(egs_4)
        egs_5_trend = eg_trend(egs_5)
        egs_6_trend = eg_trend(egs_6)
        egs_7_trend = eg_trend(egs_7)
        egs_8_trend = eg_trend(egs_8)
        egs_9_trend = eg_trend(egs_9)
        self.assertEqual(egs_1_trend, 'trending_up')
        self.assertEqual(egs_2_trend, 'trending_up')
        self.assertEqual(egs_3_trend, 'trending_down')
        self.assertEqual(egs_4_trend, 'trending_down')
        self.assertEqual(egs_5_trend, 'trending_flat')
        self.assertEqual(egs_6_trend, 'trending_flat')
        self.assertEqual(egs_7_trend, 'trending_flat')
        self.assertEqual(egs_8_trend, 'trending_flat')
        self.assertEqual(egs_9_trend, 'trending_flat')


class TestFormatDt(TestCase):
    def test_format_dt(self):
        expected_str = 'Jan 26, 2023 12:00:53 PM'
        dt_obj = datetime.strptime('2023-01-26 12:00:53.123456', '%Y-%m-%d %H:%M:%S.%f')
        dt_str = format_dt(dt_obj)
        self.assertEqual(dt_str, expected_str)


class TestTimeGreet(TestCase):
    def test_time_greet_morning(self):
        greeting = time_greet(9)
        self.assertEqual(greeting, 'Good morning')

    def test_time_greet_afternoon(self):
        greeting = time_greet(15)
        self.assertEqual(greeting, 'Good afternoon')

    def test_time_greet_evening(self):
        greeting = time_greet(21)
        self.assertEqual(greeting, 'Good evening')


class TestRedirectToHome(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_redirect_to_home(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, '/home')

    def test_redirect_to_home_followed(self):
        resp = self.client.get('/', follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="mb-5">Log In</h1>', html)


class TestShowHome(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        email = 'testuser@testing.com',
        username = 'testuser',
        password = 'testpassword'
        user = User.register(email, username, password)
        db.session.add(user)
        db.session.commit()

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_show_home_logged_out(self):
        resp = self.client.get('/home')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="mb-5">Log In</h1>', html)

    def test_show_home_logged_in(self):
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'
        resp = self.client.get('/home')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<strong>testuser</strong>', html)

    def test_show_home_log_in_and_flash_message(self):
        login_form_data = {'login-local_time': 0,
                           'login-username': 'testuser',
                           'login-password': 'testpassword',
                           'login-login': True}
        resp = self.client.post('/home', data=login_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<strong>testuser</strong>', html)
        self.assertIn('Good morning, testuser!', html)

    def test_show_home_log_in_invalid(self):
        login_form_data = {'login-local_time': 0,
                           'login-username': 'testuser',
                           'login-password': 'badpassword',
                           'login-login': True}
        resp = self.client.post('/home', data=login_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<small class="form-error d-block">Username or password is invalid.</small>', html)

    def test_show_home_register_and_flash_message(self):
        register_form_data = {'register-email': 'testnewuser@testing.com',
                              'register-username': 'testnewuser',
                              'register-password': 'testnewpassword',
                              'register-verify_password': 'testnewpassword',
                              'register-register': True}
        resp = self.client.post('/home', data=register_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<strong>testnewuser</strong>', html)
        self.assertIn('Welcome, testnewuser!', html)

    def test_show_home_register_username_error(self):
        register_form_data = {'register-email': 'testnewuser@testing.com',
                              'register-username': 'testuser',
                              'register-password': 'testnewpassword',
                              'register-verify_password': 'testnewpassword',
                              'register-register': True}
        resp = self.client.post('/home', data=register_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<small class="form-error d-block">Username unavailable. Please choose a different username.</small>', html)

    def test_show_home_register_password_error(self):
        register_form_data = {'register-email': 'testnewuser@testing.com',
                              'register-username': 'testnewuser',
                              'register-password': 'testnewpassword',
                              'register-verify_password': 'badnewpassword',
                              'register-register': True}
        resp = self.client.post('/home', data=register_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<small class="form-error d-block">Passwords do not match.</small>', html)


class TestShowResults(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        email = 'testuser@testing.com',
        username = 'testuser',
        password = 'testpassword'
        user = User.register(email, username, password)
        company_1 = Company(
                ticker='TEST_1',
                name='Test Company 1',
                description='Test description 1',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        company_2 = Company(
                ticker='TEST_2',
                name='Test Company 2',
                description='Test description 2',
                q_eps_growth_first=0.9,
                q_eps_growth_next=8.7,
                q_eps_growth_last=6.5,
                a_eps_growth_first=4.3,
                a_eps_growth_next=2.1,
                a_eps_growth_last=0.9,
                institutional_holders=4321
            )
        db.session.add(user)
        db.session.add(company_1)
        db.session.add(company_2)
        db.session.commit()

    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'

    def tearDown(self):
        db.session.rollback()

    def test_show_results_multiple_search(self):
        search_params = {'searchfield-0-attribute': 'q_eps_growth_first',
                         'searchfield-0-relation': 'greater',
                         'searchfield-0-amount': '0',
                         'searchfield-1-attribute': 'a_eps_growth_next',
                         'searchfield-1-relation': 'less',
                         'searchfield-1-amount': 5,
                         'searchfield-3-attribute': 'institutional_holders',
                         'searchfield-3-relation': 'greater',
                         'searchfield-3-amount': 2000}
        resp = self.client.get('/companies/search-results', query_string=search_params)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<a class="lead lg-item-heading" href="/companies/TEST_2">Test Company 2 (TEST_2)</a>', html)

    def test_show_results_multiple_search_none_found(self):
        search_params = {'searchfield-0-attribute': 'institutional_holders',
                         'searchfield-0-relation': 'less',
                         'searchfield-0-amount': 500}
        resp = self.client.get('/companies/search-results', query_string=search_params)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<p>No results found.</p>', html)

    def test_show_results_ticker_search(self):
        search_params = {'ticker': 'TEST_1'}
        resp = self.client.get('/companies/search-results', query_string=search_params)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<a class="lead lg-item-heading" href="/companies/TEST_1">Test Company 1 (TEST_1)</a>', html)

    def test_show_results_ticker_search_not_found(self):
        search_params = {'ticker': 'NOTATICKER'}
        resp = self.client.get('/companies/search-results', query_string=search_params)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<p>No results found.</p>', html)

    def test_show_results_save_in_watchlist_and_flash_message(self):
        watchlist_form_data = {'title': 'Test Watchlist Title',
                               'description': 'Test watchlist description',
                               'company_ids': '1,2'}
        resp = self.client.post('/companies/search-results', data=watchlist_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<a class="lead lg-item-heading" href="/users/testuser/watchlists/1">Test Watchlist Title</a>', html)
        self.assertIn('&#39;Test Watchlist Title&#39; added to your watchlists.', html)


class TestShowCompanyInfo(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        email = 'testuser@testing.com',
        username = 'testuser',
        password = 'testpassword'
        user = User.register(email, username, password)
        company = Company(
                ticker='TEST',
                name='Test Company',
                description='Test description',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        watchlist = Watchlist(
                title='Test Watchlist Title',
                description='Test description',
                user_id=1
            )
        db.session.add(user)
        db.session.add(company)
        db.session.add(watchlist)
        db.session.commit()

    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'

    def tearDown(self):
        db.session.rollback()

    def test_show_company_info(self):
        resp = self.client.get('/companies/TEST')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="mb-5">Test Company (TEST)</h1>', html)

    def test_show_company_info_add_to_watchlist_and_flash_message(self):
        watchlist_form_data = {'watchlist': 1}
        resp_show_company_info = self.client.post('/companies/TEST', data=watchlist_form_data, follow_redirects=True)
        resp_show_watchlist = self.client.get('/users/testuser/watchlists/1')
        html_show_company_info = resp_show_company_info.get_data(as_text=True)
        html_show_watchlist = resp_show_watchlist.get_data(as_text=True)
        self.assertEqual(resp_show_company_info.status_code, 200)
        self.assertIn('<h1 class="mb-5">Test Company (TEST)</h1>', html_show_company_info)
        self.assertIn('Test Company (TEST) added to &#39;Test Watchlist Title&#39;!', html_show_company_info)
        self.assertIn('<a class="lead lg-item-heading" href="/companies/TEST">Test Company (TEST)</a>', html_show_watchlist)

    def test_show_company_info_add_to_watchlist_error_and_flash_message(self):
        WatchlistCompany.query.delete()
        watchlist_company = WatchlistCompany(
                watchlist_id=1,
                company_id=1
            )
        db.session.add(watchlist_company)
        db.session.commit()
        watchlist_form_data = {'watchlist': 1}
        resp_show_company_info = self.client.post('/companies/TEST', data=watchlist_form_data, follow_redirects=True)
        resp_show_watchlist = self.client.get('/users/testuser/watchlists/1')
        html_show_company_info = resp_show_company_info.get_data(as_text=True)
        html_show_watchlist = resp_show_watchlist.get_data(as_text=True)
        self.assertEqual(resp_show_company_info.status_code, 200)
        self.assertIn('<h1 class="mb-5">Test Company (TEST)</h1>', html_show_company_info)
        self.assertIn('Error: Test Company already in &#39;Test Watchlist Title&#39;!', html_show_company_info)


class TestShowUserInfo(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        email = 'testuser@testing.com',
        username = 'testuser',
        password = 'testpassword'
        user = User.register(email, username, password)
        db.session.add(user)
        db.session.commit()

    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'

    def tearDown(self):
        db.session.rollback()

    def test_show_user_info(self):
        resp = self.client.get('/users/testuser')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<td>testuser@testing.com</td>', html)
        self.assertIn('<td>testuser</td>', html)

    def test_show_user_info_change_email_and_flash_message(self):
        change_email_form_data = {'change-email-password': 'testpassword',
                                  'change-email-new_email': 'newemail@testing.com',
                                  'change-email-change_email': True}
        resp = self.client.post('/users/testuser', data=change_email_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<td>newemail@testing.com</td>', html)
        self.assertIn('<td>testuser</td>', html)
        self.assertIn('Email changed!', html)

    def test_show_user_info_change_email_password_error(self):
        change_email_form_data = {'change-email-password': 'badpassword',
                                  'change-email-new_email': 'testuser@testing.com',
                                  'change-email-change_email': True}
        resp = self.client.post('/users/testuser', data=change_email_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<small class="form-error d-block">Invalid password. Try again.</small>', html)
        self.assertIn('<td>newemail@testing.com</td>', html)
        self.assertIn('<td>testuser</td>', html)

    def test_show_user_info_change_password_and_flash_message(self):
        change_password_form_data = {'change-password-current_password': 'testpassword',
                                  'change-password-new_password': 'newpassword',
                                  'change-password-change_password': True}
        resp = self.client.post('/users/testuser', data=change_password_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        username = 'testuser'
        password = 'newpassword'
        user = User.authenticate(username, password)
        self.assertTrue(user.username==username)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<td>newemail@testing.com</td>', html)
        self.assertIn('<td>testuser</td>', html)
        self.assertIn('Password changed!', html)

    def test_show_user_info_change_password_password_error(self):
        change_password_form_data = {'change-password-current_password': 'badpassword',
                                  'change-password-new_password': 'testpassword',
                                  'change-password-change_password': True}
        resp = self.client.post('/users/testuser', data=change_password_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        username = 'testuser'
        password = 'newpassword'
        user = User.authenticate(username, password)
        self.assertTrue(user.username==username)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<small class="form-error d-block">Invalid password. Try again.</small>', html)
        self.assertIn('<td>newemail@testing.com</td>', html)
        self.assertIn('<td>testuser</td>', html)

    def test_show_user_info_change_username_and_flash_message(self):
        change_username_form_data = {'change-username-password': 'newpassword',
                                  'change-username-new_username': 'newusername',
                                  'change-username-change_username': True}
        resp = self.client.post('/users/testuser', data=change_username_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<td>newemail@testing.com</td>', html)
        self.assertIn('<td>newusername</td>', html)
        self.assertIn('<strong>newusername</strong>', html)
        self.assertIn('Username changed!', html)

    def test_show_user_info_change_username_password_error(self):
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'newusername'
        change_username_form_data = {'change-username-password': 'badpassword',
                                  'change-username-new_username': 'testuser',
                                  'change-username-change_username': True}
        resp = self.client.post('/users/newusername', data=change_username_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<small class="form-error d-block">Invalid password. Try again.</small>', html)
        self.assertIn('<td>newemail@testing.com</td>', html)
        self.assertIn('<td>newusername</td>', html)
        self.assertIn('<strong>newusername</strong>', html)


class TestLogoutUser(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        email = 'testuser@testing.com',
        username = 'testuser',
        password = 'testpassword'
        user = User.register(email, username, password)
        db.session.add(user)
        db.session.commit()

    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'

    def tearDown(self):
        db.session.rollback()

    def test_logout_user(self):
        resp = self.client.post('/users/testuser/logout')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, '/home')

    def test_logout_user_redirect_followed_and_username_not_in_session_and_flash_message(self):
        resp = self.client.post('/users/testuser/logout', follow_redirects=True)
        html = resp.get_data(as_text=True)
        with self.client.session_transaction() as sess:
            self.assertTrue('username' not in sess)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="mb-5">Log In</h1>', html)
        self.assertIn('You&#39;ve logged out!', html)


class TestDeleteUser(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()

    def setUp(self):
        email = 'testuser@testing.com',
        username = 'testuser',
        password = 'testpassword'
        user = User.register(email, username, password)
        db.session.add(user)
        db.session.commit()
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'

    def tearDown(self):
        db.session.rollback()

    def test_delete_user(self):
        resp = self.client.post('/users/testuser/delete')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, '/home')

    def test_delete_user_username_not_in_session_and_user_removed_from_db(self):
        resp = self.client.post('/users/testuser/delete')
        with self.client.session_transaction() as sess:
            self.assertTrue('username' not in sess)
        user = User.query.filter_by(username='testuser').first()
        self.assertFalse(user)

    def test_delete_user_redirect_followed_and_flash_message(self):
        resp = self.client.post('/users/testuser/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="mb-5">Log In</h1>', html)
        self.assertIn('Account deleted!', html)


class TestShowWatchlists(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        email = 'testuser@testing.com',
        username = 'testuser',
        password = 'testpassword'
        user = User.register(email, username, password)
        watchlist_1 = Watchlist(
                title='Test Watchlist Title 1',
                description='Test description 1',
                user_id=1
            )
        watchlist_2 = Watchlist(
                title='Test Watchlist Title 2',
                description='Test description 2',
                user_id=1
            )
        db.session.add(user)
        db.session.add(watchlist_1)
        db.session.add(watchlist_2)
        db.session.commit()

    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'

    def tearDown(self):
        db.session.rollback()

    def test_show_watchlists(self):
        resp = self.client.get('/users/testuser/watchlists')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<a class="lead lg-item-heading" href="/users/testuser/watchlists/1">Test Watchlist Title 1</a>', html)
        self.assertIn('<a class="lead lg-item-heading" href="/users/testuser/watchlists/2">Test Watchlist Title 2</a>', html)

    def test_show_watchlists_add_new_watchlist_and_flash_message(self):
        watchlist_form_data = {'title': 'Test Watchlist Title 3',
                               'description': 'Test description 3'}
        resp = self.client.post('/users/testuser/watchlists', data=watchlist_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<a class="lead lg-item-heading" href="/users/testuser/watchlists/3">Test Watchlist Title 3</a>', html)
        self.assertIn('&#39;Test Watchlist Title 3&#39; created!', html)


class TestShowWatchlist(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        email = 'testuser@testing.com',
        username = 'testuser',
        password = 'testpassword'
        user = User.register(email, username, password)
        company = Company(
                ticker='TEST',
                name='Test Company',
                description='Test description',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        watchlist = Watchlist(
                title='Test Watchlist Title',
                description='Test description',
                user_id=1
            )
        watchlist_company = WatchlistCompany(
                watchlist_id=1,
                company_id=1
            )
        db.session.add(user)
        db.session.add(company)
        db.session.add(watchlist)
        db.session.add(watchlist_company)
        db.session.commit()

    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'

    def tearDown(self):
        db.session.rollback()

    def test_show_watchlist(self):
        resp = self.client.get('/users/testuser/watchlists/1')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="mb-1">Test Watchlist Title</h1>', html)
        self.assertIn('<p class="mb-5">Test description</p>', html)
        self.assertIn('<a class="lead lg-item-heading" href="/companies/TEST">Test Company (TEST)</a>', html)

    def test_show_watchlists_edit_watchlist_and_flash_message(self):
        watchlist_form_data = {'title': 'UPDATED Watchlist Title',
                               'description': 'UPDATED description'}
        resp = self.client.post('/users/testuser/watchlists/1', data=watchlist_form_data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="mb-1">UPDATED Watchlist Title</h1>', html)
        self.assertIn('<p class="mb-5">UPDATED description</p>', html)
        self.assertIn('Watchlist changes saved!', html)


class TestDeleteWatchlist(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        email = 'testuser@testing.com',
        username = 'testuser',
        password = 'testpassword'
        user = User.register(email, username, password)
        db.session.add(user)
        db.session.commit()

    def setUp(self):
        watchlist = Watchlist(
                title='Test Watchlist Title',
                description='Test description',
                user_id=1
            )
        db.session.add(watchlist)
        db.session.commit()
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'

    def tearDown(self):
        db.session.rollback()

    def test_delete_watchlist(self):
        resp = self.client.post('/users/testuser/watchlists/1/delete')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, '/users/testuser/watchlists')

    def test_delete_watchlist_redirect_followed_and_flash_message(self):
        resp = self.client.post('/users/testuser/watchlists/2/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="mb-5">Watchlists</h1>', html)
        self.assertIn('Watchlist deleted!', html)

    def test_watchlist_removed_from_db(self):
        resp = self.client.post('/users/testuser/watchlists/3/delete')
        watchlist = Watchlist.query.filter_by(id=3).first()
        self.assertFalse(watchlist)


class TestRemoveCompany(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        email = 'testuser@testing.com',
        username = 'testuser',
        password = 'testpassword'
        user = User.register(email, username, password)
        company = Company(
                ticker='TEST',
                name='Test Company',
                description='Test description',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        watchlist = Watchlist(
                title='Test Watchlist Title',
                description='Test description',
                user_id=1
            )
        watchlist_company = WatchlistCompany(
                watchlist_id=1,
                company_id=1
            )
        db.session.add(user)
        db.session.add(company)
        db.session.add(watchlist)
        db.session.commit()

    def setUp(self):
        watchlist_company = WatchlistCompany(
                watchlist_id=1,
                company_id=1
            )
        db.session.add(watchlist_company)
        db.session.commit()
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
            change_session['username'] = 'testuser'

    def tearDown(self):
        db.session.rollback()

    def test_remove_company(self):
        resp = self.client.post('/users/testuser/watchlists/1-1/delete')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, '/users/testuser/watchlists/1')

    def test_remove_company_redirect_followed_and_flash_message(self):
        resp = self.client.post('/users/testuser/watchlists/1-1/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="mb-1">Test Watchlist Title</h1>', html)
        self.assertNotIn('<a class="lead lg-item-heading" href="/companies/TEST">Test Company (TEST)</a>', html)
        self.assertIn('Company removed!', html)

    def test_watchlist_id_company_id_removed_from_db(self):
        resp = self.client.post('/users/testuser/watchlists/1-1/delete')
        watchlist_company = WatchlistCompany.query.filter_by(watchlist_id=1, company_id=1).first()
        self.assertFalse(watchlist_company)
