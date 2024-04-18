
from employee import *
from linkedlist import LinkedList
import unittest

class TestEmployee(unittest.TestCase):
    def test_creation(self):
        e = Employee('foo')
        self.assertEqual(e.name, 'foo')

        e = Employee()
        self.assertEqual(e.name, str(e))

        employees = [Employee() for _ in range(100)]
        for idx,e1 in enumerate(employees):
            for e2 in employees[idx+1:]:
                self.assertFalse(e1.id == e2.id)

class TestEmployees(unittest.TestCase):
    def test_creation(self):
        es = Employees()
        self.assertTrue(issubclass(type(es),LinkedList))
    
    def test_fill(self):
        Employee._primary_key=0 # never do that!

        es = Employees()
        es.fill()
        self.assertEqual(len(es),0)

        es.fill(employees=22)
        self.assertEqual(len(es),0)

        es.fill(number=22)
        self.assertEqual(len(es),22)

        for idx in range(22):
            self.assertEqual(es[idx].id, idx)


if __name__ == "__main__":
    unittest.main(argv=['ignore'], exit=False, verbosity=2)
