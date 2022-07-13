from employee_birthday_service import EmployeeBirthdays


class MessageFactory:
    def get_message(self, message_type):
        if message_type == 'Birthdays':
            return EmployeeBirthdays()
        else:
            raise ValueError(f"Invalid message type: {message_type}")