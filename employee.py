"""Description of an employee
The list of employees is emulated here based on IDs.
A database may be connected here to feed the list of employees.
"""

__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ['Employee', 'Employees']

from threading import Lock
from linkedlist import LinkedList

class Employee():
    """Employee record with their badge ID and name"""
    _primary_key = 1
    _key_mutex = Lock()

    @staticmethod
    def primary_key() -> int:
        """Each employee is assigned a unique incrementing ID"""
        with Employee._key_mutex:
            # both of these operations are separately atomic
            # both of them needed to become an atomic unit
            # hence the usage of a mutex
            key = Employee._primary_key
            Employee._primary_key += 1
    
        return key

    def __init__(self, name:str=None):
        self.id = Employee.primary_key()
        self.name = name

        if not name:
            # The employee gets a name by default
            self.name = 'E' + format(self.id, "03d")

    def __str__(self) -> str:
        return str(self.name)
    

class Employees(LinkedList):
    def fill(self, *args, **kwargs):
        """Fill up the list of employees to process"""
        number_of_employees = kwargs.get('number',None)
        if number_of_employees is not None:
            [self.add(Employee()) for _ in range(number_of_employees)]


"""
test_creation (__main__.TestEmployee.test_creation) ... ok
test_creation (__main__.TestEmployees.test_creation) ... ok
test_fill (__main__.TestEmployees.test_fill) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.002s

OK
"""