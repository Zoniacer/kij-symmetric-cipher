import time


class Timer():

    def __init__(self):
        pass

    def start(self):
        self.start = time.perf_counter_ns()

    def finish(self):
        self.elapsed = time.perf_counter_ns() - self.start
        self.elapsed = self.elapsed/pow(10,9)
        print(f"This process took {self.elapsed} seconds")
