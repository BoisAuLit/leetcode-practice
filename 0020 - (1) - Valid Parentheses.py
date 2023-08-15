from queue import LifoQueue
from collections import deque

"""
Time complexity: O(n)
Space complexity: O(n)
"""

# Solution 1 --> queue.LifoQueue
class Solution:
    def isValid(self, s: str) -> bool:
        stack = LifoQueue()
        closing = {"]": "[", ")": "(", "}": "{"}
        for c in s:
            if c not in closing:
                stack.put(c)
            else:
                if stack.empty() or closing[c] != stack.get():
                    return False
        return stack.empty()

# Solution 2 --> Builtin list
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        closing = {"]": "[", ")": "(", "}": "{"}
        for c in s:
            if c not in closing:
                stack.append(c)
            else:
                if not bool(stack) or closing[c] != stack.pop():
                    return False
        return not bool(stack)


# Solution 3 --> collections.deque
class Solution:
    def isValid(self, s: str) -> bool:
        stack = deque()
        closing = {"]": "[", ")": "(", "}": "{"}
        for c in s:
            if c not in closing:
                stack.append(c)
            else:
                if not bool(stack) or closing[c] != stack.pop():
                    return False
        return not bool(stack)

s = Solution()
# input_ = "()[]{}" # Expecting True
# input_ = "(((((]]]]]" # Expecting False
input_ = "{[{{()}}]}[({})]" # Expecting True
result = s.isValid(input_)
print(result)
