"""Tests for db_functions."""

from unittest import TestCase
from unittest.mock import patch
import db_functions
from app import app
from models import db, Company, EnqueuedTicker
from datetime import datetime
from decimal import Decimal


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stocks_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True


db.drop_all()
db.create_all()


class TestCheckPCalls(TestCase):
    @patch('db_functions.p_calls', new=4) #begin with 4 calls
    @patch('db_functions.sleep', return_value=None)
    def test_check_p_calls_with_5_p_calls(self, mock_sleep):
        db_functions.check_p_calls() #5th call
        self.assertEqual(db_functions.p_calls, 0)
        self.assertEqual(mock_sleep.call_count, 1)

    @patch('db_functions.p_calls', new=3) #begin with 3 calls
    @patch('db_functions.sleep', return_value=None)
    def test_check_p_calls_with_less_than_5_p_calls(self, mock_sleep):
        db_functions.check_p_calls() #4th call
        self.assertEqual(db_functions.p_calls, 4)
        self.assertEqual(mock_sleep.call_count, 0)


class TestGetTickers(TestCase):
    def test_get_tickers(self):
        expected_tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN']
        all_tickers = db_functions.get_tickers()
        expected_tickers_in_all_tickers = all(ticker in all_tickers for ticker in expected_tickers)
        over_3000_tickers = len(all_tickers) > 3000
        self.assertIsInstance(all_tickers, list)
        self.assertTrue(expected_tickers_in_all_tickers)
        self.assertTrue(over_3000_tickers)


class TestGetAEPSList(TestCase):
    def test_get_a_eps_list_with_greater_than_4_years_data(self):
        a_eps_list = db_functions.get_a_eps_list('AAPL')
        has_4_or_more_items = len(a_eps_list) >= 4
        self.assertIsInstance(a_eps_list, list)
        self.assertTrue(has_4_or_more_items)

    def test_get_a_eps_list_with_less_than_4_years_data(self):
        less_than_4_result = db_functions.get_a_eps_list('RIVN') #This test will fail once there is over 4 years of data for RIVN.
        self.assertFalse(less_than_4_result)


class TestGetCurrentSeason(TestCase):
    @patch('db_functions.CURRENT_DATE', new='2022-12-20')
    def test_get_current_season_with_month_12(self):
        expected_season = ('12-01', '02-28')
        current_season = db_functions.get_current_season()
        self.assertEqual(current_season, expected_season)

    @patch('db_functions.CURRENT_DATE', new='2022-07-12')
    def test_get_current_season_with_month_07(self):
        expected_season = ('06-01', '08-31')
        current_season = db_functions.get_current_season()
        self.assertEqual(current_season, expected_season)


class TestInsertYears(TestCase):
    @patch('db_functions.CURRENT_DATE', new='2023-01-20')
    def test_insert_years_with_month_01(self):
        cycle_if_month_is_01 = [('12-01', '02-28'), ('09-01', '11-30'), ('06-01', '08-31'), ('03-01', '05-31'), ('12-01', '02-28'), ('09-01', '11-30'), ('06-01', '08-31'), ('03-01', '05-31'), ('12-01', '02-28'), ('09-01', '11-30'), ('06-01', '08-31'), ('03-01', '05-31')]
        expected_cycle = [('2022-12-01', '2023-02-28'), ('2022-09-01', '2022-11-30'), ('2022-06-01', '2022-08-31'), ('2022-03-01', '2022-05-31'), ('2021-12-01', '2022-02-28'), ('2021-09-01', '2021-11-30'), ('2021-06-01', '2021-08-31'), ('2021-03-01', '2021-05-31'), ('2020-12-01', '2021-02-28'), ('2020-09-01', '2020-11-30'), ('2020-06-01', '2020-08-31'), ('2020-03-01', '2020-05-31')]
        cycle_years_inserted = db_functions.insert_years(cycle_if_month_is_01)
        self.assertEqual(cycle_years_inserted, expected_cycle)

    @patch('db_functions.CURRENT_DATE', new='2022-12-20')
    def test_insert_years_with_month_12(self):
        cycle_if_month_is_12 = [('12-01', '02-28'), ('09-01', '11-30'), ('06-01', '08-31'), ('03-01', '05-31'), ('12-01', '02-28'), ('09-01', '11-30'), ('06-01', '08-31'), ('03-01', '05-31'), ('12-01', '02-28'), ('09-01', '11-30'), ('06-01', '08-31'), ('03-01', '05-31')]
        expected_cycle = [('2022-12-01', '2023-02-28'), ('2022-09-01', '2022-11-30'), ('2022-06-01', '2022-08-31'), ('2022-03-01', '2022-05-31'), ('2021-12-01', '2022-02-28'), ('2021-09-01', '2021-11-30'), ('2021-06-01', '2021-08-31'), ('2021-03-01', '2021-05-31'), ('2020-12-01', '2021-02-28'), ('2020-09-01', '2020-11-30'), ('2020-06-01', '2020-08-31'), ('2020-03-01', '2020-05-31')]
        cycle_years_inserted = db_functions.insert_years(cycle_if_month_is_12)
        self.assertEqual(cycle_years_inserted, expected_cycle)

    @patch('db_functions.CURRENT_DATE', new='2022-07-12')
    def test_insert_years_with_month_07(self):
        cycle_if_month_is_07 = [('06-01', '08-31'), ('03-01', '05-31'), ('12-01', '02-28'), ('09-01', '11-30'), ('06-01', '08-31'), ('03-01', '05-31'), ('12-01', '02-28'), ('09-01', '11-30'), ('06-01', '08-31'), ('03-01', '05-31'), ('12-01', '02-28'), ('09-01', '11-30')]
        expected_cycle = [('2022-06-01', '2022-08-31'), ('2022-03-01', '2022-05-31'), ('2021-12-01', '2022-02-28'), ('2021-09-01', '2021-11-30'), ('2021-06-01', '2021-08-31'), ('2021-03-01', '2021-05-31'), ('2020-12-01', '2021-02-28'), ('2020-09-01', '2020-11-30'), ('2020-06-01', '2020-08-31'), ('2020-03-01', '2020-05-31'), ('2019-12-01', '2020-02-28'), ('2019-09-01', '2019-11-30')]
        cycle_years_inserted = db_functions.insert_years(cycle_if_month_is_07)
        self.assertEqual(cycle_years_inserted, expected_cycle)


class TestGenerateCurrentCycle(TestCase):
    @patch('db_functions.CURRENT_DATE', new='2023-01-20')
    def test_generate_current_cycle_with_month_01(self):
        expected_cycle = [('2022-12-01', '2023-02-28'), ('2022-09-01', '2022-11-30'), ('2022-06-01', '2022-08-31'), ('2022-03-01', '2022-05-31'), ('2021-12-01', '2022-02-28'), ('2021-09-01', '2021-11-30'), ('2021-06-01', '2021-08-31'), ('2021-03-01', '2021-05-31'), ('2020-12-01', '2021-02-28'), ('2020-09-01', '2020-11-30'), ('2020-06-01', '2020-08-31'), ('2020-03-01', '2020-05-31')]
        current_cycle = db_functions.generate_current_cycle()
        self.assertEqual(current_cycle, expected_cycle)

    def test_generate_current_cycle_with_month_12(self):
        expected_cycle = [('2022-12-01', '2023-02-28'), ('2022-09-01', '2022-11-30'), ('2022-06-01', '2022-08-31'), ('2022-03-01', '2022-05-31'), ('2021-12-01', '2022-02-28'), ('2021-09-01', '2021-11-30'), ('2021-06-01', '2021-08-31'), ('2021-03-01', '2021-05-31'), ('2020-12-01', '2021-02-28'), ('2020-09-01', '2020-11-30'), ('2020-06-01', '2020-08-31'), ('2020-03-01', '2020-05-31')]
        current_cycle = db_functions.generate_current_cycle()
        self.assertEqual(current_cycle, expected_cycle)

    @patch('db_functions.CURRENT_DATE', new='2022-07-12')
    def test_generate_current_cycle_with_month_07(self):
        expected_cycle = [('2022-06-01', '2022-08-31'), ('2022-03-01', '2022-05-31'), ('2021-12-01', '2022-02-28'), ('2021-09-01', '2021-11-30'), ('2021-06-01', '2021-08-31'), ('2021-03-01', '2021-05-31'), ('2020-12-01', '2021-02-28'), ('2020-09-01', '2020-11-30'), ('2020-06-01', '2020-08-31'), ('2020-03-01', '2020-05-31'), ('2019-12-01', '2020-02-28'), ('2019-09-01', '2019-11-30')]
        current_cycle = db_functions.generate_current_cycle()
        self.assertEqual(current_cycle, expected_cycle)


class TestGetQEPSSingle(TestCase):
    def test_get_q_eps_list_single_with_data_available(self):
        ticker = 'AAPL'
        season = ('2022-06-01', '2022-08-31')
        q_eps_single = db_functions.get_q_eps_single(ticker, season)
        has_2_items = len(q_eps_single) == 2
        q_date = datetime.strptime(q_eps_single[0], '%Y-%m-%d')
        q_eps = q_eps_single[1]
        self.assertIsInstance(q_eps_single, tuple)
        self.assertTrue(has_2_items)
        self.assertIsInstance(q_date, datetime)
        self.assertIsInstance(q_eps, float)

    def test_get_q_eps_list_single_with_data_unavailable(self):
        ticker = 'AAPL'
        season = ('2022-09-01', '2022-11-30') #Data should be unavailable for a 4th quarter season since this is reported in the annual filing.
        unavailable_data_result = db_functions.get_q_eps_single(ticker, season)
        has_0_items = len(unavailable_data_result) == 0
        self.assertIsInstance(unavailable_data_result, tuple)
        self.assertTrue(has_0_items)


class TestValidateFirstToThirdList(TestCase):
    def test_validate_first_to_third_list_with_more_than_two_empty_tuples(self):
        more_than_two_empty_tuples_list = [(), ('2022-11-06', 0.1), ('2022-08-02', 0.2), ('2022-05-02', 0.3), (), ('2021-11-03', 0.4), ('2021-08-05', 0.5), ('2021-05-31', 0.6), ()]
        more_than_two_empty_tuples_result = db_functions.validate_first_to_third_list(more_than_two_empty_tuples_list)
        self.assertFalse(more_than_two_empty_tuples_result)

    def test_validate_first_to_third_list_with_invalid_sequence(self):
        invalid_seq_list = [(), ('2022-11-06', 0.1), (), ('2022-05-02', 0.2), (), ('2021-11-03', 0.3), ('2021-08-05', 0.4), ('2021-05-31', 0.5), ()]
        invalid_seq_result = db_functions.validate_first_to_third_list(invalid_seq_list)
        self.assertFalse(invalid_seq_result)

    def test_validate_first_to_third_list_with_valid_sequence(self):
        valid_seq_list = [(), ('2022-11-06', 0.1), ('2022-08-02', 0.2), ('2022-05-02', 0.3), (), ('2021-11-03', 0.4), ('2021-08-05', 0.5), ('2021-05-31', 0.6)]
        valid_seq_result = db_functions.validate_first_to_third_list(valid_seq_list)
        self.assertTrue(valid_seq_result)


class TestGetFirstToThirdList(TestCase):
    ticker = 'TEST' #Value of ticker doesn't affect the result. Return value of functions that accept it as an argument are provided by mock functions.
    cycle = [('2022-12-01', '2023-02-28'), ('2022-09-01', '2022-11-30'), ('2022-06-01', '2022-08-31'), ('2022-03-01', '2022-05-31'), ('2021-12-01', '2022-02-28'), ('2021-09-01', '2021-11-30'), ('2021-06-01', '2021-08-31'), ('2021-03-01', '2021-05-31'), ('2020-12-01', '2021-02-28'), ('2020-09-01', '2020-11-30'), ('2020-06-01', '2020-08-31'), ('2020-03-01', '2020-05-31')]
    a_eps_list = [('2023-01-27', 0.1), ('2022-01-23', 0.2), ('2021-01-28', 0.3), ('2020-01-19', 0.4)]

    @patch('db_functions.get_q_eps_single')
    def test_get_first_to_third_list_with_last_two_items_sequential_tuples(self, mock_get_q_eps_single):
        mock_get_q_eps_single.side_effect = [('2022-11-06', 0.5), (), ()]
        last_two_items_seq_tuples_result = db_functions.get_first_to_third_list(self.ticker, self.cycle, self.a_eps_list)
        self.assertFalse(last_two_items_seq_tuples_result)

    @patch('db_functions.get_q_eps_single')
    def test_get_first_to_third_list_with_first_two_items_sequential_tuples(self, mock_get_q_eps_single):
        mock_get_q_eps_single.side_effect = [(), (), ('2022-11-06', 0.1), ('2022-08-02', 0.2), ('2022-05-02', 0.3), (), ('2021-11-03', 0.4), ('2021-08-05', 0.5), ('2021-05-31', 0.6)]
        expected_list = [(), ('2022-11-06', 0.1), ('2022-08-02', 0.2), ('2022-05-02', 0.3), (), ('2021-11-03', 0.4), ('2021-08-05', 0.5), ('2021-05-31', 0.6)]
        first_to_third_list = db_functions.get_first_to_third_list(self.ticker, self.cycle, self.a_eps_list)
        self.assertEqual(first_to_third_list, expected_list)

    @patch('db_functions.get_q_eps_single')
    def test_get_first_to_third_list_with_empty_tuple_at_index_one_and_fourth_q_data_present(self, mock_get_q_eps_single):
        mock_get_q_eps_single.side_effect = [(), ('2022-11-06', 0.5), ('2022-08-02', 0.5), ('2022-05-02', 0.5), (), ('2021-11-03', 0.5), ('2021-08-05', 0.5), ('2021-05-31', 0.5)]
        expected_list = [(), ('2022-11-06', 0.5), ('2022-08-02', 0.5), ('2022-05-02', 0.5), (), ('2021-11-03', 0.5), ('2021-08-05', 0.5), ('2021-05-31', 0.5)]
        first_to_third_list = db_functions.get_first_to_third_list(self.ticker, self.cycle, self.a_eps_list)
        self.assertEqual(first_to_third_list, expected_list)

    @patch('db_functions.get_q_eps_single')
    def test_get_first_to_third_list_with_empty_tuple_at_first_index_and_no_fourth_q_data(self, mock_get_q_eps_single):
        mock_get_q_eps_single.side_effect = [(), ('2023-04-17', 0.5), (), ('2022-11-06', 0.5), ('2022-08-02', 0.5), ('2022-05-02', 0.5), (), ('2021-11-03', 0.5), ('2021-08-05', 0.5), ('2021-05-31', 0.5)]
        expected_list = [('2023-04-17', 0.5), (), ('2022-11-06', 0.5), ('2022-08-02', 0.5), ('2022-05-02', 0.5), (), ('2021-11-03', 0.5), ('2021-08-05', 0.5), ('2021-05-31', 0.5)]
        first_to_third_list = db_functions.get_first_to_third_list(self.ticker, self.cycle, self.a_eps_list)
        self.assertEqual(first_to_third_list, expected_list)

    @patch('db_functions.get_q_eps_single')
    def test_get_first_to_third_list_with_two_empty_tuples_and_three_items_after_each(self, mock_get_q_eps_single):
        mock_get_q_eps_single.side_effect = [('2022-08-02', 0.5), ('2022-05-02', 0.5), (), ('2021-11-03', 0.5), ('2021-08-05', 0.5), ('2021-05-31', 0.5), (), ('2020-11-07', 0.5), ('2020-08-06', 0.5), ('2020-05-07', 0.5), (), ('2019-11-04', 0.5)]
        expected_list = [('2022-08-02', 0.5), ('2022-05-02', 0.5), (), ('2021-11-03', 0.5), ('2021-08-05', 0.5), ('2021-05-31', 0.5), (), ('2020-11-07', 0.5), ('2020-08-06', 0.5), ('2020-05-07', 0.5)]
        first_to_third_list = db_functions.get_first_to_third_list(self.ticker, self.cycle, self.a_eps_list)
        self.assertEqual(first_to_third_list, expected_list)

    @patch('db_functions.get_q_eps_single')
    def test_get_first_to_third_list_with_seven_items_and_one_empty_tuple(self, mock_get_q_eps_single):
        mock_get_q_eps_single.side_effect = [('2022-11-06', 0.5), ('2022-08-02', 0.5), ('2022-05-02', 0.5), (), ('2021-11-03', 0.5), ('2021-08-05', 0.5), ('2021-05-31', 0.5), (), ('2020-11-07', 0.5), ('2020-08-06', 0.5), ('2020-05-07', 0.5), (), ('2019-11-04', 0.5)]
        expected_list = [('2022-11-06', 0.5), ('2022-08-02', 0.5), ('2022-05-02', 0.5), (), ('2021-11-03', 0.5), ('2021-08-05', 0.5), ('2021-05-31', 0.5)] 
        first_to_third_list = db_functions.get_first_to_third_list(self.ticker, self.cycle, self.a_eps_list)
        self.assertEqual(first_to_third_list, expected_list)


class TestGetSplitData(TestCase):
    def test_get_split_data_with_data_present(self):
        splits = db_functions.get_split_data('GOOG')
        all_items_are_tuples = all(type(split) == tuple for split in splits)
        split_date = datetime.strptime(splits[0][0], '%Y-%m-%d')
        split_factor = splits[0][1]
        self.assertIsInstance(splits, list)
        self.assertTrue(all_items_are_tuples)
        self.assertIsInstance(split_date, datetime)
        self.assertIsInstance(split_factor, float)

    def test_get_split_data_with_no_data(self):
        splits_result = db_functions.get_split_data('AVGO') #This test will fail if AVGO splits later.
        self.assertFalse(splits_result)


class TestAdjustIfSplit(TestCase):
    q_eps_list = [('2022-08-02', 0.1), ('2022-05-02', 0.2), ('2022-02-06', 0.3), (), ('2021-08-05', 0.4), ('2021-05-02', 0.5), ('2021-02-04', 0.6)]

    def test_adjust_if_split_with_date_in_range(self):
        split_data_in_date_range = [('2021-12-15', 2), ('2015-08-19', 3)]
        expected_list = [('2022-08-02', 0.1), ('2022-05-02', 0.2), ('2022-02-06', 0.3), (), ('2021-08-05', 0.8), ('2021-05-02', 1.0), ('2021-02-04', 1.2)]
        adjusted_data = db_functions.adjust_if_split(split_data_in_date_range, self.q_eps_list)
        adjusted_data_rounded = [(q_eps[0], round(q_eps[1], 1)) if len(q_eps) > 0  else q_eps for q_eps in adjusted_data]
        self.assertEqual(adjusted_data_rounded, expected_list)

    def test_adjust_if_split_with_date_out_of_range(self):
        split_data_out_of_date_range = [('2018-05-03', 2), ('2003-09-18', 3)]
        unadjusted_data = db_functions.adjust_if_split(split_data_out_of_date_range, self.q_eps_list)
        self.assertEqual(unadjusted_data, self.q_eps_list)


class TestAddFourthQEPS(TestCase):
    def test_add_fourth_q_eps(self):
        q_eps_list = [(), ('2022-08-02', 0.1), ('2022-05-02', 0.2), ('2022-02-06', 0.3), (), ('2021-08-05', 0.4), ('2021-05-02', 0.5), ('2021-02-04', 0.6)]
        a_eps_list = [('2022-11-03', 1.0), ('2021-11-03', 2.0), ('2020-11-03', 3.0), ('2019-11-03', 4.0)]
        expected_list = [('2022-11-03', 0.4), ('2022-08-02', 0.1), ('2022-05-02', 0.2), ('2022-02-06', 0.3), ('2021-11-03', 0.5), ('2021-08-05', 0.4), ('2021-05-02', 0.5), ('2021-02-04', 0.6)]
        q_eps_list_fourth_q_added = db_functions.add_fourth_q_eps(q_eps_list, a_eps_list)
        q_eps_list_fourth_q_added_rounded = [(q_eps[0], round(q_eps[1], 1)) for q_eps in q_eps_list_fourth_q_added]
        self.assertEqual(q_eps_list_fourth_q_added_rounded, expected_list)


class TestGetQEPSList(TestCase):
    ticker = 'TEST' #Value of ticker doesn't affect the result. Return value of functions that accept it as an argument are provided by mock functions.
    a_eps_list = [('2022-11-03', 1.0), ('2021-11-03', 2.0), ('2020-11-03', 3.0), ('2019-11-03', 4.0)]
    split_data_in_date_range = [('2021-12-15', 2), ('2015-08-19', 3)]
    split_data_out_of_date_range = [('2018-05-03', 2), ('2003-09-18', 3)]
    expected_list_with_splits = [('2022-11-03', 0.4), ('2022-08-02', 0.1), ('2022-05-02', 0.2), ('2022-02-06', 0.3), ('2021-11-03', -1.0), ('2021-08-05', 0.8), ('2021-05-02', 1.0), ('2021-02-04', 1.2)]
    expected_list_without_splits = [('2022-11-03', 0.4), ('2022-08-02', 0.1), ('2022-05-02', 0.2), ('2022-02-06', 0.3), ('2021-11-03', 0.5), ('2021-08-05', 0.4), ('2021-05-02', 0.5), ('2021-02-04', 0.6)]

    @patch('db_functions.generate_current_cycle', return_value=None)
    @patch('db_functions.get_first_to_third_list', return_value=False)
    def test_get_q_eps_list_invalid(self, mock_get_first_to_third_list, mock_generate_current_cycle):
        q_eps_list_result = db_functions.get_q_eps_list(self.ticker, self.a_eps_list)
        self.assertFalse(q_eps_list_result)

    @patch('db_functions.generate_current_cycle', return_value=None)
    @patch('db_functions.get_first_to_third_list')
    @patch('db_functions.get_split_data', return_value=False)
    def test_get_q_eps_list_with_no_split_data(self, mock_get_split_data, mock_get_first_to_third_list, mock_generate_current_cycle):
        first_to_third_list = [(), ('2022-08-02', 0.1), ('2022-05-02', 0.2), ('2022-02-06', 0.3), (), ('2021-08-05', 0.4), ('2021-05-02', 0.5), ('2021-02-04', 0.6)]
        mock_get_first_to_third_list.return_value = first_to_third_list
        q_eps_list_without_splits = db_functions.get_q_eps_list(self.ticker, self.a_eps_list)
        q_eps_list_without_splits_rounded = [(q_eps[0], round(q_eps[1], 1)) for q_eps in q_eps_list_without_splits]
        self.assertEqual(q_eps_list_without_splits_rounded, self.expected_list_without_splits)

    @patch('db_functions.generate_current_cycle', return_value=None)
    @patch('db_functions.get_first_to_third_list')
    @patch('db_functions.get_split_data')
    def test_get_q_eps_list_with_split_data_out_of_date_range(self, mock_get_split_data, mock_get_first_to_third_list, mock_generate_current_cycle):
        first_to_third_list = [(), ('2022-08-02', 0.1), ('2022-05-02', 0.2), ('2022-02-06', 0.3), (), ('2021-08-05', 0.4), ('2021-05-02', 0.5), ('2021-02-04', 0.6)]
        mock_get_split_data.return_value = self.split_data_out_of_date_range
        mock_get_first_to_third_list.return_value = first_to_third_list
        q_eps_list_with_splits_out_of_date_range = db_functions.get_q_eps_list(self.ticker, self.a_eps_list)
        q_eps_list_with_splits_out_of_date_range_rounded = [(q_eps[0], round(q_eps[1], 1)) for q_eps in q_eps_list_with_splits_out_of_date_range]
        self.assertEqual(q_eps_list_with_splits_out_of_date_range_rounded, self.expected_list_without_splits)

    @patch('db_functions.generate_current_cycle', return_value=None)
    @patch('db_functions.get_first_to_third_list')
    @patch('db_functions.get_split_data')
    def test_get_q_eps_list_with_split_data_in_date_range(self, mock_get_split_data, mock_get_first_to_third_list, mock_generate_current_cycle):
        first_to_third_list = [(), ('2022-08-02', 0.1), ('2022-05-02', 0.2), ('2022-02-06', 0.3), (), ('2021-08-05', 0.4), ('2021-05-02', 0.5), ('2021-02-04', 0.6)]
        mock_get_split_data.return_value = self.split_data_in_date_range
        mock_get_first_to_third_list.return_value = first_to_third_list
        q_eps_list_with_splits = db_functions.get_q_eps_list(self.ticker, self.a_eps_list)
        q_eps_list_with_splits_rounded = [(q_eps[0], round(q_eps[1], 1)) for q_eps in q_eps_list_with_splits]
        self.assertEqual(q_eps_list_with_splits_rounded, self.expected_list_with_splits)


class TestGetCompanyDetails(TestCase):
    def test_get_company_details_available(self):
        company_details = db_functions.get_company_details('AAPL')
        company_name = list(company_details.values())[0]
        company_description_is_str = type(list(company_details.values())[1]) == str
        self.assertIsInstance(company_details, dict)
        self.assertIn('Apple', company_name)
        self.assertTrue(company_description_is_str)

    def test_get_company_details_unavailable(self):
        no_details_result = db_functions.get_company_details('NOTATICKER') #ticker for which there is no data (fake, in this case)
        all_values_unavailable = all(val == 'unavailable' for val in no_details_result.values())
        self.assertIsInstance(no_details_result, dict)
        self.assertTrue(all_values_unavailable)


class TestGetInstitutionalHolders(TestCase):
    def test_get_institutional_holders(self):
        institutional_holders = db_functions.get_institutional_holders('AAPL')
        self.assertIsInstance(institutional_holders, int)


class TestRateOfChange(TestCase):
    positive_num_1 = 5
    positive_num_2 = 8
    negative_num_1 = -7
    negative_num_2 = -3

    def test_rate_of_change_with_different_positives(self):
        roc = db_functions.rate_of_change(self.positive_num_2, self.positive_num_1)
        self.assertEqual(roc, 60)

    def test_rate_of_change_with_same_positives(self):
        roc = db_functions.rate_of_change(self.positive_num_1, self.positive_num_1)
        self.assertEqual(roc, 0)

    def test_rate_of_change_with_one_negative(self):
        roc_result = db_functions.rate_of_change(self.positive_num_1, self.negative_num_1)
        self.assertIsNone(roc_result)

    def test_rate_of_change_with_both_negative(self):
        roc_result = db_functions.rate_of_change(self.negative_num_1, self.negative_num_2)
        self.assertIsNone(roc_result)


class TestMakeCompanyDict(TestCase):
    @patch('db_functions.get_company_details', return_value={'name': 'Company Name', 'description': 'Company Description'})
    @patch('db_functions.get_institutional_holders', return_value=1234)
    def test_make_company_dict(self, mock_get_institutional_holders, mock_get_company_details):
        ticker = 'TEST' #Value of ticker doesn't affect the result. Return value of functions that accept it as an argument are provided by mock functions.
        a_eps_list = [('2022-11-03', 1.0), ('2021-11-03', 2.0), ('2020-11-03', 3.0), ('2019-11-03', 4.0)]
        q_eps_list = [('2022-11-03', 0.4), ('2022-08-02', 0.1), ('2022-05-02', 0.2), ('2022-02-06', 0.3), ('2021-11-03', 0.5), ('2021-08-05', 0.4), ('2021-05-02', 0.5), ('2021-02-04', 0.6)]
        expected_dict = {'ticker': 'TEST', 'name': 'Company Name', 'description': 'Company Description', 'q_eps_growth_first': -20.0, 'q_eps_growth_next': -75.0, 'q_eps_growth_last': -60.0, 'a_eps_growth_first': -50.0, 'a_eps_growth_next': -33.3, 'a_eps_growth_last': -25.0, 'institutional_holders': 1234}
        company_dict = db_functions.make_company_dict(ticker, a_eps_list, q_eps_list)
        company_dict_rounded = company_dict
        company_dict_rounded['q_eps_growth_first'] = round(company_dict['q_eps_growth_first'], 1)
        company_dict_rounded['q_eps_growth_next'] = round(company_dict['q_eps_growth_next'], 1)
        company_dict_rounded['q_eps_growth_last'] = round(company_dict['q_eps_growth_last'], 1)
        company_dict_rounded['a_eps_growth_first'] = round(company_dict['a_eps_growth_first'], 1)
        company_dict_rounded['a_eps_growth_next'] = round(company_dict['a_eps_growth_next'], 1)
        company_dict_rounded['a_eps_growth_last'] = round(company_dict['a_eps_growth_last'], 1)
        self.assertEqual(company_dict_rounded, expected_dict)


class TestUpdateCompany(TestCase):
    def setUp(self):
        Company.query.delete()
        company = Company(
                ticker='TESTUPDATE',
                name='Company name',
                description='Company description',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        db.session.add(company)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_update_company(self):
        company_dict = {
                'name': 'Company name updated',
                'description': 'Company description updated',
                'q_eps_growth_first': 0.9,
                'q_eps_growth_next': 8.7,
                'q_eps_growth_last': 6.5,
                'a_eps_growth_first': 4.3,
                'a_eps_growth_next': 2.1,
                'a_eps_growth_last': 0.9,
                'institutional_holders': 4321
            }
        company_to_update = Company.query.filter_by(ticker='TESTUPDATE').first()
        db_functions.update_company(company_to_update, company_dict)
        updated_company = Company.query.filter_by(ticker='TESTUPDATE').first()
        self.assertEqual(updated_company.name, 'Company name updated')
        self.assertEqual(updated_company.description, 'Company description updated')
        self.assertEqual(updated_company.q_eps_growth_first, Decimal('0.9'))
        self.assertEqual(updated_company.q_eps_growth_next, Decimal('8.7'))
        self.assertEqual(updated_company.q_eps_growth_last, Decimal('6.5'))
        self.assertEqual(updated_company.a_eps_growth_first, Decimal('4.3'))
        self.assertEqual(updated_company.a_eps_growth_next, Decimal('2.1'))
        self.assertEqual(updated_company.a_eps_growth_last, Decimal('0.9'))
        self.assertEqual(updated_company.institutional_holders, 4321)


class TestAddNewCompany(TestCase):
    def setUp(self):
        Company.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_add_new_company(self):
        company_dict = {
                'ticker': 'TESTADD',
                'name': 'New company name',
                'description': 'New company description',
                'q_eps_growth_first': 0.9,
                'q_eps_growth_next': 8.7,
                'q_eps_growth_last': 6.5,
                'a_eps_growth_first': 4.3,
                'a_eps_growth_next': 2.1,
                'a_eps_growth_last': 0.9,
                'institutional_holders': 4321
            }
        db_functions.add_new_company(company_dict)
        new_company = Company.query.filter_by(ticker='TESTADD').first()
        self.assertEqual(new_company.ticker, 'TESTADD')
        self.assertEqual(new_company.name, 'New company name')
        self.assertEqual(new_company.description, 'New company description')
        self.assertEqual(new_company.q_eps_growth_first, Decimal('0.9'))
        self.assertEqual(new_company.q_eps_growth_next, Decimal('8.7'))
        self.assertEqual(new_company.q_eps_growth_last, Decimal('6.5'))
        self.assertEqual(new_company.a_eps_growth_first, Decimal('4.3'))
        self.assertEqual(new_company.a_eps_growth_next, Decimal('2.1'))
        self.assertEqual(new_company.a_eps_growth_last, Decimal('0.9'))
        self.assertEqual(new_company.institutional_holders, 4321)


class TestDeleteEnqueuedTicker(TestCase):
    def setUp(self):
        EnqueuedTicker.query.delete()
        et = EnqueuedTicker(ticker='TESTDELETE')
        db.session.add(et)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_delete_enqueued_ticker(self):
        db_functions.delete_enqueued_ticker('TESTDELETE')
        deleted_et = EnqueuedTicker.query.filter_by(ticker='TESTDELETE').first()
        self.assertIsNone(deleted_et)


class TestReconcileTickers(TestCase):
    def setUp(self):
        Company.query.delete()
        apple = Company(
                ticker='AAPL',
                name='Apple, Inc.',
                description='Apple description',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        company_1 = Company(
                ticker='TESTRECONCILE1',
                name='Company name',
                description='Company description',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        company_2 = Company(
                ticker='TESTRECONCILE2',
                name='Company name',
                description='Company description',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        db.session.add(apple)
        db.session.add(company_1)
        db.session.add(company_2)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_reconcile_tickers_removes_db_tickers(self):
        api_tickers = ['AAPL']
        db_tickers = ['TESTRECONCILE1', 'AAPL', 'TESTRECONCILE2']
        expected_tickers = api_tickers
        db_functions.reconcile_tickers(api_tickers, db_tickers)
        reconciled_db_tickers = [company.ticker for company in Company.query.all()]
        self.assertCountEqual(reconciled_db_tickers, expected_tickers)


class TestUpdateTickerQueue(TestCase):
    def setUp(self):
        EnqueuedTicker.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_update_ticker_queue(self):
        tickers_to_enqueue = ['TESTUPDATE1', 'TESTUPDATE2', 'TESTUPDATE3', 'TESTUPDATE4']
        expected_tickers = tickers_to_enqueue
        db_functions.update_ticker_queue(tickers_to_enqueue)
        enqueued_tickers = [et.ticker for et in EnqueuedTicker.query.all()]
        self.assertCountEqual(enqueued_tickers, expected_tickers)


class TestUpdateDb(TestCase):
    def setUp(self):
        Company.query.delete()
        company_1 = Company(
                ticker='TESTEXISTING1',
                name='Company name',
                description='Company description',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        company_2 = Company(
                ticker='TESTEXISTING2',
                name='Company name',
                description='Company description',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        company_3 = Company(
                ticker='TESTEXISTING3',
                name='Company name',
                description='Company description',
                q_eps_growth_first=1.2,
                q_eps_growth_next=3.4,
                q_eps_growth_last=5.6,
                a_eps_growth_first=7.8,
                a_eps_growth_next=9.0,
                a_eps_growth_last=1.2,
                institutional_holders=1234
            )
        db.session.add(company_1)
        db.session.add(company_2)
        db.session.add(company_3)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    tickers = ['TESTEXISTING1', 'TESTEXISTING2', 'TESTNEW', 'TESTEXISTING3']

    @patch('db_functions.delete_enqueued_ticker', return_value=None)
    @patch('db_functions.add_new_company', return_value=None)
    @patch('db_functions.update_company', return_value=None)
    @patch('db_functions.make_company_dict')
    @patch('db_functions.get_q_eps_list')
    @patch('db_functions.get_a_eps_list')
    def test_update_db_with_new_and_existing_tickers(self, mock_get_a_eps_list, mock_get_q_eps_list, mock_make_company_dict, mock_update_company, mock_add_new_company, mock_delete_enqueued_ticker):
        mock_get_a_eps_list.side_effect = [['test_existing_1_a_eps_list'], ['test_existing_2_a_eps_list'], ['test_new_a_eps_list'], ['test_existing_3_a_eps_list']]
        mock_get_q_eps_list.side_effect = [['test_existing_1_q_eps_list'], ['test_existing_2_q_eps_list'], ['test_new_q_eps_list'], ['test_existing_3_q_eps_list']]
        mock_make_company_dict.side_effect = [{'test_existing_1_key': 'test_existing_1_value'}, {'test_existing_2_key': 'test_existing_2_value'}, {'test_new_key': 'test_new_value'}, {'test_existing_3_key': 'test_existing_3_value'}]
        db_functions.update_db(self.tickers)
        self.assertEqual(mock_delete_enqueued_ticker.call_count, 4)
        self.assertEqual(mock_update_company.call_count, 3)
        self.assertEqual(mock_add_new_company.call_count, 1)

    @patch('db_functions.delete_enqueued_ticker', return_value=None)
    @patch('db_functions.add_new_company', return_value=None)
    @patch('db_functions.update_company', return_value=None)
    @patch('db_functions.make_company_dict')
    @patch('db_functions.get_q_eps_list')
    @patch('db_functions.get_a_eps_list')
    def test_update_db_continues_with_a_eps_list_false(self, mock_get_a_eps_list, mock_get_q_eps_list, mock_make_company_dict, mock_update_company, mock_add_new_company, mock_delete_enqueued_ticker):
        mock_get_a_eps_list.side_effect = [['test_existing_1_a_eps_list'], ['test_existing_2_a_eps_list'], False, ['test_existing_3_a_eps_list']]
        mock_get_q_eps_list.side_effect = [['test_existing_1_q_eps_list'], ['test_existing_2_q_eps_list'], ['test_existing_3_q_eps_list']]
        mock_make_company_dict.side_effect = [{'test_existing_1_key': 'test_existing_1_value'}, {'test_existing_2_key': 'test_existing_2_value'}, {'test_existing_3_key': 'test_existing_3_value'}]
        db_functions.update_db(self.tickers)
        self.assertEqual(mock_update_company.call_count, 3)
        self.assertEqual(mock_add_new_company.call_count, 0)

    @patch('db_functions.delete_enqueued_ticker', return_value=None)
    @patch('db_functions.add_new_company', return_value=None)
    @patch('db_functions.update_company', return_value=None)
    @patch('db_functions.make_company_dict')
    @patch('db_functions.get_q_eps_list')
    @patch('db_functions.get_a_eps_list')
    def test_update_db_continues_with_q_eps_list_false(self, mock_get_a_eps_list, mock_get_q_eps_list, mock_make_company_dict, mock_update_company, mock_add_new_company, mock_delete_enqueued_ticker):
        mock_get_a_eps_list.side_effect = [['test_existing_1_a_eps_list'], ['test_existing_2_a_eps_list'], ['test_new_a_eps_list'], ['test_existing_3_a_eps_list']]
        mock_get_q_eps_list.side_effect = [['test_existing_1_q_eps_list'], ['test_existing_2_q_eps_list'], False, ['test_existing_3_q_eps_list']]
        mock_make_company_dict.side_effect = [{'test_existing_1_key': 'test_existing_1_value'}, {'test_existing_2_key': 'test_existing_2_value'}, {'test_existing_3_key': 'test_existing_3_value'}]
        db_functions.update_db(self.tickers)
        self.assertEqual(mock_update_company.call_count, 3)
        self.assertEqual(mock_add_new_company.call_count, 0)

    @patch('db_functions.delete_enqueued_ticker', return_value=None)
    @patch('db_functions.add_new_company', return_value=None)
    @patch('db_functions.update_company', return_value=None)
    @patch('db_functions.make_company_dict')
    @patch('db_functions.get_q_eps_list')
    @patch('db_functions.get_a_eps_list')
    def test_update_db_continues_with_unexpected_exception(self, mock_get_a_eps_list, mock_get_q_eps_list, mock_make_company_dict, mock_update_company, mock_add_new_company, mock_delete_enqueued_ticker):
        mock_get_a_eps_list.side_effect = [['test_existing_1_a_eps_list'], ['test_existing_2_a_eps_list'], ['test_new_a_eps_list'], ['test_existing_3_a_eps_list']]
        mock_get_q_eps_list.side_effect = [['test_existing_1_q_eps_list'], ['test_existing_2_q_eps_list'], IndexError('tuple index out of range'), ['test_existing_3_q_eps_list']]
        mock_make_company_dict.side_effect = [{'test_existing_1_key': 'test_existing_1_value'}, {'test_existing_2_key': 'test_existing_2_value'}, {'test_existing_3_key': 'test_existing_3_value'}]
        db_functions.update_db(self.tickers)
        self.assertEqual(mock_update_company.call_count, 3)
        self.assertEqual(mock_add_new_company.call_count, 0)
