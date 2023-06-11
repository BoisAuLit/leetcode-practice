from queue import LifoQueue

"""
Time complexity: O(n)
Space complexity: O(n)
"""


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


s = Solution()
# input_ = "()[]{}" # Expecting True
# input_ = "(((((]]]]]" # Expecting False
input_ = "{[{{()}}]}[({})]" # Expecting True
result = s.isValid(input_)
print(result)

"""
Runtime
- 56 ms
- Beats 7.91%

Memory
- 16.5 MB
- Beats 7.81%
"""
