"""LC-1986 - Minimum Number of Work Sessions to Finish the Tasks

Level 1 · 09 计数 DP 与多维状态 → Level 2 · 05 特殊输入压缩与计数 DP

题目在问：n ≤ 14 个任务，每个耗时 ≤ sessionTime ≤ 15；一个 session 最多工作 sessionTime 小时，任务不可拆。最少几个 session？
这是**装箱问题（bin packing）**的小规模版 —— NP-hard，n ≤ 14 在暗示 **2ⁿ 的状态压缩 DP**。

### 状态：dp[mask] = (完成 mask 里的任务所需的最少 session 数, 最后一个 session 已用的时间)

对比两个状态时先比 session 数，再比最后一个 session 的已用时间（越少越好）—— 用元组 `(sessions, used)` 直接 `min`。
转移：从 `mask` 加一个任务 t：
- 放得进当前 session（`used + task[t] <= sessionTime`）→ `(sessions, used + task[t])`
- 否则新开一个 → `(sessions + 1, task[t])`

**为什么「贪心地塞进当前 session，塞不下才新开」在这个状态下是对的？**
因为状态里已经记录了「最后一个 session 用了多少」，而且比较时把 used 作为第二关键字 —— 同样的 session 数、更少的 used 一定不劣。
任务加入的**顺序**由 mask 的枚举覆盖了所有可能，所以不会漏掉「先放大的再放小的」这类排列。

### 另两条路

- **枚举子集 + 可行子集 DP**（`Solution_2`）：`dp[mask] = min over 子集 sub ⊆ mask 且 sum(sub) <= T: dp[mask ^ sub] + 1`。
  O(3ⁿ) = 4.8×10⁶，也能过；它把「一个 session 装哪些」显式枚举，概念最清晰。
- **回溯 + 剪枝**（`Solution_3`）：按任务顺序放进已有 session 或新开；剪枝「相同剩余容量的 session 只试一个」。n=14 时很快，是真值基线。
"""
from functools import lru_cache
from typing import List


##################################################################################################
##### ! Solution 1: 状压 DP，状态 (session 数, 最后一个 session 已用时间)
##### ! 时间复杂度: O(2ⁿ · n)   空间复杂度: O(2ⁿ)
##### ! 适用：面试标准答案；元组比较天然实现「先少 session 再少 used」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minSessions(self, tasks: List[int], sessionTime: int) -> int:
        n = len(tasks)
        INF = (float("inf"), 0)
        dp = [INF] * (1 << n)
        dp[0] = (1, 0)                                  # ! 开着一个空 session（used = 0）
        for mask in range(1 << n):
            if dp[mask] == INF:
                continue
            sessions, used = dp[mask]
            for t in range(n):
                if mask >> t & 1:
                    continue
                nm = mask | 1 << t
                if used + tasks[t] <= sessionTime:
                    cand = (sessions, used + tasks[t])  # ! 塞进当前 session
                else:
                    cand = (sessions + 1, tasks[t])     # ! 新开一个
                if cand < dp[nm]:
                    dp[nm] = cand
        return dp[-1][0]


##################################################################################################
##### ! Solution 2: 枚举「最后一个 session 装哪个子集」的子集 DP
##### ! 时间复杂度: O(3ⁿ)   空间复杂度: O(2ⁿ)
##### ! 适用：概念最清楚：先预处理哪些子集能装进一个 session（sum <= T），dp[mask] = min(dp[mask ^ sub] + 1)。
#####         枚举 mask 的所有子 mask 用 sub = (sub - 1) & mask 技巧
##################################################################################################


class Solution_2:
    def minSessions(self, tasks: List[int], sessionTime: int) -> int:
        n = len(tasks)
        total = [0] * (1 << n)
        for mask in range(1, 1 << n):
            low = mask & -mask                          # ! 最低位
            total[mask] = total[mask ^ low] + tasks[low.bit_length() - 1]
        INF = float("inf")
        dp = [INF] * (1 << n)
        dp[0] = 0
        for mask in range(1, 1 << n):
            sub = mask
            while sub:
                if total[sub] <= sessionTime:           # ! sub 可以作为一个 session
                    dp[mask] = min(dp[mask], dp[mask ^ sub] + 1)
                sub = (sub - 1) & mask                  # ! 枚举 mask 的下一个子集
        return dp[-1]


##################################################################################################
##### ! Solution 3: 回溯 + 剪枝（真值基线）
##### ! 时间复杂度: 指数，但剪枝后 n=14 很快   空间复杂度: O(n)
##### ! 适用：面试里想不到状压时的「能过」方案；剪枝 ① 任务降序排 ② 剩余容量相同的 session 只试第一个 ③ 超过当前最优就停
##################################################################################################


class Solution_3:
    def minSessions(self, tasks: List[int], sessionTime: int) -> int:
        tasks = sorted(tasks, reverse=True)             # ! 大的先放，更早触发剪枝
        n = len(tasks)
        best = [n]
        rooms: List[int] = []                           # ! 每个 session 的剩余容量

        def bt(i: int):
            if len(rooms) >= best[0]:
                return                                  # ! 已经不可能更优
            if i == n:
                best[0] = len(rooms); return
            seen = set()
            for k in range(len(rooms)):
                if rooms[k] >= tasks[i] and rooms[k] not in seen:   # ! 相同剩余容量只试一个
                    seen.add(rooms[k])
                    rooms[k] -= tasks[i]; bt(i + 1); rooms[k] += tasks[i]
            rooms.append(sessionTime - tasks[i]); bt(i + 1); rooms.pop()   # ! 新开一个

        bt(0)
        return best[0]


if __name__ == "__main__":
    import random
    cases = [([1, 2, 3], 3, 2), ([3, 1, 3, 1, 1], 8, 2), ([1, 2, 3, 4, 5], 15, 1), ([7], 7, 1), ([2, 3, 3, 4, 4, 4, 5, 6, 7, 10], 12, 4)]   # ! 10+2, 7+5, 6+3+3, 4+4+4 恰好装满 4 个
    for tasks, T, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().minSessions(tasks, T)
            assert got == want, (cls.__name__, tasks, T, got, want)
    rng = random.Random(1986)
    for _ in range(600):
        T = rng.randint(1, 15)
        tasks = [rng.randint(1, T) for _ in range(rng.randint(1, 10))]
        outs = [cls().minSessions(tasks, T) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (tasks, T, outs)
    print("所有测试通过 ✓")
