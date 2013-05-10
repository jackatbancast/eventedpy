import threading
import json
from queue import Queue, Empty
import re

class Event:
    def __init__(self, type="", *args, **kwargs):
        self.type = data.get('type') or type
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
        self.queue = Queue()
        self.__max_threads = max_threads
        self.__threads = []
        self.processed_events = 0

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
                        self.__threads.append(threading.Thread(target=function, args=(evt,)))
                        self.__threads[-1].start()

    def join(self, timeout=None):
        self.__running = False
        self.__kill_joiner()
        threading.Thread.join(self, timeout)
