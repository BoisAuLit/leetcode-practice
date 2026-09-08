"""
📌 信号→模式: 带 . 和 * 的模式匹配 → 双序列 DP：星号 = 前线二选一（不吃跳 j+2 / 吃一个 i+1 且 j 原地踏步）
📅 首次: 2026-09-06 | 卡点: M1 第三次复发——普通字符分支漏 i<m 守卫，j==n-1 特判只挡住一条边（M9 影子） | 守卫: ("a","abc")->False, ("aab","c*a*b")->True
🔁 复习: 未排期
"""
from functools import lru_cache


class Solution:
    # ============================================================
    # 验户口：双序列 DP（i、j 两个指针），72/97/115/1143 的亲兄弟。
    # 新花样只有一个：星号允许 j 原地踏步（dp(i+1, j)）。
    #
    # dp(i, j) = s[i:] 能否被 p[j:] 完全匹配。
    #
    # 星号的前线思想（与 Edit Distance 的"深处操作推迟"同源）：
    #   x* 面前只问一个问题——它吃不吃当前这一个 s[i]？
    #     · 不吃：跳过整个 x*        → dp(i, j+2)
    #     · 吃一个：i 前进，j 不动   → dp(i+1, j)（x* 留在原地，下个状态再问一次）
    #   "吃 k 个"不用现在决定，连做 k 次"吃一个"就是吃 k 个。
    #   每个状态 2 个分支，O(m*n)；逐个数枚举则是 O(m^2*n)。
    #
    # 疤痕（M1 第三次复发：97 漏 break、115 切片比较、本题漏守卫）：
    #   我的原版在普通字符分支直接访问 s[i]，没有 i<m 担保；
    #   j==n-1 的手写特判恰好只在那一条边上挡住了越界，
    #   让人误以为全体安全 → s="a", p="abc" 直接 IndexError 崩溃，
    #   而 NeetCode 测试没有覆盖这个形状（测试通过 ≠ 正确，第三次！）。
    #   教训：每个 s[i]/p[j] 的出现点，守卫必须写在同一个表达式里
    #   （first = i < m and ...），而不是寄希望于某个上游特判替你挡。
    # ============================================================

    # ------------------------------------------------------------
    # 解法一：记忆化递归（主力版本）
    # ------------------------------------------------------------
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)

        @lru_cache(maxsize=None)
        def dp(i: int, j: int) -> bool:
            if j == n:                       # 模式用完：s 也必须恰好用完
                return i == m

            # 唯一的守卫：i < m 写在 and 左边，担保右边的 s[i] 永远安全
            first = i < m and (p[j] == "." or s[i] == p[j])

            if j + 1 < n and p[j + 1] == "*":
                return (
                    dp(i, j + 2)                  # * 不吃了：跳过整个 x*
                    or (first and dp(i + 1, j))   # * 再吃一个：i 前进，j 原地
                )
            return first and dp(i + 1, j + 1)     # 普通字符：配上则双双前进

        return dp(0, 0)

    # ------------------------------------------------------------
    # 解法二：二维迭代（由解法一按四步配方机械翻译）
    #   ① cache 键 (i, j) → (m+1) x (n+1) 数组
    #   ② base case j==n → i==m：dp[m][n]=True，右列其余为 False
    #      （数组初始化为全 False，所以只需点亮 dp[m][n]）
    #   ③ dp(i,j+2)→dp[i][j+2]；dp(i+1,j)→dp[i+1][j]；
    #      dp(i+1,j+1)→dp[i+1][j+1]；return → 写 dp[i][j]
    #   ④ 循环方向 = "被读的先算"，逐维度判断：
    #      · i 这一维：读 i+1（更大的 i）→ i 倒序
    #      · j 这一维：读 j+2（更大的 j）；dp[i+1][j] 是同列下面的格子，
    #        已由 i 倒序保证先算 → j 倒序
    #      （画表格看：每个格子抄"右边两格"和"正下方"，
    #        所以从右下角往左上角填，和 72/97/115 同款）
    # ------------------------------------------------------------
    def isMatch_iter(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[m][n] = True                      # 双双用完 → 匹配成功

        for i in range(m, -1, -1):           # i 倒序（含 i==m 这一行！它不是全 False）
            for j in range(n - 1, -1, -1):   # j 倒序
                first = i < m and (p[j] == "." or s[i] == p[j])
                if j + 1 < n and p[j + 1] == "*":
                    dp[i][j] = dp[i][j + 2] or (first and dp[i + 1][j])
                else:
                    dp[i][j] = first and dp[i + 1][j + 1]

        return dp[0][0]
        # 注意 i==m 这一行也要正常计算（不能当全 False 的边界甩掉）：
        # s 用完时 p 剩 "a*b*" 仍可匹配成功（星号全取 0 次）。
        # first 在 i==m 时自然为 False，通用公式直接给出正确答案——
        # 这正是"统一守卫优于手写特判"的又一例证。


if __name__ == "__main__":
    sol = Solution()
    for f in (sol.isMatch, sol.isMatch_iter):
        assert f("a", "abc") is False        # 守卫：疤痕——原版漏 i<m 守卫在此崩溃
        assert f("aab", "c*a*b") is True     # 守卫：* 匹配 0 次（c 出现 0 次）
        assert f("mississippi", "mis*is*p*.") is False
        assert f("aa", ".b") is False        # 题面样例
        assert f("nnn", "n*") is True
        assert f("xyz", ".*z") is True
        assert f("", "a*b*") is True         # s 为空 + 星号全取 0
        assert f("abc", "") is False
        assert f("", "") is True
    print("全部守卫通过 ✅")
