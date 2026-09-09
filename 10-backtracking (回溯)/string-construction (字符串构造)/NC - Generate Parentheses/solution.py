from typing import List


"""
You can add '(' only if you still have openings left (open < n).
You can add ')' only if it won't break validity (close < open).
A string is complete and valid only when open == close == n.

open - number of '(' used.
close - number of ')' used.
"""


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        stack = []
        res = []

        def backtrack(openN, closedN):
            if openN == closedN == n:
                res.append("".join(stack))
                return

            if openN < n:
                stack.append("(")
                backtrack(openN + 1, closedN)
                stack.pop()
            if closedN < openN:
                stack.append(")")
                backtrack(openN, closedN + 1)
                stack.pop()

        backtrack(0, 0)
        return res


s = Solution()
input_ = 3
result = s.generateParenthesis(3)
print(result)
