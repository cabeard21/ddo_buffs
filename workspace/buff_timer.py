import time


class BuffTimer:

    def __init__(self):
        self.timers = {}

    def update(self, buff, time_value):
        self.timers[buff] = time_value + time.time()

    def get_remaining(self, buff):
        if (time.time() - self.timers[buff]) > 0:
            return 0
        else:
            return self.timers[buff] - time.time()
