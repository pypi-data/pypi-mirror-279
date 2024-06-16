import time
class Timer:
    def __init__(self):
        pass

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def get_interval(self) -> float:
        return self.end_time - self.start_time
