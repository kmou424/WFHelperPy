import time

from lib.utils import Args


class Timer:
    def __init__(self):
        self.clock = time.perf_counter()

    def resetClock(self):
        self.clock = time.perf_counter()

    def run(self, mArgs: Args):
        mThisTaskRunningTime = time.perf_counter() - self.clock
