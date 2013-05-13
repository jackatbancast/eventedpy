import threading
import json
from queue import Queue, Empty
import re
import time
import datetime
import uuid

class Event:
    """Basic Event, not needed, but useful to pass addition data in the events"""
    def __init__(self, type="", *args, **kwargs):
        self.type = type
        self.args = args
        self.kwargs = kwargs

class EventLoop(threading.Thread):
    """A simple event loop that spawns :max_threads: number of threads
    to handle events
    
    Example Usage:
        loop = eventedpy.EventLoop()
        loop.start()
        loop.on("message", print)

        loop.add(eventedpy.Event('message now', message='hello world')))
        #Would print `<Event>`
    """
    def __init__(self, maxsize=0, max_threads=32, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.listeners = {}
        self.oneshots = {}
        self.queue = Queue()
        self.__max_threads = max_threads
        self.__threads = []
        self.processed_events = 0
        
        self.on('__setTimeout', self.__timed_timeout)
        self.on('__setInterval', self.__timed_interval)
        self.on('__setImmediate', self.__timed_immediate)

    def set_queue(self, maxsize=0):
        self.queue = Queue(maxsize)
        return queue

    def __start_joiner(self):
        self.__joiner_running = True
        while self.__joiner_running:
            for t in self.__threads:
                try:
                    t.join(timeout=0.0001)#attempt to kill thread quickly
                    if not t.is_alive():
                        self.__threads.pop(self.__threads.index(t))
                except RuntimeError:
                    continue

    def __kill_joiner(self):
        self.__joiner_running = False
        if self.__joiner_thread.is_alive():
            self.__joiner_thread.join()

    def add(self, evt):
        self.queue.put(evt)

    def on(self, pattern, function):
        evt = re.compile(pattern)
        if not evt in self.listeners.keys():
            self.listeners[evt] = []
        if not function in self.listeners[evt]:
            self.listeners[evt].append(function)

    @property
    def threads(self):
        return len(self.__threads)

    def run(self):
        self.__joiner_thread = threading.Thread(target=self.__start_joiner)
        self.__joiner_thread.start()
        self.__running = True
        while self.__running:
            evt = None
            while self.__running and not evt:
                try:
                    evt = self.queue.get_nowait()
                except Empty:
                    evt = None
            self.processed_events += 1
            try:
                evt_type = evt.type
            except AttributeError:
                evt_type = str(evt)
            for pattern in self.listeners.keys():
                if pattern.match(evt_type):
                    for function in self.listeners[pattern]:
                        while len(self.__threads) >= self.__max_threads:
                            pass
                        self.__threads.append(threading.Thread(target=function, args=evt.args, kwargs=evt.kwargs))
                        self.__threads[-1].start()

    def join(self, timeout=None):
        self.__running = False
        self.__kill_joiner()
        threading.Thread.join(self, timeout)

    def __timed_timeout(self, *args, **kwargs):
        time = datetime.datetime.utcnow()
        __function = kwargs['__function']
        __time = kwargs['__time']
        if __time < time:
            del kwargs['__function']
            del kwargs['__time']
            __function(*args, **kwargs)
        else:
            self.add(Event('__setTimeout', __time=__time, __function=__function, *args, **kwargs))

    def __timed_interval(self, *args, **kwargs):
        time = datetime.datetime.utcnow()
        __delay = kwargs['__delay']
        __function = kwargs['__function']
        __time = kwargs['__time']
        if __time < time:
            del kwargs['__function']
            del kwargs['__time']
            del kwargs['__delay']
            __function(*args, **kwargs)
        else:
            pass
        __time = time + datetime.timedelta(seconds=__delay)
        self.add(Event(
            '__setInterval',
             __time=__time,
             __function=__function,
             __delay=__delay,
             *args, **kwargs))

    def __timed_immediate(self, *args, **kwargs):
        kwargs['__function'](*args, **kwargs)

    def setInterval(self, time, function, *args, **kwargs):
        time = time/1000#so that time can be specified in ms
        self.add(Event(
            '__setInterval',
            __time=datetime.datetime.utcnow() + datetime.timedelta(seconds=time),
            __delay = time,
            __function=function
            *args, **kwargs))

    def setTimeout(self, time, function, *args, **kwargs):
        time = time/1000#so that time can be specified in ms
        self.add(Event(
            '__setTimeout',
            __time=datetime.datetime.utcnow() + datetime.timedelta(seconds=time),
            __function = function,
            *args, **kwargs))

    def setImmediate(self, function, *args, **kwargs):
        self.add(Event('__setImmediate', __function=function, *args, **kwargs))
