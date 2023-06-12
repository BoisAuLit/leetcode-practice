from collections import deque

"""
Time complexity: O(n)
Space complexity: O(n)
"""


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
input_ = "()[]{}" # Expecting True
# input_ = "(((((]]]]]" # Expecting False
# input_ = "{[{{()}}]}[({})]" # Expecting True
result = s.isValid(input_)
print(result)

"""
Runtime
- 43 ms
- Beats 56.69%

Memory
- 16.3 MB
- Beats 61.8%
"""
