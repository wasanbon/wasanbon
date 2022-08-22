import threading


class TimeoutTask(threading.Thread):
    def __init__(self, func, var=None):
        super(TimeoutTask, self).__init__()
        self._stop_event = threading.Event()

        self._var = var

        self._func = func

    def run(self):
        self._func(self._var)

    def quit(self):
        self._stop_event.set()


def task_with_wdt(task_func, arg, interval):
    t = TimeoutTask(task_func, arg)
    t.start()

    def kill_thread():
        t.quit()
    wdt = threading.Timer(interval, kill_thread)
    wdt.start()
    t.join()
    wdt.cancel()
