
from threading import Event,Thread
import time
from random import randint, choice
from typing import Dict,TypeAlias

ID:TypeAlias=int
Duration:TypeAlias=int

class ZoomSession:
    def __init__(self, timeout:Duration):
        self.conversations = dict()

        # everybod says "hello"
        self.call('start')

        # bye bye time to leave
        self.call('stop')

        self.zoom = None

        self.call_length = timeout

        def host(call_length, phone):
            # the host has just joined and let everybody joining
            phone.talk('start')
            # emulating the duration of the session
            time.sleep(call_length)

        self.zoom = Thread(target=host, args=(self.call_length, self))

    def start(self):
        """the host starts the session"""
        self.zoom.start()

    def end(self):
        """the session ends"""
        self.zoom.join()
        self.talk('stop')

    def call(self, call_):
        """create a channel of communication"""
        self.conversations[call_] = Event()

    def talk(self, call_):
        """start talking in a channel of communication"""
        self.conversations[call_].set()

    def listen(self, call_):
        """listen from a channel of communication"""
        return self.conversations[call_].is_set()

    def operator(self, call_):
        """operator places the call on hold"""
        self.conversations[call_].wait()


def attendant(name:ID, engagement:Dict, zoom:ZoomSession, engagement_threshold:int):
    actions = ['talks', 'draws', 'shows code', 'asks', 'answers', 'discusses', 'complains', 'sighs']
    
    # when using threads, the results have to be passed by reference
    engagement[name] = list()

    #wait until the session starts
    zoom.operator('start')

    # keep doing (or not doing)
    while True:
        for _ in range(engagement_threshold):

            # stop when the session ends
            if zoom.listen('stop'):
                return
            time.sleep(1)

        # time to participate
        engagement[name].append(choice(actions))


# how many people attend the session
MAX_ATTENDANTS = 15
# how long the zoom session lasts
ZOOM_SESSION_TIME = 10
# meta-data to emulate the level of engagement from 1 (very active) to SLACK (poorly active)
SLACK = 20

attendants = list()
participation = dict()

zoom = ZoomSession(ZOOM_SESSION_TIME)

for idx in range(MAX_ATTENDANTS):
    attendants.append(Thread(target=attendant, args=(idx, participation, zoom, randint(1,SLACK),)))
    attendants[idx].start()

zoom.start()
# zoom meeting is happening
# bla bla bla
# more bla bla bla
# finally...
zoom.end()

# let's check everybody's participation
for person in participation:
    print(f'{person+1}: {participation[person]}')



