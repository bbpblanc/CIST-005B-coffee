"""Main class
Run the command without argument or with -h to get a descriptio of the CLI
For a given number of employees N, the program finds N-1 unique N//2 pairs.

The algorithm is based on a graph exploration.

It is possible that N-k unique N//2 pairs are found while not being 
possible to find any further unique N//2 pairs for k with k > 1.

Different sorting strategies to process the employees are possible.
This program implemented 5 of them. The option --sorting allows to pick
any of these sorting strategies individually. The strategy by default
exercises each of them until it finds one which would output the N-1 unique
N//2 pairs. A timer sets to 1 second gives a chance for a startegy to complete
before sending a kill signal. According to the mass of data to process, the 
--timeout option allows to increase the throttle. It is still possible tho
that none of these strategies provide a N-1 saturated set.

Threads were used to implement this try-an-fail strategy, leading to heavily
instrument the code to be sensitive to the killing signal. Using processes 
instead would have avoided such instrumentation by sending a SIGTERM signal.
I chose the threading approach.
"""


__author__ = "Bertrand Blanc (Alan Turing)"

from coffee import Meeting,Coffee
from employee import Employee,Employees
import argparse
import sys

from decorator_timer import Timer
from threading import Thread,Event
import time

class Termination(Exception):
    pass

class Main():
    def __init__(self, *args, **kargs):
        self.parser = None
        if len(*args) == 0:
            args=[['-h']]

        self._cli()
        self.args = self.parser.parse_args(*args)
        self._dispatch()

    def _cli(self):
        """Definition of the CLI arguments"""
        self.parser = argparse.ArgumentParser(
            prog='main.py',
            description='Creates the weekly coffee pairing for the employees',
            epilog='Thanks for using my program',
        )

        self.parser.add_argument('--author', help="author", action='store_true')
        self.parser.add_argument('--sorting', help="sorting mechanism to use. Different sorting strategies", nargs='?', type=int, default=-1, choices=[0,1,2,3,4])
        self.parser.add_argument('--timer', help="enables the timer to monitor the elapsed time", action='store_true')
        self.parser.add_argument('--timeout', help="aborts the execution after N seconds. Dafault to 1s. May help giving more time to complete", action='store', type=int, metavar='N', default=1)
        self.parser.add_argument('--employees', '-e', help="number of employees", action='store', type=int, metavar='<integer>')
        self.parser.add_argument('--weeks', '-w', help="generate the pairing for this number of weeks", action='store', type=int, metavar='<integer>')

    def _dispatch(self):
        """Find out what part of code to trigger based on the CLI arguments"""
        if self.args.author:
            self._author()
            self._terminate()

        if self.args.employees:
            # semantical properties and assumptions on employees
            if self.args.employees <= 0:
                print(f'the number of employees shall be positive')
                self._terminate(-1)

            if self.args.employees % 2:
                print(f'the number of employees shall be an even number')
                self._terminate(-1)

            self._run()
            self._terminate()

        self._terminate(-1)

        
    def _author(self):
        print('Bertrand Blanc (Alan Turing)')

    def _run(self):
        def _timeout(n, signal, inc=0.01):
            """timeout function triggering a signal once the time lapses
            The timer can be interrupted if the signal has been raised by
            another thread.
            """
            cpt = 0
            while not signal.is_set() and cpt < n:
                time.sleep(inc)
                cpt += inc
            signal.set()

        # timeout setting for the following decorator allowing to display
        # the elapsed time and/or to abort a too long execution
        timeout = self.args.timeout if self.args.sorting >= 0 else None

        @Timer(self.args.timer, timeout=timeout)
        def _execute(self, employees:Employees, *, sorting_algo=None, signal=None, data:dict={}) -> None:
            """This is the core algorith to exercise the different sorting mechanism to find
            the N-1 N//2 pairs of unique employees
            :employees: list of employees
            :sorting algo: allows to select the algorith to run. None to select the one by default.
            :signal: signal to communicate the termonation of the process/thread
            :data: threads don't return data, hence the data are passed by reference
            data['finished'] = True - the algo terminated. False - the algo was interrupted.
            data['data'] = str of N-1 saturated pairs of employees upon successful completion.
            """

            assert self.args.employees % 2 == 0, "BUG, the number of employees shall be even"

            data['finished'] = False
            data['data'] = f'Employees: {employees}\n'

            if self.args.weeks:
                # I implemented an option to produce the saturated lists of pairs for a random number of weeks
                # The number can be < N-1
                # The number can be > N-1, a (Repeat) tag is displayed every time a new sequence of N-1 starts

                # note the usage of a more comprehensive iterator to add extra settings required for this multi-threaded approach
                # the basic __iter__ iterator cannot be used directly, hence implementing an iterator via __next__
                planning = Coffee(employees).feed(endless=True, asynchronous_signal=signal, sorting_algo=sorting_algo)
                for i in range(self.args.weeks):
                    meetings, new_set = next(planning)
                    data['data'] += f'{"(Repeat)" if new_set else ""}week {i+1}: {meetings}\n'
            else:
                # If this option is not set, the sequence of N-1 is generated
                # Basic iterator is used __iter__
                planning = Coffee(employees).feed(asynchronous_signal=signal, sorting_algo=sorting_algo)
                for i, meetings in enumerate(planning):
                    data['data'] += f'week {i+1}: {meetings}\n'


            if signal and not signal.is_set():
                # the algorithm successfully terminated without being aborted
                data['finished'] = True

            if signal is None:
                # if no signal was set, this means no multi-threaded approach was used
                # hence relying on basic arguments and a specific sorting algorithm.
                print(data['data'])
        

        # The declaration of the employees
        employees = Employees()
        employees.fill(number=self.args.employees)

        if self.args.sorting >= 0:
            # a specific sorting algorithm is selected (no multi-threading)
            _execute(self, employees, sorting_algo=self.args.sorting)
            return
        
        # No specific sorting algorithm is selected, hence the multi-threaded approach
        # to find a working strategy, if any
        timeout = self.args.timeout
        threads  = []
        timers   = []
        results  = []
        signal   = Event() # even to carry the abortion signal between threads

        for idx in range(5):
            # the results from the algo are passed by reference
            results.append(dict())
            # the thread running a specific algo
            threads.append(Thread(target=_execute, args=(self,employees), kwargs={'sorting_algo':idx, 'signal':signal, 'data':results[idx]}))
            # the timeout thread raising the abortion signal according to the timeout value (default 1 second, can be increased with --timeout option)
            timers.append(Thread(target=_timeout, args=(timeout, signal)))

        for thread,timer,result in zip(threads,timers,results):
            # iterating for each sorting strategy until one successfully completes
            signal.clear()
            thread.start()
            timer.start()
            
            timer.join()
            thread.join()

            if result.get('finished',False):
                print(result['data'])
                break


    def _terminate(self, exit_=0):
        termination = Termination()
        termination.exit_ = exit_
        raise termination

if __name__ == "__main__":
    try:
        Main(sys.argv[1:])
    except Termination as e:
        exit(e.exit_)
    except Exception as e:
        # catchall to elegantly terminate in case of unexpected exception
        print('Abnormal cause of premature termination:', e)
        exit(-3)
    exit(-2)


"""
test_000 (__main__.TestIntegration.test_000) ... ok
test_002 (__main__.TestIntegration.test_002) ... ok
test_004 (__main__.TestIntegration.test_004) ... ok
test_006 (__main__.TestIntegration.test_006) ... ok
test_008 (__main__.TestIntegration.test_008) ... ok
test_010 (__main__.TestIntegration.test_010) ... ok
test_010_deep (__main__.TestIntegration.test_010_deep) ... ok
test_012 (__main__.TestIntegration.test_012) ... ok
test_014 (__main__.TestIntegration.test_014) ... ok
test_016 (__main__.TestIntegration.test_016) ... ok
test_016_deep (__main__.TestIntegration.test_016_deep) ... ok
test_018 (__main__.TestIntegration.test_018) ... ok
test_020 (__main__.TestIntegration.test_020) ... ok
test_022 (__main__.TestIntegration.test_022) ... ok
test_024 (__main__.TestIntegration.test_024) ... ok
test_026 (__main__.TestIntegration.test_026) ... ok
test_028 (__main__.TestIntegration.test_028) ... ok
test_030 (__main__.TestIntegration.test_030) ... ok
test_032 (__main__.TestIntegration.test_032) ... ok
test_036 (__main__.TestIntegration.test_036) ... ok
test_038 (__main__.TestIntegration.test_038) ... ok
test_040 (__main__.TestIntegration.test_040) ... ok
test_042 (__main__.TestIntegration.test_042) ... ok
test_044 (__main__.TestIntegration.test_044) ... skipped ''
test_046 (__main__.TestIntegration.test_046) ... skipped ''
test_odd (__main__.TestIntegration.test_odd) ... ok
test_weeks (__main__.TestIntegration.test_weeks) ... ok

----------------------------------------------------------------------
Ran 27 tests in 638.379s

OK (skipped=2)
"""