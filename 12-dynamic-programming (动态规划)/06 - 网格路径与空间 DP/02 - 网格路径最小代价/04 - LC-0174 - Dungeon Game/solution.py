"""LC-0174 - Dungeon Game

Level 1 · 06 网格路径与空间 DP —— **必须倒着推的 DP**（本专题最重要的一个反例）
题目在问：骑士从左上走到右下（只能右/下），格子的值是增减的血量。
         血量**任何时刻都必须 > 0**。求出发时所需的最少初始血量。

为什么这题必须**从右下往左上**推（这是全题的灵魂）：
  1. 如果定义 `dp[i][j] = 从起点走到 (i,j) 的最优某值`，**定义不出来** ——
     「最优」到底是「剩余血量最多」还是「所需初始血量最少」？
     **这两个目标不等价**：
     剩余血量多的路径，可能中途掉到 0 以下而非法；
     而一条中途血量低但最终剩得少的路径反而可能合法。
     **局部最优不构成全局最优 ⟹ 从前往后的 DP 不成立。**
  2. 换成 **`dp[i][j] = 从 (i,j) 出发走到终点，进入 (i,j) 之前至少需要多少血`**，
     就变成了一个**自洽**的定义：
     ```
     need = min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]
     dp[i][j] = max(1, need)          # ★ 血量必须 >= 1
     ```
     倒着推，每一步都只依赖「后面的需求」，没有歧义。
  3. **`max(1, ...)`** 是关键：如果当前格子是个大血包，算出来的 need 可能 <= 0，
     但**进入这个格子之前至少也得有 1 点血**（否则人已经死了）。

边界初始化：
```
dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])   # 终点：出来时至少剩 1 点
最后一行/最后一列只有一个方向可走
```
实现上用一个 `(m+1) × (n+1)` 的数组、哨兵填 `inf`（除了终点右边和下边填 1），
就能统一所有边界，不用写特例。

复杂度：**O(m·n)** 时间，O(n) 空间（滚动一行）。

**这道题值得专门记住的一句话**：
> 当「从起点出发的状态」定义不出自洽的最优子结构时，试试**从终点倒推**。
> 同样的思路也出现在 LC-0931、以及各种「路径上有硬约束」的题里。

边界：
  - 1×1 网格：`[[0]]` → 1；`[[-5]]` → 6；`[[100]]` → 1
  - 全是正数 → 1
  - 全是负数 → 需要很多血
  - 单行 / 单列
"""

from typing import List


##################################################################################################
##### ! Solution 1: 从右下往左上倒推 + 哨兵消除边界（滚动一行，O(n) 空间）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(n)
##### ! 适用：路径上有「任意时刻都必须满足」的硬约束时，正推定义不出来 ⟹ 倒推
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        m, n = len(dungeon), len(dungeon[0])
        INF = float("inf")
        # ! dp[j] = 从 (i, j) 出发、进入该格之前至少需要的血量
        dp = [INF] * (n + 1)
        dp[n - 1] = 1                     # ! 终点右边的哨兵设为 1：走出终点时至少剩 1 点血
        for i in range(m - 1, -1, -1):
            nxt = [INF] * (n + 1)
            for j in range(n - 1, -1, -1):
                need = min(dp[j], nxt[j + 1]) - dungeon[i][j]
                nxt[j] = max(1, need)     # ! 进入任何格子之前至少要有 1 点血
            dp = nxt
        return dp[0]


##################################################################################################
##### ! Solution 2: 二维倒推（不压缩空间，最好读）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：第一次写这题时用这版，状态定义看得最清楚
##################################################################################################


class Solution_2:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        m, n = len(dungeon), len(dungeon[0])
        INF = float("inf")
        dp = [[INF] * (n + 1) for _ in range(m + 1)]
        dp[m][n - 1] = dp[m - 1][n] = 1   # ! 终点的两个哨兵
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                need = min(dp[i + 1][j], dp[i][j + 1]) - dungeon[i][j]
                dp[i][j] = max(1, need)
        return dp[0][0]


##################################################################################################
##### ! Solution 3: 二分答案 + 正向可行性检查（基准答案，用来对拍）
##### ! 时间复杂度: O(m·n·log(范围))   空间复杂度: O(n)
##### ! 适用：正确性参照。它也说明了为什么正推不行 —— 必须「给定初始血量再验证」
#####   才能让正向 DP 有意义（这时状态变成「剩余血量最大」，目标才唯一）
##################################################################################################


class Solution_3:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        m, n = len(dungeon), len(dungeon[0])

        def feasible(start: int) -> bool:
            NEG = float("-inf")
            # ! 给定初始血量后，目标唯一了：最大化剩余血量；中途 <= 0 就视为不可达
            best = [NEG] * n
            for i in range(m):
                cur = [NEG] * n
                for j in range(n):
                    if i == 0 and j == 0:
                        v = start + dungeon[0][0]
                    else:
                        cand = NEG
                        if i > 0:
                            cand = max(cand, best[j])
                        if j > 0:
                            cand = max(cand, cur[j - 1])
                        v = NEG if cand == NEG else cand + dungeon[i][j]
                    cur[j] = v if v > 0 else NEG      # ! 血量必须 > 0
                best = cur
            return best[n - 1] != NEG

        lo, hi = 1, sum(abs(v) for row in dungeon for v in row) + 1
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


if __name__ == "__main__":
    import random

    # ! 最后一个是官方样例 3：路径 1→-3→3→0→-3，初始 3 点血全程 > 0，所以答案是 3
    cases = [([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]], 7), ([[0]], 1),
             ([[-5]], 6), ([[100]], 1), ([[1, -3, 3], [0, -2, 0], [-3, -3, -3]], 3)]
    for d, want in cases:
        a = Solution_1().calculateMinimumHP([r[:] for r in d])
        b = Solution_2().calculateMinimumHP([r[:] for r in d])
        c = Solution_3().calculateMinimumHP([r[:] for r in d])
        assert a == b == c == want, (d, a, b, c, want)
        print(f"{d} -> {a}")

    for _ in range(500):
        m, n = random.randint(1, 4), random.randint(1, 4)
        d = [[random.randint(-6, 6) for _ in range(n)] for _ in range(m)]
        a = Solution_1().calculateMinimumHP([r[:] for r in d])
        b = Solution_2().calculateMinimumHP([r[:] for r in d])
        c = Solution_3().calculateMinimumHP([r[:] for r in d])
        assert a == b == c, (d, a, b, c)
    print("随机对拍 500 组通过 ✓（倒推 == 二维倒推 == 二分答案 + 正向验证）")
