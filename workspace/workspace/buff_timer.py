import time

class BuffTimer:
    def __init__(self):
        self.timers = {}

    def update(self, buff, time):
        self.timers[buff] = time

    def get_remaining(self, buff):
        return max(0, self.timers[buff] - time.time())
