import time


class Timer:
    def __init__(self):
        self.start = time.perf_counter()

    def reset(self):
        self.start = time.perf_counter()

    def getPassTime(self):
        return time.perf_counter() - self.start
