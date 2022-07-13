import unittest

from employee_birthday_service import EmployeeBirthdays


class TestEmployeeBirthdays(unittest.TestCase):
    def test_employee_birthday_return_message(self):
        employee_list = ["Harry Potter", "Money Maker"]
        emp_birthday_obj = EmployeeBirthdays()
        response_message = emp_birthday_obj.message(employee_list)
        self.assertEqual(response_message, "Happy Birthday Harry Potter, Money Maker")

    def test_employee_birthday_return_empty_list(self):
        employee_list = []
        emp_birthday_obj = EmployeeBirthdays()
        response_message = emp_birthday_obj.message(employee_list)
        self.assertEqual(response_message, [])