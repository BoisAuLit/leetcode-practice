"""LC-1029 - Two City Scheduling

Level 1 · 03 排序贪心 —— **按「差额」排序**（本节的核心思想）
题目在问：2n 个人，每人去 A 市花 `costs[i][0]`、去 B 市花 `costs[i][1]`，
         要求**恰好 n 人去 A、n 人去 B**，求最小总花费。

决定性观察（整道题就是一行排序）：
  1. **不能按绝对花费排序**。`[10, 20]` 和 `[30, 200]` 里，
     第二个人去 A 虽然贵（30 > 10），但他去 B 更亏（200）⟹ 应该让他去 A。
  2. **要按「差额」排序**：`costs[i][0] - costs[i][1]`（去 A 比去 B 省多少）。
     差额最小（最负）的前 n 个人去 A，其余去 B。
  3. **为什么正确（交换论证）**：
     设最优解里有两个人 i、j，`diff[i] < diff[j]`，但 i 去了 B、j 去了 A。
     把两人互换：总花费的变化是
     `(a_i + b_j) - (a_j + b_i) = (a_i - b_i) - (a_j - b_j) = diff[i] - diff[j] < 0`
     ⟹ **互换后更便宜**，矛盾。所以最优解一定是按 diff 排序取前 n 个。∎

```python
costs.sort(key=lambda c: c[0] - c[1])
return sum(c[0] for c in costs[:n]) + sum(c[1] for c in costs[n:])
```

> **「有两个选项、要恰好各选一半」⟹ 按两个选项的差额排序。**
> 这个模式在很多「二选一 + 配额」的题里出现。

**另一个等价视角**：先假设所有人都去 B（基准花费 `sum(b)`），
然后选 n 个人「改去 A」，每人的额外代价是 `a[i] - b[i]` ⟹ 选最小的 n 个。
这个视角和上面的排序完全等价，但更容易推广到「配额不是一半」的情形。

复杂度：**O(n log n)** 时间（排序主导），O(1) 额外空间。

边界：
  - 所有人去 A 都更便宜（但必须有一半去 B）
  - 差额全部相同
  - n = 1（2 个人）
  - 花费相等
"""

from typing import List


##################################################################################################
##### ! Solution 1: 按 (去 A 的花费 − 去 B 的花费) 排序，前 n 个去 A
##### ! 时间复杂度: O(n log n)   空间复杂度: O(1) 额外
##### ! 适用：「二选一 + 恰好各占一半/固定配额」⟹ 按差额排序
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def twoCitySchedCost(self, costs: List[List[int]]) -> int:
        costs = sorted(costs, key=lambda c: c[0] - c[1])   # ! 差额升序：越该去 A 的排越前
        n = len(costs) // 2
        return sum(c[0] for c in costs[:n]) + sum(c[1] for c in costs[n:])


##################################################################################################
##### ! Solution 2: 「先全去 B，再挑 n 个改去 A」的等价视角
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：配额不是一半时更容易推广；也更能看清「差额」的含义就是「改主意的代价」
##################################################################################################


class Solution_2:
    def twoCitySchedCost(self, costs: List[List[int]]) -> int:
        n = len(costs) // 2
        base = sum(c[1] for c in costs)                    # ! 先假设全去 B
        extra = sorted(c[0] - c[1] for c in costs)         # ! 改去 A 的额外代价
        return base + sum(extra[:n])                       # ! 挑最便宜的 n 个改


##################################################################################################
##### ! Solution 3: DP（基准答案，用来对拍；不依赖贪心的正确性）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：正确性参照 —— dp[i][a] = 前 i 个人里有 a 个去 A 的最小花费
##################################################################################################


class Solution_3:
    def twoCitySchedCost(self, costs: List[List[int]]) -> int:
        total = len(costs)
        n = total // 2
        INF = float("inf")
        dp = [INF] * (n + 1)
        dp[0] = 0
        for i, (a, b) in enumerate(costs):
            nxt = [INF] * (n + 1)
            for ga in range(min(i + 1, n) + 1):
                if dp[ga] == INF:
                    continue
                if ga + 1 <= n:                            # ! 这个人去 A
                    nxt[ga + 1] = min(nxt[ga + 1], dp[ga] + a)
                if (i - ga) + 1 <= n:                      # ! 这个人去 B
                    nxt[ga] = min(nxt[ga], dp[ga] + b)
            dp = nxt
        return int(dp[n])


if __name__ == "__main__":
    import random

    cases = [([[10, 20], [30, 200], [400, 50], [30, 20]], 110),
             ([[259, 770], [448, 54], [926, 667], [184, 139], [840, 118], [577, 469]], 1859),
             ([[10, 20], [20, 10]], 20),
             ([[5, 5], [5, 5]], 10)]
    for costs, want in cases:
        a = Solution_1().twoCitySchedCost([c[:] for c in costs])
        b = Solution_2().twoCitySchedCost([c[:] for c in costs])
        c = Solution_3().twoCitySchedCost([x[:] for x in costs])
        assert a == b == c == want, (costs, a, b, c, want)
        print(f"{costs} -> {a}")

    for _ in range(800):
        n = random.randint(1, 5)
        costs = [[random.randint(0, 50), random.randint(0, 50)] for _ in range(2 * n)]
        a = Solution_1().twoCitySchedCost([c[:] for c in costs])
        b = Solution_2().twoCitySchedCost([c[:] for c in costs])
        c = Solution_3().twoCitySchedCost([x[:] for x in costs])
        assert a == b == c, (costs, a, b, c)
    print("随机对拍 800 组通过 ✓（差额排序 == 改主意视角 == DP）")
