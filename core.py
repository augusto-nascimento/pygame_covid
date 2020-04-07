import threading
from typing import Any
import functools

from pygame.color import THECOLORS


lock = threading.Lock()


def synchronized(lock: Any) -> Any:
    def wrapper(f: Any) -> Any:
        @functools.wraps(f)
        def inner_wrapper(*args: Any, **kw: Any) -> Any:
            with lock:
                return f(*args, **kw)
        return inner_wrapper
    return wrapper


class Singleton(type):
    _instances: dict = {}

    @synchronized(lock)
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = (
                super(Singleton, cls).__call__(*args, **kwargs)
                )
        return cls._instances[cls]


class Status(object):
    """docstring for Status."""
    def __init__(self, name: str, color: list, count: int):
        super(Status, self).__init__()
        self.name = name
        self.color = color
        self.count = count


class StatusHealth(object):
    healthy = Status('healthy', THECOLORS['green'], 0)
    contaminated = Status('contaminated', THECOLORS['yellow'], 0)
    sick = Status('sick', THECOLORS['orange'], 0)
    sick_icu = Status('sick_icu', THECOLORS['red'], 0)
    dead = Status('dead', THECOLORS['black'], 0)
    recovered = Status('recovered', THECOLORS['blue'], 0)


class Report(metaclass=Singleton):
    """docstring for Report."""
    def __init__(self):
        super(Report, self).__init__()
        self.healthy = StatusHealth.healthy
        self.contaminated = StatusHealth.contaminated
        self.sick = StatusHealth.sick
        self.sick_icu = StatusHealth.sick_icu
        self.dead = StatusHealth.dead
        self.recovered = StatusHealth.recovered
        self.max_sick = 0

    def get_report(self):
        report = {}
        for r in ['healthy', 'contaminated', 'sick', 'sick_icu', 'dead', 'recovered']:
            report[r] = getattr(self, r)
        return report

    def update(self, old_status, new_status):
        if old_status:
            o = getattr(self, old_status.name)
            o.count -= 1

        n = getattr(self, new_status.name)
        n.count += 1
        if self.max_sick < (self.sick.count + self.sick_icu.count):
            self.max_sick = self.sick.count + self.sick_icu.count
