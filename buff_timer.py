import time


class BuffTimer:

    def __init__(self):
        self.timers = {}

    def update(self, buff, time_value):
        # Check if the new remaining time is greater than the current
        # remaining time
        if time_value > self.get_remaining(buff):
            self.timers[buff] = time_value + time.time()

    def get_remaining(self, buff):
        if buff not in self.timers or (time.time() - self.timers[buff]) > 0:
            return 0
        else:
            return self.timers[buff] - time.time()
