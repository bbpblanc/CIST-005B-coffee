
from main import Main,Termination
import unittest
import sys
import os



class TestIntegration(unittest.TestCase):
    def test_000(self):
        args = ['--employees', '0']
        with self.assertRaises(Termination):
            Main(args)

    def test_odd(self):
        FILE = 'test.txt'

        for idx in range(20,30):
            if idx & 1 == 0:
                continue
            args = ['--employees', str(idx)]
            out = sys.stdout
            with open(FILE,'w',encoding='utf-8') as fd:
                sys.stdout = fd
                try:
                    Main(args)
                except Termination:
                    pass
            sys.stdout = out

            with open(FILE,'r',encoding='utf-8') as fd:
                buf = fd.read()
                self.assertEqual(len(buf.split('\n')),2)

        os.remove(FILE)

    def _test_run(self, employees, *, sorting=None, timeout=None, data=None):
        FILE = 'test.txt'

        args = ['--employees', str(employees)]
        if sorting is not None:
            args += ['--sorting', str(sorting)]
        if timeout is not None:
            args += ['--timeout', str(timeout)]

        out = sys.stdout
        err = sys.stderr
        with self.assertRaises(Termination):
            with open(FILE,'w',encoding='utf-8') as fd:
                sys.stdout = fd
                sys.stderr = fd
                try:
                    Main(args)
                except Termination as e:
                    raise e
                except:
                    raise Termination()
        sys.stdout = out
        sys.stderr = err

        with open(FILE,'r',encoding='utf-8') as fd:
            buf = fd.read().rstrip('\n').split('\n')
            if data is None:
                self.assertEqual(len(buf),employees)
                self.assertTrue(buf[0].startswith('Employees'))
                self.assertTrue(buf[-1].startswith('week ' + str(employees-1)))
            else:
                data[0] = buf

        os.remove(FILE)

    def _test_good_bad_sorting(self,employees,good,bad):
        data = [None]
        for algo in bad:
            self._test_run(employees, sorting=algo, data=data)
            self.assertEqual(len(data[0]),1)
        
        for algo in good:
            self._test_run(employees, sorting=algo)


    def test_002(self):
        self._test_run(2)

    def test_004(self):
        self._test_run(4)

    def test_006(self):
        self._test_run(6)

    def test_008(self):
        self._test_run(8)

    def test_010(self):
        # problematic
        self._test_run(10)

    def test_010_deep(self):
        self._test_good_bad_sorting(10, good=[1], bad=[0,2,3,4])
    
    def test_012(self):
        self._test_run(12)

    def test_014(self):
        self._test_run(14)

    def test_016(self):
        # problematic
        self._test_run(16)

    def test_016_deep(self):
        self._test_good_bad_sorting(16, good=[2,3,4], bad=[0,1])

    def test_018(self):
        self._test_run(18)

    def test_020(self):
        self._test_run(20)

    def test_022(self):
        self._test_run(22)

    def test_024(self):
        self._test_run(24)

    def test_026(self):
        self._test_run(26)

    def test_028(self):
        self._test_run(28)

    def test_030(self):
        self._test_run(30)

    def test_032(self):
        self._test_run(32)

    def test_036(self):
        self._test_run(36, timeout=2)

    def test_038(self):
        # needs a bit higher throttle
        self._test_run(38, timeout=5)

    def test_040(self):
        # needs a bit higher throttle
        self._test_run(40, timeout=5)

    def test_042(self):
        # needs a bit higher throttle
        self._test_run(42, timeout=5)

    @unittest.skip
    def test_044(self):
        # does not terminate timely
        pass

    @unittest.skip
    def test_046(self):
        # does not terminate timely
        pass

    def test_weeks(self):
        FILE = 'test.txt'
        employees = 4
        weeks = 10

        args = ['--employees', str(employees), '--weeks', str(weeks)]

        out = sys.stdout
        err = sys.stderr
        with self.assertRaises(Termination):
            with open(FILE,'w',encoding='utf-8') as fd:
                sys.stdout = fd
                sys.stderr = fd
                try:
                    Main(args)
                except Termination as e:
                    raise e
                except:
                    raise Termination()
        sys.stdout = out
        sys.stderr = err

        with open(FILE,'r',encoding='utf-8') as fd:
            buf = fd.read().rstrip('\n').split('\n')
            self.assertEqual(len(buf),weeks+1)
            self.assertTrue(buf[0].startswith('Employees'))

            if weeks % (employees-1) == 1:
                self.assertTrue(buf[-2].startswith('week ' + str(weeks-1)))
                self.assertTrue(buf[-1].startswith('(Repeat)week ' + str(weeks)))
            else:
                self.assertTrue(buf[-1].startswith('week ' + str(weeks)))

        os.remove(FILE)




class TestIntegration2():
    def _test_run(self, employees, *, sorting=None, timeout=None, data=None):
        FILE = 'test.txt'

        args = ['--employees', str(employees)]
        if sorting is not None:
            args += ['--sorting', str(sorting)]
        if timeout is not None:
            args += ['--timeout', str(timeout)]

        out = sys.stdout
        err = sys.stderr
        with self.assertRaises(Termination):
            with open(FILE,'w',encoding='utf-8') as fd:
                sys.stdout = fd
                sys.stderr = fd
                try:
                    Main(args)
                except Termination as e:
                    raise e
                except:
                    raise Termination()
        sys.stdout = out
        sys.stderr = err

        with open(FILE,'r',encoding='utf-8') as fd:
            buf = fd.read().rstrip('\n').split('\n')
            if data is None:
                self.assertEqual(len(buf),employees)
                self.assertTrue(buf[0].startswith('Employees'))
                self.assertTrue(buf[-1].startswith('week ' + str(employees-1)))
            else:
                data[0] = buf

        os.remove(FILE)

    def _test_good_bad_sorting(self,employees,good,bad):
        data = [None]
        for algo in bad:
            self._test_run(employees, sorting=algo, data=data)
            self.assertEqual(len(data[0]),1)
        
        for algo in good:
            self._test_run(employees, sorting=algo)

    def test_weeks(self):
        FILE = 'test.txt'
        employees = 4
        weeks = 10

        args = ['--employees', str(employees), '--weeks', str(weeks)]

        out = sys.stdout
        err = sys.stderr
        with self.assertRaises(Termination):
            with open(FILE,'w',encoding='utf-8') as fd:
                sys.stdout = fd
                sys.stderr = fd
                try:
                    Main(args)
                except Termination as e:
                    raise e
                except:
                    raise Termination()
        sys.stdout = out
        sys.stderr = err

        with open(FILE,'r',encoding='utf-8') as fd:
            buf = fd.read().rstrip('\n').split('\n')
            self.assertEqual(len(buf),weeks+1)
            self.assertTrue(buf[0].startswith('Employees'))

            if weeks % (employees-1) == 1:
                self.assertTrue(buf[-2].startswith('week ' + str(weeks-1)))
                self.assertTrue(buf[-1].startswith('(Repeat)week ' + str(weeks)))
            else:
                self.assertTrue(buf[-1].startswith('week ' + str(weeks)))

        os.remove(FILE)

if __name__ == "__main__":
    unittest.main(argv=['ignore'], exit=False, verbosity=2)

