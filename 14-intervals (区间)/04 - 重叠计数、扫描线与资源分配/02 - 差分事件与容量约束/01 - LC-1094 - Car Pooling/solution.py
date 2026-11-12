"""LC-1094 - Car Pooling

Level 1 · 04 重叠计数、扫描线与资源分配 —— **差分数组（Difference Array）模板题**
题目在问：车容量 `capacity`，`trips[i] = [numPassengers, from, to]` 表示
         在 `from` 上车、`to` 下车（**半开区间 `[from, to)`**，车只往东开、不回头）。
         问能不能完成所有行程。

决定性观察：
  **「某一时刻车上有几个人」= 所有覆盖该位置的 trip 的人数之和 = 带权最大重叠。**
  于是题目 ⟹ **检查任意位置的覆盖权重和是否超过 capacity**。

### 差分数组的三句话

对区间 `[l, r)` 整体加 `v`：
```python
diff[l] += v
diff[r] -= v          # ! 半开区间 ⟹ 在 r 处就减掉（r 位置已经不在车上了）
```
扫一遍前缀和，`prefix[i]` 就是位置 `i` 的实际值。
**把 n 次「区间加」从 O(n·len) 降到 O(n + V)。**

为什么 `diff[r] -= v` 而不是 `diff[r + 1] -= v`：
  因为乘客在 `to` 这一站**下车**，`to` 位置他已经不占座。
  这是半开区间；对比 [LC-2406](../../01%20-%20最少会议室与最大并发数) 的闭区间要写 `right + 1`。
  → **先判断端点语义，再决定减号写在哪一格。**

为什么只检查「车上人数」而不用真的模拟上下车顺序：
  车单向行驶 ⟹ 位置 `i` 处车上的人恰好是 `{trip : from <= i < to}`。
  同一站先下后上是自动满足的：`diff[to] -= v` 和 `diff[to] += v'`
  在同一格累加，前缀和取到该格时两者都已生效。∎

三种解法：
  1. **差分数组 + 前缀和**（`to <= 1000`，值域小）—— O(n + V)，最快最短。⭐️
  2. **事件排序扫描**（`(pos, delta)` 排序，`delta` 升序让「下车」先于「上车」）
     —— O(n log n)，值域无限/浮点时的通用写法。
  3. **最小堆**（堆里存当前在车上的 trip 的 `to`，到站先弹出）—— O(n log n)，
     和 Meeting Rooms II 同构，便于迁移。

复杂度：解法 1 **O(n + V)** / O(V)；解法 2、3 **O(n log n)** / O(n)。

边界：
  - 同一站下车又上车 `[[2,1,5],[3,5,7]]`, cap 3 → **True**（5 这一站先下 2 再上 3）
  - 单次行程就超载 `[[5,1,2]]`, cap 4 → False
  - 嵌套行程 `[[2,1,5],[3,3,7]]`, cap 4 → False（位置 3~5 车上 5 人）
  - `capacity` 刚好等于峰值 → True（`<=` 不是 `<`）
"""

import heapq
from typing import List


##################################################################################################
##### ! Solution 1: 差分数组 + 前缀和（to 处直接减，因为是半开区间）
##### ! 时间复杂度: O(n + V)   空间复杂度: O(V)，本题 V = 1001
##### ! 适用：值域有限的「区间加 + 查最大值」；差分数组的标准模板
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        diff = [0] * 1001                         # ! 题目保证 0 <= from < to <= 1000
        for num, start, end in trips:
            diff[start] += num                    # ! start 站上车
            diff[end] -= num                      # ! end 站下车 —— 半开区间，就减在 end 这一格
        cur = 0
        for d in diff:
            cur += d
            if cur > capacity:                    # ! 任何一刻超了就失败
                return False
        return True


##################################################################################################
##### ! Solution 2: 事件排序扫描（(pos, delta) 排序，delta 升序 ⟹ 同站先下车再上车）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：坐标很大或是浮点数时；排序的 tie-break 是本解法唯一的坑
##################################################################################################


class Solution_2:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        events: List[tuple] = []
        for num, start, end in trips:
            events.append((start, num))           # ! +num
            events.append((end, -num))            # ! -num
        # ! tie-break：同一位置先处理负的（下车），否则会虚高导致误判超载
        events.sort(key=lambda e: (e[0], e[1]))
        cur = 0
        for _, delta in events:
            cur += delta
            if cur > capacity:
                return False
        return True


##################################################################################################
##### ! Solution 3: 最小堆（堆顶是最早下车的 trip，和 Meeting Rooms II 同构）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：想复用 LC-0253 的肌肉记忆；也便于扩展成「输出每一站车上有谁」
##################################################################################################


class Solution_3:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        trips.sort(key=lambda t: t[1])            # ! 按上车站排序
        heap: List[tuple] = []                    # ! (下车站 to, 人数 num)
        cur = 0
        for num, start, end in trips:
            while heap and heap[0][0] <= start:   # ! <= ：到站就下车（半开区间）
                _, out = heapq.heappop(heap)
                cur -= out
            cur += num
            if cur > capacity:
                return False
            heapq.heappush(heap, (end, num))
        return True


##################################################################################################
##### ! Solution 4: 暴力基准（对每个位置直接把覆盖它的 trip 人数加起来，用于对拍）
##### ! 时间复杂度: O(V · n)   空间复杂度: O(1)
##### ! 适用：仅用于对拍，顺便把「车上人数 = 带权覆盖数」这个定义写成代码
##################################################################################################


class Solution_4:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        if not trips:
            return True
        hi = max(t[2] for t in trips)
        for pos in range(hi + 1):
            onboard = sum(num for num, s, e in trips if s <= pos < e)   # ! 半开：s <= pos < e
            if onboard > capacity:
                return False
        return True


if __name__ == "__main__":
    import random

    for cls in (Solution_1, Solution_2, Solution_3, Solution_4):
        s = cls()
        assert s.carPooling([[2, 1, 5], [3, 3, 7]], 4) is False
        assert s.carPooling([[2, 1, 5], [3, 3, 7]], 5) is True
        # ! 同一站先下后上：5 站下 2 人、上 3 人 ⟹ 峰值 3，容量 3 够用
        assert s.carPooling([[2, 1, 5], [3, 5, 7]], 3) is True
        assert s.carPooling([[5, 1, 2]], 4) is False
        assert s.carPooling([[9, 0, 1], [3, 3, 7]], 4) is False
        assert s.carPooling([], 1) is True

    print([[2, 1, 5], [3, 3, 7]], "cap=4 ->", Solution_1().carPooling([[2, 1, 5], [3, 3, 7]], 4))
    print([[2, 1, 5], [3, 5, 7]], "cap=3 ->", Solution_1().carPooling([[2, 1, 5], [3, 5, 7]], 3))

    for _ in range(600):                          # ! 随机对拍（小值域，刻意制造同站上下车）
        n = random.randint(0, 6)
        tr = []
        for _ in range(n):
            a = random.randint(0, 6)
            b = random.randint(a + 1, 7)
            tr.append([random.randint(1, 4), a, b])
        cap = random.randint(1, 10)
        a1 = Solution_1().carPooling([t[:] for t in tr], cap)
        a2 = Solution_2().carPooling([t[:] for t in tr], cap)
        a3 = Solution_3().carPooling([t[:] for t in tr], cap)
        a4 = Solution_4().carPooling([t[:] for t in tr], cap)
        assert a1 == a2 == a3 == a4, (tr, cap, a1, a2, a3, a4)
    print("随机对拍 600 组通过 ✓（差分 == 事件排序 == 最小堆 == 逐位置暴力）")
