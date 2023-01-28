"""Tests for models."""

from unittest import TestCase
from app import app
from models import db, User, Company


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stocks_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True


db.drop_all()
db.create_all()


class TestUserModel(TestCase):
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

    def tearDown(self):
        db.session.rollback()

    def test_authenticate(self):
        user = User.authenticate('testuser', 'testpassword')
        self.assertTrue(user)

    def test_authenticate_invalid_username(self):
        user = User.authenticate('badusername', 'testpassword')
        self.assertFalse(user)

    def test_authenticate_invalid_password(self):
        user = User.authenticate('testuser', 'badpassword')
        self.assertFalse(user)

    def test_register(self):
        email = 'newuser@testing.com'
        username = 'newuser'
        password = 'newuserpassword'
        user = User.register(email, username, password)
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertNotEqual(user.password, password)
        self.assertTrue(type(user.password)==str)

    def test_change_email(self):
        new_email = 'newemail@testing.com'
        username = 'testuser'
        password = 'testpassword'
        user = User.query.filter_by(username='testuser').first()
        user_email_changed = User.change_email(username, password, new_email)
        self.assertEqual(user_email_changed.id, user.id)
        self.assertEqual(user_email_changed.email, new_email)

    def test_change_username(self):
        current_username = 'testuser'
        new_username = 'newusername'
        password = 'testpassword'
        user = User.query.filter_by(username=current_username).first()
        user_username_changed = User.change_username(current_username, password, new_username)
        self.assertEqual(user_username_changed.id, user.id)
        self.assertEqual(user_username_changed.username, new_username)

    def test_change_password(self):
        username = 'testuser'
        current_password = 'testpassword'
        new_password = 'newpassword'
        user = User.query.filter_by(username=username).first()
        user_password_changed = User.change_password(username, current_password, new_password)
        user_old_password = User.authenticate(username, current_password)
        self.assertEqual(user_password_changed.id, user.id)
        self.assertFalse(user_old_password)


class TestCompanyModel(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
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
        db.session.add(company_1)
        db.session.add(company_2)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_search(self):
        single_condition = [('q_eps_growth_first', 'greater', 1)]
        multiple_conditions = [('a_eps_growth_first', 'less', 5), ('q_eps_growth_next', 'greater', 5), ('institutional_holders', 'greater', 3000)]
        no_matches = [('institutional_holders', 'equal', 50), ('q_eps_growth_last', 'less', 10)]
        single_condition_companies = Company.search(single_condition)
        multiple_conditions_companies = Company.search(multiple_conditions)
        no_matches_companies = Company.search(no_matches)
        self.assertEqual(single_condition_companies[0].id, 1)
        self.assertEqual(multiple_conditions_companies[0].id, 2)
        self.assertFalse(no_matches_companies)

    def test_ticker_search(self):
        ticker = 'TEST_2'
        no_matches_ticker = 'NOTATICKER'
        ticker_companies = Company.search_by_ticker(ticker)
        no_matches_companies = Company.search_by_ticker(no_matches_ticker)
        self.assertEqual(ticker_companies[0].id, 2)
        self.assertFalse(no_matches_companies)
