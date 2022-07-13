from datetime import datetime
import requests
import calendar


def check_employee_termination_date_set(current_date: str, employee_end_date: str) -> bool:
    if employee_end_date is not None:
        employee_end_date = datetime.strftime(employee_end_date, '%Y-%m-%d')
        return True if current_date < employee_end_date else False
    return False


def check_employee_start_date(
        employee_birth_date: str, employee_start_date: str, current_date: str, employee_end_date: str
) -> bool:
    if employee_start_date is not None:

        employee_birth_date = datetime.strftime(employee_birth_date, '%m-%d')
        start_date = datetime.strftime(employee_start_date, '%m-%d')

        if employee_birth_date >= start_date and\
                not check_employee_termination_date_set(current_date, employee_end_date):
            return True
        else:
            return False
    return False


def check_employee_exclude_list(employee_id: int) -> bool:
    response = requests.get('https://interview-assessment-1.realmdigital.co.za/do-not-send-birthday-wishes')
    if response.ok:
        return True if str(employee_id) in response.text else False
    else:
        raise Exception(f"Error retrieving employee exclusion data")


def fetch_realm_digital_employees():
    response = requests.get('https://interview-assessment-1.realmdigital.co.za/employees')
    if response.ok:
        data = response.json()
        return data
    else:
        raise Exception(f"Error retrieving employee data")


def check_leap_year(current_year: str, date_of_birth: str) -> bool:
    return True if calendar.isleap(current_year) is True and date_of_birth == "03-29" else False


def get_message_recipients():
    employee_message_list = []
    employees = fetch_realm_digital_employees()

    today = datetime.today()
    current_date = datetime.strftime(today, '%Y-%m-%d')
    current_month_day = datetime.strftime(today, '%m-%d')
    current_year = datetime.strftime(today, '%Y')

    for employee in employees:

        employee_birth_date = datetime.strptime(employee['dateOfBirth'], '%Y-%m-%dT%H:%M:%S')
        birth_month_day = datetime.strftime(employee_birth_date, '%m-%d')

        emp_end_date = employee['employmentEndDate']
        if emp_end_date is not None:
            emp_end_date = datetime.strptime(employee['employmentEndDate'], '%Y-%m-%dT%H:%M:%S')

        emp_start_date = employee['employmentStartDate']
        if emp_start_date is not None:
            emp_start_date = datetime.strptime(employee['employmentStartDate'], '%Y-%m-%dT%H:%M:%S')

        if birth_month_day == current_month_day:

            if check_employee_exclude_list(employee['id']) is True:
                continue

            if any(
                    [
                        check_employee_termination_date_set(current_date, emp_end_date),
                        check_employee_start_date(birth_month_day, emp_start_date, current_date, emp_end_date),
                        check_leap_year(current_year)
                    ]
            ):
                employee_message_list.append(f"{employee['name']} {employee['lastname']}")

    return employee_message_list
