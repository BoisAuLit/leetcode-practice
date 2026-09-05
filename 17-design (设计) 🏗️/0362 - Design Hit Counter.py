from collections import deque

"""
Time complexity: O()
Space complexity: O()
"""


class HitCounter:
    def __init__(self):
        self.deque = deque()

    def hit(self, timestamp: int) -> None:
        self.deque.appendleft(timestamp)
        while timestamp - self.deque[-1] > 300:
            self.deque.pop()

    def getHits(self, timestamp: int) -> int:
        return sum(1 for t in self.deque if timestamp - t < 300)


h = HitCounter()
h.hit(1)
h.hit(2)
h.hit(3)
print(h.getHits(4))
h.hit(300)
print(h.getHits(300))
print(h.getHits(301))
