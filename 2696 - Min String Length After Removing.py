from collections import deque

class Solution:
    def minLength(self, s: str) -> int:
        stack = deque()
        for c in s:
            if not stack:
                stack.append(c)
                continue
            if (stack[-1] + c) in ["AB", "CD"]:
                stack.pop()
            else:
                stack.append(c)
        return len(stack)
s = Solution()

# Expecting 2
input_ = "ABFCACDB"
result = s.minLength(input_)
print(result)
