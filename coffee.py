"""
Main algorithm exploring a graph to find N//2 unique pairs of employees among N employees
"""

__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ["Meeting", "Coffee"]

from employee import Employee
from graph import Vertex, Graph
from linkedlist import LinkedList
import random
from decorator_timer import Timer


class Meeting():
    """A meeting for a pair of employees"""
    def __init__(self, employee1, employee2):
        self.employee1 = employee1
        self.employee2 = employee2

    def __str__(self):
        return '(' + str(self.employee1.data.name) + ', ' + str(self.employee2.data.name) + ')'


class Coffee():
    """Create the graph and explores it to find N//2 unique pairs of employees"""

    class _Week():
        """Iterator finding for each of the N//2 iterations a new set of unique set of N//2 pairs"""
        def __init__(self, planning, *, endless=False, signal=None, algo=0):
            self.planning = planning
            self.endless = endless
            self.signal = signal
            self.algo=algo

        def check(self, pairing):
            """Check that a set of pairs of employees meet the expectations:
            * N//2 pairs
            * Each employee in these pairs appears only once
            * all N employees are paired up

            The algorithms shall by default implement natively these properties
            However too many algorithms failed, hence this extra safety net as a QA assessment
            """
            assert len(pairing) == len(self.planning), f'{len(self.planning) - len(pairing)} meetings still need to be booked'

            employees = dict()
            for employee in self.planning.planning:
                employees[employee] = False

            for meeting in pairing:
                employees[meeting.employee1] = True
                employees[meeting.employee2] = True

            for employee in employees:
                assert employees[employee], f'{employee.id} has not been booked'
                pass 

        def __iter__(self):
            return self

        def __next__(self):
            # running the pairing exploration for a given sorting algo
            pairing = self.planning.schedule(termination=self.signal, sorting_algo=self.algo)

            if self.endless:
                # section of the code dealing with a random number of N//2 pairs
                # especially for the "restart" tag to tell a new N-1 sequence has started
                restart = False
                if self.signal and self.signal.is_set():
                    # handling the abort signal for the multi-threaded approach
                    return [],False

                if len(pairing) == 0:
                    restart=True
                    self.planning.reset()
                    pairing = self.planning.schedule(termination=self.signal, sorting_algo=self.algo)

                self.check(pairing)
                return pairing, restart

            # section of code covering the defaulted N-1 sequence
            if len(pairing) == 0:
                raise StopIteration()
                
            self.check(pairing)
            return pairing


    def __init__(self, employees):
        self.employees = employees
        self.planning = None

        self.reset()

    def reset(self):
        self.planning = Graph()
        for idx,employee in enumerate(self.employees):
            self.planning.add(Vertex(idx, employee))

        for idx,v1 in enumerate(self.planning):
            for idx2 in range(idx+1,len(self.planning)):
                v1.add(self.planning[idx2])

    def __len__(self):
        return len(self.employees) // 2
    
    def __iter__(self):
        """basic iterator"""
        return Coffee._Week(self)
    
    def feed(self, *, endless=False, asynchronous_signal=None, sorting_algo=None):
        """iterator handling more advanced fine tuned features like multi-threading or sorting algorith selection"""
        return Coffee._Week(self, endless=endless, signal=asynchronous_signal, algo=sorting_algo)

    def schedule(self, *, termination=None, sorting_algo=0):
        """Explore the graph of possibilities to find N//2 pairs is they exist"""

        def browse(employees, available, meetings, length):
            """recusrive helper to find the next correct candidate pair"""

            if len(employees) == 0:
                """no more employees to process, they've all been paired up"""
                return
            
            if not available[employees[0]]:
                """this employee has already been paired, hence not available anymore"""
                return
            
            # employee candidate
            employee = employees.pop(0)
            available[employee] = False

            for neighbor in sorted(employee.neighbors, key=lambda x:-x.id):
                # explore each neighbor until one is available AND allows to find N//2 pairs total
                if not available[neighbor]:
                    continue

                available[neighbor] = False
                meetings.append((employee,neighbor))
                browse(employees, available, meetings, length)

                if len(meetings) == length:
                    return
                available[neighbor] = True
                meetings.pop()

            available[employee] = True
            employees.append(employee)

        # getting an idea of how many nodes still need to be processed in the worst case scenario
        # helped to identify the deadlock when there was not enough employees to properly pair up
        #print(self.complexity())
        available   = dict()
        employees   = []
        edges       = list()
        meetings    = LinkedList()


        # important heuristics to sort the vertices according to a sorting strategy
        match sorting_algo:
            case 0:
                sorted_vertices=sorted(self.planning.vertices, key=lambda x:(len(x),x.id))
            case 1:
                sorted_vertices=sorted(self.planning.vertices, key=lambda x:(-len(x),x.id))
            case 2:
                sorted_vertices=sorted(self.planning.vertices, key=lambda x:(-len(x),-x.id))
            case 3:
                sorted_vertices=sorted(self.planning.vertices, key=lambda x:(len(x),-x.id))
            case 4:
                # this random shuffling strategy means that if we shuffle the vertices enough times
                # a proper list will be found to find the N//2 pairs
                sorted_vertices = list(self.planning.vertices)
                random.shuffle(sorted_vertices)
            case _:
                sorted_vertices=sorted(self.planning.vertices, key=lambda x:(len(x),x.id))

        #for node in an ordered set of vertices:
        for node in sorted_vertices:
            if len(node) != 0:
                employees.append(node)
            available[node] = True
        
        while True:
            if termination and termination.is_set():
                # handling of asynchronous termination signal coming from outside
                return []
            
            if len(edges) == len(self):
                # all N//2 pairs were found
                break

            if len(employees) == 0:
                # no more employees to pair up
                # this test may be redundant with the previous one
                break
            browse(employees, available, edges, len(self))
            



        if termination and termination.is_set():
            # in case the process was aborted, return nothing since the data are meaningless
            return []
            
        # critical section to update the graph by removing the edges between the employees
        # who've been paired up so that they're not picked during the next iterations
        # that section can ONLY be exercised if no abort signal has been raised

        # QA assertion - can be disabled via the __debug__ option
        assert len(edges) in [0,len(self)], f'bug: {len(edges)} != [0, {len(self)}]'


        for employee1, employee2 in edges:
            if employee1 in employee2.neighbors:
                employee2.remove(employee1)
            if employee2 in employee1.neighbors:
                employee1.remove(employee2)
            meetings.append(Meeting(employee1, employee2))

        return meetings
        


@Timer(enable=True,timeout=None)
def main():
    employees = [Employee() for _ in range(4)]
    coffee = Coffee(employees)

    for idx, meetings in enumerate(coffee):
        print(f'week {idx+1}', meetings)

if __name__ == "__main__":
    main()
    

"""
test_creation (__main__.TestCoffee.test_creation) ... ok
test_feed (__main__.TestCoffee.test_feed) ... ok
test_feed_endless (__main__.TestCoffee.test_feed_endless) ... ok
test_feed_sorting (__main__.TestCoffee.test_feed_sorting) ... ok
test_feed_termination (__main__.TestCoffee.test_feed_termination) ... ok
test_iter (__main__.TestCoffee.test_iter) ... ok
test_creation (__main__.TestMeeting.test_creation) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.004s

OK
"""