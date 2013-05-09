import threading
import json
import datetime
from queue import Queue

EXIT = -1
UNKNOWN = 0

class BaseEvent:
    def __init__(self, type=UNKNOWN, data={}, *args, **kwargs):
        self.type = data.get('type') or type
        self.data = data
        self.timestamp = datetime.datetime.utcnow()
        self.args = args
        self.kwargs = kwargs

class EventLoop(threading.Thread):
    def __init__(self, handler, maxsize=0, max_threads=32, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.handler = handler
        self.queue = Queue()
        self.__max_threads = max_threads
        self.__threads = []

    def set_queue(self, maxsize=0):
        self.queue = Queue(maxsize)
        return queue

    def __start_joiner(self):
        self.__joiner_running = True
        while self.__joiner_running:
            for t in self.__threads:
                try:
                    t.join(timeout=0.0001)
                    if not t.is_alive():
                        self.__threads.pop(self.__threads.index(t))
                except RuntimeError:
                    continue

    def __kill_joiner(self):
        self.__joiner_running = False
        self.__joiner_thread.join()

    def add(self, evt):
        self.queue.put(evt)

    def run(self):
        self.__joiner_thread = threading.Thread(target=self.__start_joiner)
        self.__joiner_thread.start()
        self.__running = True
        while self.__running:
            evt = self.queue.get() 
            try:
                if evt.type == EXIT:
                    self.__running = False
                    break
            except AttributeError:
                continue
            while len(self.__threads) >= self.__max_threads:
                pass
            self.__threads.append(threading.Thread(target=self.handler, args=(evt,)))
            self.__threads[-1].start()

    def join(self, timeout=None):
        self.add(BaseEvent(EXIT))
        self.__kill_joiner()
        threading.Thread.join(self, timeout)
