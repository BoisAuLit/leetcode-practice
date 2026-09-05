"""
Time complexity: O(1)
Space complexity: O(n)
"""


class Logger:
    def __init__(self):
        self.map = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if message not in self.map:
            self.map[message] = timestamp
            return True
        if timestamp - self.map[message] >= 10:
            self.map[message] = timestamp
            return True
        return False


timstamps = [1, 2, 3, 8, 10, 11]
messages = [
    "foo",
    "bar",
    "foo",
    "bar",
    "foo",
    "foo",
]

logger = Logger()  # Expecting [True, True, False, False, False, True]
for timstmap, message in zip(timstamps, messages):
    print(logger.shouldPrintMessage(timstmap, message))

"""
Runtime                                      
- 150 ms
- Beats 89.28%

Memory
- 22.8 MB
- Beats 51.52%
"""
