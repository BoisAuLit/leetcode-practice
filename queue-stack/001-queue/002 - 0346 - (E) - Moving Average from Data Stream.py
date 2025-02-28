from collections import deque
        
class MovingAverage:

    def __init__(self, size: int):
        self.sum = 0
        self.capacity = size
        self.current_size = 0
        self.queue = deque()

    def next(self, val: int) -> float:
        self.queue.append(val)
        self.sum += val
        self.current_size += 1
        if len(self.queue) > self.capacity:
            self.sum -= self.queue.popleft()
            self.current_size -= 1
        return self.sum / self.current_size


ma = MovingAverage(3)
print(ma.next(1))
print(ma.next(10))
print(ma.next(3))
print(ma.next(5))
