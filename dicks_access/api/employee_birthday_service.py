from employee_interface import Employee


class EmployeeBirthdays(Employee):

    def message(self, employee_list: list):
        return f"Happy Birthday {', '.join(employee_list)}" if len(employee_list) > 0 else []
