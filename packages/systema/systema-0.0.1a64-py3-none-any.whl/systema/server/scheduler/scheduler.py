import threading
import time
from contextlib import contextmanager

from schedule import get_jobs, run_pending

from systema.server.scheduler.jobs import add_jobs


class Scheduler:
    def __init__(self, interval: float = 1.0) -> None:
        self._stop_event = threading.Event()
        self.interval = interval

    def start(self):
        print("Starting scheduler...")

        scheduler_instance = self

        class ScheduleThread(threading.Thread):
            def run(self):
                if not get_jobs():
                    add_jobs()
                while not scheduler_instance._stop_event.is_set():
                    run_pending()
                    time.sleep(scheduler_instance.interval)

        ScheduleThread().start()

    def stop(self):
        print("Stopping scheduler...")

        self._stop_event.set()

    @contextmanager
    def run(self):
        self.start()
        yield
        self.stop()
