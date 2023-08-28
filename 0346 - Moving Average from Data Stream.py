from collections import deque


class MovingAverage:
    def __init__(self, size: int):
        self.deque = deque()
        self.sum = 0
        self.size = size

    def next(self, val: int) -> float:
        if len(self.deque) == self.size:
            self.sum -= self.deque.popleft()
        self.deque.append(val)
        self.sum += val
        return self.sum / len(self.deque)
