import asyncio
from functools import partial
from pylapse.configuration import debug
from pylapse.utils import calculate_interval, TcpLikeStrategy


class PeriodicTask(object):
    def __init__(self, func, interval=None):
        self.func = func
        self.hash = None
        self.prev_hash = None
        self.strategy = TcpLikeStrategy()
        self.interval = interval if interval else calculate_interval(self.strategy)
        self._loop = asyncio.get_event_loop()
        self._set()

    def _set(self):
        self._handler = self._loop.call_later(self.interval, self._run)

    def _run(self):
        self.hash, self.prev_hash = partial(self.func, self.hash)()

        if (self.hash == self.prev_hash) or (self.prev_hash is None):
            action = "increase"
            if debug:
                print("No new image found for {}".format(self.func.args[0]))

        else:
            action = "decrease"
            if debug:
                print("New image found for {}".format(self.func.args[0]))

        self.interval = calculate_interval(self.strategy, action)

        if debug:
            print("Next timeout for {} {}d to {}s using strategy {}\n".format(self.func.args[0],
                                                                              action,
                                                                              self.interval,
                                                                              self.strategy.__class__.__name__))

        self._set()

    def stop(self):
        self._handler.cancel()
