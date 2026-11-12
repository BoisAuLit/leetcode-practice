"""LC-0120 - Triangle

Level 1 · 06 网格路径与空间 DP —— **自底向上消除边界特判**
题目在问：三角形数组，每步只能走到下一行的 `i` 或 `i+1`，求从顶到底的最小路径和。
         进阶要求：**O(n) 额外空间**。

决定性观察：
  1. **自顶向下**写的话，每一行的**首尾两个位置**都是特例
     （第一个只能从上一行的第一个来，最后一个只能从上一行的最后一个来）——
     要写三个分支。
  2. **自底向上**写的话，`dp[i] = min(dp[i], dp[i+1]) + row[i]`，
     **每个位置都有两个合法的来源，没有任何特例**。
     这就是本题最值得记的一点：**换个方向推，边界特判就消失了。**
  3. 自底向上还天然满足 O(n) 空间：
     用一个长度 n 的数组，从最后一行往上**原地覆盖**即可。
     `dp[i]` 读的是 `dp[i]` 和 `dp[i+1]`（都是下一行的值），
     而写的是 `dp[i]` —— 从左往右遍历时，`dp[i+1]` 还没被这一轮覆盖，所以安全。

```python
dp = triangle[-1][:]                       # 最后一行就是初始状态
for row in reversed(triangle[:-1]):
    for i in range(len(row)):
        dp[i] = row[i] + min(dp[i], dp[i + 1])
return dp[0]
```

复杂度：**O(n²)** 时间（n 行，第 i 行 i+1 个元素），**O(n)** 空间。
      不做空间优化的二维版是 O(n²) 空间。

和 LC-0064 Minimum Path Sum 的区别：
      64 是矩形网格、只能右/下；本题是三角形、只能下/右下。
      **但「自底向上消除边界」这个技巧在 64 上也成立**（从右下角往左上推）。

边界：
  - 单行 `[[-10]]` → -10
  - 含负数（所以**不能贪心每步选小的**，必须 DP）
  - 全正数
  - 两行
"""

from typing import List


##################################################################################################
##### ! Solution 1: 自底向上 + 原地滚动数组（O(n) 空间，无边界特判）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：所有「下一步只能到相邻两个位置」的路径 DP；换方向推就能消掉边界特判
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        dp = triangle[-1][:]                    # ! 从最后一行开始
        for row in reversed(triangle[:-1]):
            for i in range(len(row)):
                # ! 每个位置都有两个合法来源，没有任何特例
                dp[i] = row[i] + min(dp[i], dp[i + 1])
        return dp[0]


##################################################################################################
##### ! Solution 2: 自顶向下（需要处理首尾两个特例，用来对照「为什么自底向上更好」）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：说明方向选择的影响；注意首尾要单独写，三个分支
##################################################################################################


class Solution_2:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        n = len(triangle)
        dp = [triangle[0][0]]
        for i in range(1, n):
            row = triangle[i]
            nxt = [0] * (i + 1)
            for j in range(i + 1):
                if j == 0:
                    nxt[j] = dp[0] + row[j]              # ! 特例：只能从上一行第一个来
                elif j == i:
                    nxt[j] = dp[i - 1] + row[j]          # ! 特例：只能从上一行最后一个来
                else:
                    nxt[j] = min(dp[j - 1], dp[j]) + row[j]
            dp = nxt
        return min(dp)


##################################################################################################
##### ! Solution 3: 记忆化搜索（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)
##### ! 适用：正确性参照；也最直白地表达状态定义
##################################################################################################


class Solution_3:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        from functools import lru_cache
        n = len(triangle)

        @lru_cache(maxsize=None)
        def dfs(i: int, j: int) -> int:
            if i == n - 1:
                return triangle[i][j]
            return triangle[i][j] + min(dfs(i + 1, j), dfs(i + 1, j + 1))

        res = dfs(0, 0)
        dfs.cache_clear()
        return res


if __name__ == "__main__":
    import random

    cases = [([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]], 11), ([[-10]], -10),
             ([[1], [2, 3]], 3), ([[-1], [2, 3], [1, -1, -3]], -1)]
    for tri, want in cases:
        a = Solution_1().minimumTotal([r[:] for r in tri])
        b = Solution_2().minimumTotal([r[:] for r in tri])
        c = Solution_3().minimumTotal([tuple(r) for r in tri] and [r[:] for r in tri])
        assert a == b == c == want, (tri, a, b, c, want)
        print(f"{tri} -> {a}")

    for _ in range(600):
        n = random.randint(1, 7)
        tri = [[random.randint(-9, 9) for _ in range(i + 1)] for i in range(n)]
        a = Solution_1().minimumTotal([r[:] for r in tri])
        b = Solution_2().minimumTotal([r[:] for r in tri])
        c = Solution_3().minimumTotal([r[:] for r in tri])
        assert a == b == c, (tri, a, b, c)
    print("随机对拍 600 组通过 ✓（自底向上 == 自顶向下 == 记忆化，含负数）")
