import unittest

from message_factory import MessageFactory
from employee_birthday_service import EmployeeBirthdays


class TestMessageFactory(unittest.TestCase):
    def test_get_message_return_class_obj(self):
        message_type = "Birthdays"
        factory = MessageFactory()
        factory_obj = factory.get_message(message_type)
        self.assertIsInstance(factory_obj, EmployeeBirthdays)

    def test_get_message_raise_error(self):
        message_type = "blah"
        factory = MessageFactory()
        with self.assertRaises(ValueError) as exception_context:
            factory.get_message(message_type)
        self.assertEqual(
            str(exception_context.exception),
            "Invalid message type: blah"
        )