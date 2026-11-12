"""LC-1854 - Maximum Population Year

Level 1 · 04 重叠计数、扫描线与资源分配 → Level 2 · 02 差分事件与容量约束

题目在问：每个人 `[birth, death]`，活着的年份是 `[birth, death − 1]`（出生年算、死亡年不算）。求人口最多的**最早**年份。
Easy，但它是差分数组最干净的教学题：值域只有 1950..2050（101 个点）。

### 差分三步

    diff[birth] += 1        diff[death] -= 1        # ! 死亡年不算活着 → 半开区间 [birth, death)，减在 death 上
    前缀和得到每年人口
    取最大值出现的第一个年份

### 和 LC-1094 / LC-1109 / LC-2251 的关系

四道题的差别只有：
| 题 | 区间 | 减在哪 | 要什么 |
|---|---|---|---|
| 1854 | `[birth, death)` | `death` | argmax（最早） |
| 1094 Car Pooling | `[from, to)` | `to` | 最大值是否 ≤ capacity |
| 1109 | `[first, last]` 闭 | `last + 1` | 整条前缀和 |
| 2251 | `[start, end]` 闭，值域 10⁹ | `end + 1`，要坐标压缩或二分 | 每个查询点的值 |

### 为什么本题可以用差分而 2251 不能

差分数组长度 = 值域大小。101 可以；10⁹ 不行 —— 那时要么坐标压缩、要么换成「两次二分」。
`Solution_2` 的扫描线对值域不敏感，是面试里应对「年份范围变成任意整数怎么办」的答案。
"""
from typing import List


##################################################################################################
##### ! Solution 1: 差分数组（值域 1950..2050）
##### ! 时间复杂度: O(n + 101)   空间复杂度: O(101)
##### ! 适用：面试标准答案。偏移 1950 做下标；death 处 −1（半开区间）
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maximumPopulation(self, logs: List[List[int]]) -> int:
        BASE, SIZE = 1950, 102                          # ! 2050 - 1950 + 2，留一个位置给 death=2050 的 -1
        diff = [0] * SIZE
        for birth, death in logs:
            diff[birth - BASE] += 1
            diff[death - BASE] -= 1                     # ! 死亡那年不算活着
        best_year = best = cur = 0
        for i in range(SIZE):
            cur += diff[i]
            if cur > best:                              # ! 严格大于 → 取最早的
                best, best_year = cur, i + BASE
        return best_year


##################################################################################################
##### ! Solution 2: 事件排序扫描线（不依赖值域）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：年份范围任意时。同一年先处理 −1 再处理 +1（因为死亡年不算活着，先减后加恰好对应半开区间）
##################################################################################################


class Solution_2:
    def maximumPopulation(self, logs: List[List[int]]) -> int:
        events = sorted([(b, 1) for b, _ in logs] + [(d, -1) for _, d in logs])   # ! 同年 (y,-1) 排在 (y,1) 前
        best_year = best = cur = 0
        for year, delta in events:
            cur += delta
            if cur > best:
                best, best_year = cur, year
        return best_year


##################################################################################################
##### ! Solution 3: 暴力 —— 对每个候选年份数人（真值基线）
##### ! 时间复杂度: O(n · 101)   空间复杂度: O(1)
##### ! 适用：只用来对拍；候选年份只需是某个 birth（人口只在出生年可能变多）
##################################################################################################


class Solution_3:
    def maximumPopulation(self, logs: List[List[int]]) -> int:
        best_year = best = 0
        for year in range(1950, 2051):
            cnt = sum(1 for b, d in logs if b <= year < d)
            if cnt > best:
                best, best_year = cnt, year
        return best_year


if __name__ == "__main__":
    import random
    cases = [([[1993, 1999], [2000, 2010]], 1993), ([[1950, 1961], [1960, 1971], [1970, 1981]], 1960),
             ([[2000, 2050]], 2000), ([[1950, 1951], [1950, 1951]], 1950)]
    for logs, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().maximumPopulation(logs)
            assert got == want, (cls.__name__, logs, got, want)
    rng = random.Random(1854)
    for _ in range(3000):
        logs = []
        for _ in range(rng.randint(1, 10)):
            b = rng.randint(1950, 2049); logs.append([b, rng.randint(b + 1, 2050)])
        outs = [cls().maximumPopulation(logs) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (logs, outs)
    print("所有测试通过 ✓（样例 + 3000 随机对拍）")
