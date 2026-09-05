from collections import deque


# Using value-min_value pair
class MinStack1:
    def __init__(self):
        self.stack = deque()

    def push(self, val: int) -> None:
        if len(self.stack) == 0:
            self.stack.append((val, val))
            return
        prev_min = self.stack[-1][1]
        self.stack.append((val, min(val, prev_min)))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


# Using Two Stacks
class MinStack2:
    def __init__(self) -> None:
        self.stack = []
        self.min_stack = []

    def push(self, x: int) -> None:
        self.stack.append(x)
        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)

    def pop(self) -> None:
        if self.min_stack[-1] == self.stack[-1]:
            self.min_stack.pop()
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


# minStack = MinStack()
# minStack.push(-2)
# minStack.push(0)
# minStack.push(-3)
# print(minStack.getMin())  # return -3
# minStack.pop()
# print(minStack.top())  # return 0
# print(minStack.getMin())  # return -2
