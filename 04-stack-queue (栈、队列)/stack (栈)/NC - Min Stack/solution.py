class MinStack:
    def __init__(self):
        self.stack = []
        """
        minStack 就是一列"最小值的历史快照",
        和主栈同生同灭——所以主栈退一步,最小值也精确地退回上一步。
        """
        self.minStack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        val = min(val, self.minStack[-1] if self.minStack else val)
        self.minStack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.minStack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.minStack[-1]
