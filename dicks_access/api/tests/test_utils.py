import unittest
import responses
import datetime
from freezegun import freeze_time
from unittest.mock import patch

from utils import (
    check_employee_termination_date_set,
    check_employee_start_date,
    check_employee_exclude_list,
    fetch_realm_digital_employees,
    check_leap_year,
    get_message_recipients
)


class TestUtils(unittest.TestCase):

    @freeze_time('2022-06-14')
    def test_check_employee_termination_date_set_true(self):
        today = datetime.datetime.today()
        current_date = datetime.datetime.strftime(today, '%Y-%m-%d')
        employee_end_date = datetime.datetime.strptime("2022-06-30T00:00:00", "%Y-%m-%dT%H:%M:%S")
        response = check_employee_termination_date_set(current_date, employee_end_date)
        self.assertEqual(response, True)

    @freeze_time('2022-07-01')
    def test_check_employee_termination_date_set_false(self):
        today = datetime.datetime.today()
        current_date = datetime.datetime.strftime(today, '%Y-%m-%d')
        employee_end_date = datetime.datetime.strptime("2022-06-30T00:00:00", "%Y-%m-%dT%H:%M:%S")
        response = check_employee_termination_date_set(current_date, employee_end_date)
        self.assertEqual(response, False)

    @freeze_time('2022-07-01')
    def test_check_employee_start_date_true(self):
        today = datetime.datetime.today()
        current_date = datetime.datetime.strftime(today, '%Y-%m-%d')
        employee_start_date = datetime.datetime.strptime("2022-06-30T00:00:00", "%Y-%m-%dT%H:%M:%S")
        employee_end_date = None
        birthday_monday_day = datetime.datetime.strptime("2022-07-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
        response = check_employee_start_date(birthday_monday_day, employee_start_date, current_date, employee_end_date)
        self.assertEqual(response, True)

    @freeze_time('2022-06-29')
    def test_check_employee_start_date_false(self):
        today = datetime.datetime.today()
        current_date = datetime.datetime.strftime(today, '%Y-%m-%d')
        employee_start_date = datetime.datetime.strptime("2022-06-30T00:00:00", "%Y-%m-%dT%H:%M:%S")
        employee_end_date = None
        birthday_monday_day = datetime.datetime.strptime("2022-06-29T00:00:00", "%Y-%m-%dT%H:%M:%S")
        response = check_employee_start_date(birthday_monday_day, employee_start_date, current_date, employee_end_date)
        self.assertEqual(response, False)

    @responses.activate
    def test_check_employee_exclude_list_true(self):
        responses.add(
            responses.GET,
            "https://interview-assessment-1.realmdigital.co.za/do-not-send-birthday-wishes",
            json=[1, 2, 3],
            status=200,
        )
        response = check_employee_exclude_list(1)
        self.assertEqual(response, True)

    @responses.activate
    def test_check_employee_exclude_list_error(self):
        responses.add(
            responses.GET,
            "https://interview-assessment-1.realmdigital.co.za/do-not-send-birthday-wishes",
            status=500,
        )

        with self.assertRaises(Exception) as exception_context:
            check_employee_exclude_list(1)
        self.assertEqual(
            str(exception_context.exception),
            "Error retrieving employee exclusion data"
        )

    @responses.activate
    def test_fetch_realm_digital_employees_true(self):
        employees = [
            {'hello': 'world'}
        ]
        responses.add(
            responses.GET,
            "https://interview-assessment-1.realmdigital.co.za/employees",
            json=employees,
            status=200,
        )

        response = fetch_realm_digital_employees()
        self.assertEqual(response, employees)

    @responses.activate
    def test_fetch_realm_digital_employees_error(self):
        responses.add(
            responses.GET,
            "https://interview-assessment-1.realmdigital.co.za/employees",
            status=500,
        )

        with self.assertRaises(Exception) as exception_context:
            fetch_realm_digital_employees()
        self.assertEqual(
            str(exception_context.exception),
            "Error retrieving employee data"
        )

    def test_check_leap_year_true(self):
        self.assertEqual(check_leap_year(2020, "03-29"), True)

    def test_check_leap_year_false(self):
        self.assertEqual(check_leap_year(2021, "04-29"), False)

    @freeze_time('2022-06-01')
    @responses.activate
    @patch('utils.check_employee_termination_date_set')
    @patch('utils.check_employee_start_date')
    @patch('utils.check_employee_exclude_list')
    @patch('utils.check_leap_year')
    def test_get_message_recipients(
            self,
            mock_check_leap_year,
            mock_check_employee_exclude_list,
            mock_check_employee_start_date,
            mock_check_employee_termination_date_set,
    ):

        employee_list = [
            {
                "id": 100,
                "name": "TestNew21",
                "lastname": "Test123",
                "dateOfBirth": "1960-06-01T00:00:00",
                "employmentStartDate": "2001-03-01T00:00:00",
                "employmentEndDate": None,
                "lastNotification": "2022-03-16T12:16:03.5156964+02:00",
                "lastBirthdayNotified": "2021-03-01"
            }
        ]

        responses.add(
            responses.GET,
            "https://interview-assessment-1.realmdigital.co.za/employees",
            json=employee_list,
            status=200,
        )

        mock_check_employee_termination_date_set.return_value = False
        mock_check_employee_start_date.return_value = True
        mock_check_employee_exclude_list.return_value = False
        mock_check_leap_year.return_value = False

        response = get_message_recipients()

        self.assertEqual(response, ['TestNew21 Test123'])

