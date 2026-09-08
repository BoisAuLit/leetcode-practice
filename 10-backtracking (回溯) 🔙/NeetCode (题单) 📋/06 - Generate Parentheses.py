"""
📌 信号→模式: n 对合法括号 → 回溯：左数 < n 可加左，右数 < 左数可加右
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
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
