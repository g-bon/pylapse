import asyncio
from functools import partial


class PeriodicTask(object):
    def __init__(self, func, interval):
        self.func = func
        self.interval = interval
        self.ret_value = None
        self._loop = asyncio.get_event_loop()
        self._set()

    def _set(self):
        self._handler = self._loop.call_later(self.interval, self._run)

    def _run(self):
        self.ret_value = partial(self.func, self.ret_value)()
        self._set()

    def stop(self):
        self._handler.cancel()
