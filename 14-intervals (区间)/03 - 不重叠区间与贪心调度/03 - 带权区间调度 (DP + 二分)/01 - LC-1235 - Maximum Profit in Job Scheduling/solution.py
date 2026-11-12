"""LC-1235 - Maximum Profit in Job Scheduling

Level 1 · 03 不重叠区间与贪心调度 → Level 2 · 03 带权区间调度 (DP + 二分)

题目在问：每个任务 `[start, end, profit]`，选一组**互不重叠**（端点相接允许）的任务，使利润和最大。

### 为什么贪心（LC-0435 的套路）在这里失效

LC-0435 / LC-0646 求「最多选几个」时按结束时间贪心是对的 —— 每个任务权重相同。
本题带权：一个长任务的利润可能超过它挤掉的三个短任务之和，贪心没有办法比较。这是**带权区间调度**（Weighted Interval Scheduling），教科书 DP。

### DP：按结束时间排序，dp[i] = 前 i 个任务的最优利润

    排序后 jobs[0..n-1] 按 end 升序
    dp[i] = max( dp[i-1],                                   # ! 不选第 i 个
                 profit[i] + dp[j] )                        # ! 选第 i 个；j = 最后一个 end <= start[i] 的任务
    j 用二分找：bisect_right(ends, start[i]) 给出「有多少个任务 end <= start[i]」，正好是 dp 的下标

### 两个细节

1. `bisect_right` 而不是 `bisect_left`：`end == start` 允许相接，所以 end ≤ start 的都算 → right。
2. 把 `dp` 做成长度 n+1 的数组、`dp[0] = 0`，二分返回的个数 k 直接当下标 `dp[k]`，不用 −1。

### 另一个方向：按 start 排 + 「从 i 往后的最优」

`Solution_2` 按 start 排序，`dp[i]` = 从第 i 个任务开始（只看 i..n−1）的最优；转移 `dp[i] = max(dp[i+1], profit + dp[next])`，
`next = bisect_left(starts, end[i])`。两者对称，面试里任选一个，但要能说出两者的二分方向相反。
"""
from bisect import bisect_left, bisect_right
from typing import List


##################################################################################################
##### ! Solution 1: 按 end 排序 + dp[i] = max(不选, 选 + dp[二分找到的前驱]) 
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：面试标准答案。ends 单独抽出来给 bisect；dp 多留一个 0 位
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = sorted(zip(endTime, startTime, profit))  # ! 按 end 排
        ends = [e for e, _, _ in jobs]
        dp = [0] * (len(jobs) + 1)                      # ! dp[k] = 前 k 个任务的最优
        for i, (e, s, p) in enumerate(jobs):
            k = bisect_right(ends, s)                   # ! 有多少个任务 end <= s（允许相接）
            dp[i + 1] = max(dp[i], dp[k] + p)
        return dp[-1]


##################################################################################################
##### ! Solution 2: 按 start 排序 + 后缀 dp（dp[i] = 从 i 开始的最优）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：对称写法；next = bisect_left(starts, end_i) 是第一个 start >= end_i 的任务。
#####         记忆化递归版就是这个方向（从 0 往后选），所以更接近「回溯 + 记忆化」的思路
##################################################################################################


class Solution_2:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = sorted(zip(startTime, endTime, profit))
        starts = [s for s, _, _ in jobs]
        n = len(jobs)
        dp = [0] * (n + 1)                              # ! dp[n] = 0：没有任务可选
        for i in range(n - 1, -1, -1):
            s, e, p = jobs[i]
            nxt = bisect_left(starts, e)                # ! 第一个 start >= e 的任务
            dp[i] = max(dp[i + 1], p + dp[nxt])
        return dp[0]


##################################################################################################
##### ! Solution 3: 按 end 排序 + 堆维护「已结束任务的最优 dp」（不用二分的 O(n log n)）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：另一条思路：扫描时把 (end, dp_at_end) 放进最小堆；处理 start = s 的任务前，
#####         把所有 end <= s 的弹出并更新 best = max(best, 它们的 dp)；当前任务的 dp = best + p。
#####         这是 LC-0253 式「按时间推进、堆里放已完成事件」的变体
##################################################################################################


class Solution_3:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        import heapq
        jobs = sorted(zip(startTime, endTime, profit))  # ! 按 start 排
        heap: List[tuple] = []                          # ! (end, 选到该任务为止的最优利润)
        best = 0                                        # ! 所有 end <= 当前 start 的任务里的最优
        for s, e, p in jobs:
            while heap and heap[0][0] <= s:             # ! 这些任务在 s 之前已经结束，可以接在前面
                best = max(best, heapq.heappop(heap)[1])
            heapq.heappush(heap, (e, best + p))
        return max(best, max(v for _, v in heap))


def _brute(st, et, pr):
    n = len(st); best = 0
    for mask in range(1 << n):
        chosen = [(st[i], et[i], pr[i]) for i in range(n) if mask >> i & 1]
        chosen.sort()
        if all(chosen[k][1] <= chosen[k + 1][0] for k in range(len(chosen) - 1)):
            best = max(best, sum(p for _, _, p in chosen))
    return best


if __name__ == "__main__":
    import random
    cases = [
        ([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70], 120),
        ([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60], 150),
        ([1, 1, 1], [2, 3, 4], [5, 6, 4], 6),
        ([1], [2], [7], 7),
    ]
    for st, et, pr, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().jobScheduling(st, et, pr)
            assert got == want, (cls.__name__, st, et, pr, got, want)
    rng = random.Random(1235)
    for _ in range(1500):
        n = rng.randint(1, 9)
        st = [rng.randint(0, 10) for _ in range(n)]
        et = [s + rng.randint(1, 6) for s in st]
        pr = [rng.randint(1, 20) for _ in range(n)]
        want = _brute(st, et, pr)
        for cls in (Solution_1, Solution_2, Solution_3):
            assert cls().jobScheduling(st, et, pr) == want, (cls.__name__, st, et, pr)
    print("所有测试通过 ✓（样例 + 1500 随机对拍）")
