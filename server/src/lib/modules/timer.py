import time as tm

class Timer:
    def __init__(self):
        self.time = tm.time()

    def tick(self):
        self._oldtime = self.time
        self.time = tm.time()
        self.deltaTime = self.time - self._oldtime
        return self.deltaTime

    def postpone(self, seconds, message = None):
        counter = 0
        while counter < seconds:
            counter += self.tick()
            tm.sleep(0.01)
        if message != None:
            print(message)