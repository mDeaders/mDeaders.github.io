from datetime import datetime
from threading import Timer
import time


class InternalError(Exception):
    pass


def now():
    return datetime.now().strftime("%H:%M:%S")


def log(message):
    print(f"{now()} - {message}", flush=True)


class debounce(object):
    """
    Decorator postponing the decorated function execution until after @delay seconds have elapsed since the last time it was invoked.
    Several calls to the decorated fonction in the time interval result in one real call.
    """
    def __init__(self, delay):
        self.delay = delay
        self.timer = None

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            if self.timer is not None:
                self.timer.cancel()
            self.timer = Timer(self.delay, lambda: fn(*args, **kwargs))
            self.timer.start()
        return wrapped
