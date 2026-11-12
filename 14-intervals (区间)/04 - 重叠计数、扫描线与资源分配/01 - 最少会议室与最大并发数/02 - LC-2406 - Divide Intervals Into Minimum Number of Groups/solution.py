"""LC-2406 - Divide Intervals Into Minimum Number of Groups

Level 1 · 04 重叠计数、扫描线与资源分配 —— **闭区间版的 Meeting Rooms II**
题目在问：把 `intervals`（**闭区间** `[left, right]`）分组，同组内任意两个区间
         **不能相交**，问最少分几组。

决定性观察（一句话）：
  **答案 = 最大「同时刻被覆盖」的区间数**（最大重叠数 / 图论里的最大团）。
  - 下界：若某一时刻 `t` 有 `k` 个区间同时覆盖它，这 `k` 个区间两两相交，
    必须分到 `k` 个不同的组 ⟹ 至少要 `k` 组。
  - 上界：按 start 排序 + 贪心（把区间塞进任意一个「右端点已经过去」的组）
    恰好用掉 `max_overlap` 组。两边一夹 ⟹ 答案就是最大重叠数。∎

### ⚠️ 本题与 LC-0253 Meeting Rooms II 唯一的区别：端点语义

| | LC-0253 Meeting Rooms II | LC-2406 本题 |
|---|---|---|
| 区间 | **半开** `[start, end)` | **闭** `[left, right]` |
| `[1,2]` 和 `[2,3]` | **不冲突**，可以复用同一间会议室 | **冲突**（都含 2），必须分开 |
| 复用条件 | `start >= 前一个 end` | `left > 前一个 right`，即 `left >= right + 1` |
| 差分数组 | `diff[start] += 1; diff[end] -= 1` | `diff[left] += 1; diff[right + 1] -= 1` |
| 堆的弹出条件 | `heap[0] <= start` | `heap[0] < left` |

> **这是本题唯一的坑。** 把 253 的代码原封不动搬过来（`<=` / `diff[right] -= 1`）
> 会在 `[[1,2],[2,3]]` 上答 1（正确答案是 2）。
> **区间题读完题干先问自己：端点算不算重叠？**

三种等价解法：
  1. **差分数组 + 前缀和**（值域 `1..1e6` 足够小）—— O(n + V)，最直观。
  2. **双排序扫描**（把所有 start 和 `right+1` 分别排序，双指针扫）—— O(n log n)，不依赖值域。
  3. **最小堆**（堆里存各组当前的右端点）—— O(n log n)，顺手给出分组方案。

复杂度：解法 1 **O(n + V)** 时间 / O(V) 空间；解法 2、3 **O(n log n)** 时间 / O(n) 空间。
       `V = 1e6`，`n <= 1e5` ⟹ 两者实际都很快，面试里解法 2/3 更稳（不吃值域）。

边界：
  - `[[1,2],[2,3]]` → **2**（闭区间，共享端点 2）
  - 单个区间 → 1
  - 全部相同 `[[5,5],[5,5],[5,5]]` → 3
  - 完全不相交 `[[1,2],[4,5]]` → 1
  - 嵌套 `[[1,10],[2,3],[4,5]]` → 2（`[2,3]` 和 `[4,5]` 可同组）
"""

import heapq
from typing import List


##################################################################################################
##### ! Solution 1: 差分数组 + 前缀和求最大重叠（right + 1 处减一）
##### ! 时间复杂度: O(n + V)   空间复杂度: O(V)，V 为值域上界 1e6
##### ! 适用：值域有限的闭区间最大重叠；代码最短、最不容易写错
##################################################################################################


class Solution_1:
    def minGroups(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0
        hi = max(r for _, r in intervals)
        diff = [0] * (hi + 2)                     # ! +2：要能写下标 right + 1
        for left, right in intervals:
            diff[left] += 1
            diff[right + 1] -= 1                  # ! 闭区间 ⟹ 在 right+1 才结束（253 是在 end 结束）
        best = cur = 0
        for d in diff:
            cur += d
            best = max(best, cur)
        return best


##################################################################################################
##### ! Solution 2: 双排序 + 双指针扫描（把 right 平移成 right + 1，退化成半开区间）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：值域很大/是浮点数时的通用写法；面试首选
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def minGroups(self, intervals: List[List[int]]) -> int:
        # ! 关键变换：闭区间 [l, r] ≡ 半开区间 [l, r+1)，之后就是标准 Meeting Rooms II
        starts = sorted(l for l, _ in intervals)
        ends = sorted(r + 1 for _, r in intervals)
        i = j = 0
        cur = best = 0
        n = len(intervals)
        while i < n:
            if starts[i] < ends[j]:               # ! 下一个事件是「开始」⟹ 占用一组
                cur += 1
                best = max(best, cur)
                i += 1
            else:                                 # ! 下一个事件是「结束」⟹ 释放一组
                cur -= 1
                j += 1
        return best


##################################################################################################
##### ! Solution 3: 最小堆存各组的当前右端点（能顺手还原分组方案）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：题目还要求输出具体分组时；堆大小就是答案
##################################################################################################


class Solution_3:
    def minGroups(self, intervals: List[List[int]]) -> int:
        intervals.sort()                          # ! 按 left 升序；left 相同时 right 顺序不影响
        heap: List[int] = []                      # ! heap[k] = 第 k 组当前最后一个区间的 right
        for left, right in intervals:
            # ! 闭区间复用条件是 heap[0] < left（不是 <=！共享端点算重叠）
            if heap and heap[0] < left:
                heapq.heapreplace(heap, right)    # ! 复用结束最早的那一组
            else:
                heapq.heappush(heap, right)       # ! 所有组都还占着 ⟹ 开新组
        return len(heap)


##################################################################################################
##### ! Solution 4: 暴力基准（区间冲突图的染色数 = 最大团，n 小时穷举验证）
##### ! 时间复杂度: O(n^2 · n)   空间复杂度: O(n^2)
##### ! 适用：仅用于对拍。最大重叠数 = 冲突图最大团（区间图是完美图，色数 = 团数）
##################################################################################################


class Solution_4:
    def minGroups(self, intervals: List[List[int]]) -> int:
        n = len(intervals)
        if n == 0:
            return 0
        # ! 直接在所有端点上检查覆盖数（最大重叠一定出现在某个 left 上）
        best = 0
        for l0, _ in intervals:
            cnt = sum(1 for l, r in intervals if l <= l0 <= r)
            best = max(best, cnt)
        return best


if __name__ == "__main__":
    import random

    for cls in (Solution_1, Solution_2, Solution_3, Solution_4):
        s = cls()
        assert s.minGroups([[5, 10], [6, 8], [1, 5], [2, 3], [1, 10]]) == 3
        assert s.minGroups([[1, 3], [5, 6], [8, 10], [11, 13]]) == 1
        # ! 闭区间的招牌样例：253 会答 1，本题必须答 2
        assert s.minGroups([[1, 2], [2, 3]]) == 2
        assert s.minGroups([[1, 1]]) == 1
        assert s.minGroups([[5, 5], [5, 5], [5, 5]]) == 3
        assert s.minGroups([[1, 10], [2, 3], [4, 5]]) == 2

    print([[5, 10], [6, 8], [1, 5], [2, 3], [1, 10]], "->", Solution_2().minGroups([[5, 10], [6, 8], [1, 5], [2, 3], [1, 10]]))
    print([[1, 2], [2, 3]], "->", Solution_2().minGroups([[1, 2], [2, 3]]))

    for _ in range(800):                          # ! 随机对拍（小值域，刻意制造共享端点）
        n = random.randint(1, 8)
        iv = []
        for _ in range(n):
            a = random.randint(1, 8)
            b = random.randint(a, 8)
            iv.append([a, b])
        a1 = Solution_1().minGroups([x[:] for x in iv])
        a2 = Solution_2().minGroups([x[:] for x in iv])
        a3 = Solution_3().minGroups([x[:] for x in iv])
        a4 = Solution_4().minGroups([x[:] for x in iv])
        assert a1 == a2 == a3 == a4, (iv, a1, a2, a3, a4)
    print("随机对拍 800 组通过 ✓（差分 == 双排序扫描 == 最小堆 == 端点暴力）")
