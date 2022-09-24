class FloatRange:
    """same as built it range(start,stop,step) but with floats
    """

    def __init__(self, start, stop=None, step=1):
        if stop is None:
            self.start = 0
            self.stop = start
        else:
            self.start = start
            self.stop = stop
        self.step = step
        self.curr = self.start

    def __iter__(self):
        return self

    def __next__(self) -> float:
        res = self.curr
        self.curr += self.step
        if (self.curr > self.stop and self.step > 0) or (self.curr < self.stop and self.step < 0):
            raise StopIteration()
        return res
