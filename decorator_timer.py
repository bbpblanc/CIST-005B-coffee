"""Timer decorator"""

__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ['Timer']

from typing import TypeAlias
from threading import Thread
import time
import functools

Seconds:TypeAlias=int

class Timer():
    """Decorator with two purposes: logging the elapsed time, and acting as a timeout"""

    def __init__(self, enable:bool=True, *, timeout:Seconds=None):
        """Create a timer which logs the elapsed time and and acts as a timeout
        :param bool enable: enables the feature to display the elapsed time
        :param Seconds timeout: enables the timer to abort the execution after N seconds
        :return: None
        """
        self.enable = enable
        self.timeout = timeout

    def __call__(self, func):
        """Magic dunder method to write for a class-based decorator
        """

        @functools.wraps(func) # this decorator allows the python help to properly display the arguments 
        def wrapper(*args, **kargs):

            def _execute_function(func,result,*args,**kargs):
                # helper function to get the result of the called function by reference
                result[0] = func(*args, **kargs)

            if self.timeout:
                # the timeout feature is enabled
                try:
                    # with the usage of threads, no data are returned.
                    # To access the returned data, the targetted function shall provide this data by reference
                    # only a python list allows this trick: the content of the list is mutable and a nifty way
                    # to communicate data both ways between the caller and the callee
                    data = [None]

                    # creation of the thread which runs the code to execute including its parameters *args and **kargs
                    # a given parameter is the data to return by reference
                    # the thread is run as a daemon in the background, hence the main calling thread can proceed forward
                    code_to_execute = Thread(target=_execute_function, args=(func,data,*args), kwargs={**kargs}, daemon=True)

                    # instrumentation of the code to compute later the elapsed time
                    start = time.time()
                    # start the thread
                    code_to_execute.start()

                    # that is THE feature of the threading mechanism that I leveraged to implement the timeout
                    # usually the join method blocks the process until the thread finishes
                    # the timeout parameter is blocking up to the timeout is reached
                    # join does not return any data
                    code_to_execute.join(timeout=self.timeout)

                    # since join does not return any data, I need to figure out whether the thread
                    # terminated naturally or not
                    if code_to_execute.is_alive():
                        # if the timeout occurred (i.e. the thread is still alive), I abort any
                        # further execution which become pointless
                        raise TimeoutError(f'{self.timeout}-second Timer')

                    # if the thread properly terminated, further processing may happen
                    # instrumentation of the code to log the elapsed time
                    elapsed = time.time() - start

                    # the function inside the thread produced some data and stored them as reference
                    # that data is available to the main process as the result of the executed function
                    result = data[0]
                except TimeoutError as e:
                    #print(e)
                    raise e
            else:
                # no timer enabled, the exceution of the function will lasts as much as needed
                # no need to run the function in a thread
                start = time.time()
                result = func(*args, **kargs)
                elapsed = time.time() - start

            
            if self.enable:
                # displaying the elapsed time if requested
                minutes = int(elapsed) // 60
                seconds = int(elapsed % 60)
                print(f'elapsed time: {minutes:02d} minutes {seconds:02d} seconds')

            return result
        
        return wrapper
    