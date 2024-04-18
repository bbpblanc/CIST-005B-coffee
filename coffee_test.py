
from coffee import *
from employee import *
import unittest
from linkedlist import LinkedList
from threading import Event

class TestMeeting(unittest.TestCase):
    def test_creation(self):
        e1 = Employee()
        e2 = Employee()
        m = Meeting(e1,e2)

        self.assertIs(m.employee1,e1)
        self.assertIs(m.employee2,e2)


class TestCoffee(unittest.TestCase):
    def test_creation(self):
        es = Employees()
        es.fill(number=4)
        coffee = Coffee(es)

        self.assertEqual(len(coffee),len(es)//2)

    def test_iter(self):
        es = Employees()
        es.fill(number=4)
        coffee = Coffee(es)

        cpt = 0
        for w in coffee:
            cpt += 1
            self.assertEqual(len(w),len(es)//2)
        self.assertEqual(cpt,len(es)-1)

    def test_feed(self):
        es = Employees()
        es.fill(number=4)
        coffee = Coffee(es)

        cpt = 0
        it = coffee.feed()

        try:
            while True:
                w = next(it)
                cpt += 1
                self.assertEqual(len(w),len(es)//2)
                # w is QA'ed on-the-fly inside the code
        except StopIteration:
            self.assertTrue(True)

        self.assertEqual(cpt,len(es)-1)

    def test_feed_endless(self):
        es = Employees()
        es.fill(number=4)
        coffee = Coffee(es)

        cpt = 0
        it = coffee.feed(endless=True)

        try:
            for _ in range(10):
                w = next(it)
                cpt += 1
                self.assertEqual(len(w),len(es)//2)
        except StopIteration:
            self.assertTrue(False)

        self.assertEqual(cpt,10)


    def test_feed_sorting(self):
        es = Employees()
        es.fill(number=4)
        coffee = Coffee(es)

        for algo in range(-2,10):
            cpt = 0
            it = coffee.feed(sorting_algo=algo)
            coffee.reset()

            try:
                while True:
                    w = next(it)
                    cpt += 1
                    self.assertEqual(len(w),len(es)//2)
            except StopIteration:
                self.assertTrue(True)

            self.assertEqual(cpt,len(es)-1)

    def test_feed_termination(self):
        es = Employees()
        es.fill(number=4)
        coffee = Coffee(es)
        sig = Event()

        cpt = 0
        it = coffee.feed(asynchronous_signal=sig)
        coffee.reset()

        try:
            while True:
                w = next(it)
                cpt += 1

                if not sig.is_set():
                    self.assertEqual(len(w),len(es)//2)
                    sig.set()
                else:
                    self.assertEqual(len(w),0)
                    break
        except StopIteration:
            self.assertTrue(True)

        self.assertEqual(cpt,1)


if __name__ == "__main__":
    unittest.main(argv=['ignore'], exit=False, verbosity=2)