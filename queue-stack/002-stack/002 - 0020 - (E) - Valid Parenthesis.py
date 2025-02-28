from collections import deque


class Solution:
    def isValid(self, s: str) -> bool:
        mapping = {"}": "{", ")": "(", "]": "["}
        stack = deque()
        for c in s:
            if c not in mapping:
                stack.append(c)
                continue
            if not stack or mapping[c] != stack[-1]:
                return False
            stack.pop()
        return len(stack) == 0


s = Solution()

# Test case 1: Expecting True
input_ = "()"


# Test case 2: Expecting True
input_ = "()[]{}"

# Test case 3: Expecting False
input_ = "(]"

# Test case 5: Expecting true
input_ = "([])"

result = s.isValid(input_)
print(result)
