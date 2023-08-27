from collections import deque


class RecentCounter:
    def __init__(self):
        self.calls = deque()

    def ping(self, t: int) -> int:
        self.calls.append(t)
        while t - self.calls[0] > 3000:
            self.calls.popleft()

        return len(self.calls)


rc = RecentCounter()
print(rc.ping(642))
print()
print(rc.ping(1849))
print()
print(rc.ping(4921))
print()
print(rc.ping(5936))
print()
print(rc.ping(5957))
