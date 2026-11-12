from functools import lru_cache


class Solution:
    # ============================================================
    # 解法一：记忆化递归（主力版本）
    # ------------------------------------------------------------
    # dp(i, j) = 把 word1[i:] 改成 word2[j:] 的最少操作数。
    # 视角：word1[0..i-1] 和 word2[0..j-1] 已处理完、彻底退场，
    #       每个状态只决策"前线"两个字符 word1[i] 和 word2[j] 的命运。
    #
    # 为什么 8 种想象中的操作只剩 3 种？
    #   ① 题目只允许操作 word1，针对 word2 的 4 种被规则排除
    #      （且它们与 word1 操作对偶等价：往 word1 插 ≡ 从 word2 删，
    #        这也是编辑距离对称 dist(a,b)==dist(b,a) 的原因）。
    #   ② "在 i 之后插" / 一切深处操作被规范顺序推迟：
    #      任何最优方案都可重排成"从左到右、只在前线操作"，
    #      等那个位置成为前线时，它所在的状态自然会枚举到。
    #      （与 Coin Change II 的"规范顺序去重"是同一思想）
    #
    # 插入 = 在前线（i 之前）凭空造一个等于 word2[j] 的字符，
    #        出生即配对即退场，所以 word1 的 i 不动、只有 j 前进。
    #        插别的字符纯亏一步，不用考虑。
    # ============================================================
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)

        @lru_cache(maxsize=None)
        def dp(i: int, j: int) -> int:
            if i == m:                      # word1 用完 → 剩下的 word2[j:] 只能逐个插入
                return n - j
            if j == n:                      # word2 用完 → 剩下的 word1[i:] 只能逐个删除
                return m - i
            if word1[i] == word2[j]:        # 前线相等 → 免费配对，双双退场
                return dp(i + 1, j + 1)
            return 1 + min(
                dp(i, j + 1),               # 插入：造一个 word2[j] 配对 → 只消耗 j
                dp(i + 1, j),               # 删除：word1[i] 谁也不配，扔掉 → 只消耗 i
                dp(i + 1, j + 1),           # 替换：word1[i] 整容成 word2[j] → 双双消耗
            )

        return dp(0, 0)

    # ============================================================
    # 解法二：二维迭代（由解法一按四步配方机械翻译）
    # ------------------------------------------------------------
    # ① cache 键 (i, j) → 数组 dp[(m+1) x (n+1)]
    # ② base case → 边界初始化：dp[m][j] = n - j；dp[i][n] = m - i
    # ③ 递归调用 → 数组读取；return → 写入 dp[i][j]
    # ④ 循环方向 = "被读的先算"：读的是 i+1 / j+1 → 两层都倒序
    # ============================================================
    def minDistance_iter(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for j in range(n + 1):              # 底边：word1 用完，只剩插入
            dp[m][j] = n - j
        for i in range(m + 1):              # 右边：word2 用完，只剩删除
            dp[i][n] = m - i

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if word1[i] == word2[j]:
                    dp[i][j] = dp[i + 1][j + 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i][j + 1],       # 插入
                        dp[i + 1][j],       # 删除
                        dp[i + 1][j + 1],   # 替换
                    )
        return dp[0][0]


if __name__ == "__main__":
    s = Solution()
    for f in (s.minDistance, s.minDistance_iter):
        assert f("", "abc") == 3            # 守卫：空 word1 → 全靠插入
        assert f("abc", "") == 3            # 守卫：空 word2 → 全靠删除
        assert f("horse", "ros") == 3       # 守卫：换 h→r、删 r、删 e
        assert f("intention", "execution") == 5
        assert f("a", "a") == 0
    print("全部守卫通过 ✅")
