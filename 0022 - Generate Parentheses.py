from typing import List

"""
Time complexity: O(2ᴺ)
Space complexity: O(N)
"""


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []

        def backtrack(array, left, right):
            if right < left or left < 0 or right < 0:
                return
            if left == 0 and right == 0:
                result.append("".join(array))
                return
            array.append("(")
            backtrack(array, left - 1, right)
            array.pop()
            array.append(")")
            backtrack(array, left, right - 1)
            array.pop()

        backtrack(["("], n - 1, n)
        return result


s = Solution()
input_ = 1
result = s.generateParenthesis(input_)
print(result)

"""

"""
