import abc


class Employee(metaclass=abc.ABCMeta):
    def message(self, param):
        pass