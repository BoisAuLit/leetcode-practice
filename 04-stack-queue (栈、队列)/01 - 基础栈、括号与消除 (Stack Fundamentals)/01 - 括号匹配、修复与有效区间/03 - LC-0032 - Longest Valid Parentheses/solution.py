# Python Solution
def longestValidParentheses(s):
    best = 0
    wall = -1            # 最近的墙:最近一个多余的 ")" 的位置,初始是开头左边
    stack = []           # 还没配对的 "(" 的下标

    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)                       # 等待配对
        elif stack:                               # 有 "(" 可以配
            stack.pop()                           # 配上了
            left = stack[-1] if stack else wall   # 最近的挡板:剩下的 "(" 或者墙
            best = max(best, i - left)
        else:                                     # 没有 "(" 可配
            wall = i                              # 这个 ")" 多余,它成为新的墙

    return best


##################################################################################################
##### ! Solution DP: 来自 12-dynamic-programming 的另一份实现（同一道题的 DP 视角）
##### ! 这道题在仓库里曾有两份实体目录（本专题的栈版 / 12-DP 的 DP 版）。
#####   本次统一成**一份**：本目录是正式位置（它有两张讲解图和 1 条复习记录），
#####   12-DP 的那份已归档为「变体 · …」（不再匹配题目前缀，不参与复习队列），文件一个没删。
##### ! 栈版 vs DP 版：
#####   - **栈版**：栈底垫一个 -1 当哨兵，弹栈后若栈空就把当前下标压进去当新哨兵，
#####     用「当前下标 − 栈顶」算长度。O(n) 时间 O(n) 空间。
#####   - **DP 版**：dp[i] = 以 i 结尾的最长有效长度，分 s[i]==')' 且 s[i-1]=='(' 和
#####     s[i-1]==')' 两种情况。O(n) 时间 O(n) 空间。
#####   - 还有一种 **O(1) 空间**的两趟计数法（左右各扫一遍数左右括号）。
##### ! 下面把 DP 版的实现原样搬过来（类名加 _DP 后缀），方便对照。
##################################################################################################


class Solution_DP:
    def longestValidParentheses(self, s: str) -> int:
        maxans = 0
        dp = [0] * len(s)
        for i in range(1, len(s)):
            if s[i] == ")":
                if s[i - 1] == "(":
                    dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
                elif i - dp[i - 1] > 0 and s[i - dp[i - 1] - 1] == "(":
                    dp[i] = (
                        dp[i - 1]
                        + (dp[i - dp[i - 1] - 2] if i - dp[i - 1] >= 2 else 0)
                        + 2
                    )
                maxans = max(maxans, dp[i])
        return maxans
