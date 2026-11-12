"""LC-1353 - Maximum Number of Events That Can Be Attended

Level 1 · 05 Heap + Scheduling —— **按天推进 + 堆里放 endDay（最早截止优先）**
题目在问：每个会议是区间 `[start, end]`，**每天只能参加一个**会议
         （参加当天即可，不必待满整个区间）。求最多能参加几个会议。

决定性观察（贪心策略是本题的灵魂）：
  1. **每天应该参加「所有当前可参加的会议里，结束最早的那个」。**
     理由：结束早的会议「机会窗口」最窄，再不参加就过期了；
     而结束晚的会议以后还有机会。这是经典的 **Earliest Deadline First**。
  2. 实现：
     - 按 **start 排序**，用指针把 `start <= day` 的会议的 **end** 推进最小堆。
     - **先清理堆顶所有 `end < day` 的**（已经过期，永远参加不了了）。
     - 堆非空就弹一个（参加它），计数 +1。
     - `day += 1`。
  3. **天数可以跳跃**：如果堆空且还有未入堆的会议，
     直接 `day = 下一个会议的 start`，不要逐天空转（end 可达 10⁵，逐天也能过，
     但跳跃更稳妥，也是通用写法）。

**为什么不能按 end 排序然后贪心取**：那是「区间调度」（LC-0435）的做法，
      适用于「必须占满整个区间」的情形。本题**只占一天**，
      所以同一个会议可以等到它区间里的任意一天再参加 —— 这让它变成了
      「每天做一次选择」的问题，必须用堆动态维护当前可选集合。
      **这是本题和区间贪心最容易混的地方。**

复杂度：**O(n log n + D log n)**，D 是天数跨度（有跳跃时接近 O(n log n)）。
      空间 O(n)。

边界：
  - 会议完全重叠（`[[1,2],[1,2],[1,2]]` → 2，因为只有第 1、2 天）
  - 会议互不重叠 → 全部能参加
  - 单天会议 `[d, d]`
  - 某些会议永远参加不了（堆顶过期清理）
"""

# ! ============================================================================================
# ! 下面这个 Solution 是**用户原有的实现**（逐天 + 最小堆的 EDF 贪心），一字未改。
# ! 后面追加的 Solution_1 / Solution_2 是本次补充的「可跳跃天数」版本和暴力对拍基准。
# ! ============================================================================================

from typing import List
import heapq


class Solution:
    def maxEvents(self, events: List[List[int]]) -> int:
        n = len(events)
        max_day = max(event[1] for event in events)
        events.sort()
        min_heap = []
        ans, j = 0, 0
        for day in range(1, max_day + 1):
            # ! Add all the events whose start date <= today to the min heap
            while j < n and events[j][0] <= day:
                heapq.heappush(min_heap, events[j][1])
                j += 1
            
            # !Remove all the events in the past (e)
            while min_heap and min_heap[0] < day:
                heapq.heappop(min_heap)
            # ! Greedily pick the event whose end date is the earliest
            if min_heap:
                heapq.heappop(min_heap)
                # ! Every time we participate in an event, we
                # ! increase the answer by one
                ans += 1

        return ans


##################################################################################################
##### ! Solution 1: 按 start 排序 + endDay 最小堆 + 逐天（可跳跃）推进
##### ! 时间复杂度: O(n log n + D log n)   空间复杂度: O(n)
##### ! 适用：「每个时间点只能选一个、每个候选有截止期」⟹ Earliest Deadline First
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxEvents(self, events: List[List[int]]) -> int:
        events.sort()                                # ! 按 start 升序
        heap: List[int] = []                         # ! 存 endDay 的最小堆
        i, n, count = 0, len(events), 0
        day = 0
        while i < n or heap:
            if not heap and day < events[i][0]:
                day = events[i][0]                   # ! 天数跳跃，跳到下一个会议开始
            while i < n and events[i][0] <= day:     # ! 所有已开始的会议，把 end 入堆
                heapq.heappush(heap, events[i][1])
                i += 1
            while heap and heap[0] < day:            # ! 清理已过期的（end < 今天）
                heapq.heappop(heap)
            if heap:
                heapq.heappop(heap)                  # ! 参加结束最早的那个
                count += 1
            day += 1
        return count


##################################################################################################
##### ! Solution 2: 暴力 —— 逐天扫描所有未参加的会议，选 end 最小的（基准答案，用来对拍）
##### ! 时间复杂度: O(D · n)   空间复杂度: O(n)
##### ! 适用：正确性参照；直接翻译贪心策略，不用堆
##################################################################################################


class Solution_2:
    def maxEvents(self, events: List[List[int]]) -> int:
        n = len(events)
        used = [False] * n
        count = 0
        last_day = max(e[1] for e in events)
        for day in range(1, last_day + 1):
            best, best_i = None, -1
            for i, (s, e) in enumerate(events):
                if not used[i] and s <= day <= e:
                    if best is None or e < best:
                        best, best_i = e, i
            if best_i >= 0:
                used[best_i] = True
                count += 1
        return count


if __name__ == "__main__":
    import random

    cases = [[[1, 2], [2, 3], [3, 4]], [[1, 2], [2, 3], [3, 4], [1, 2]],
             [[1, 4], [4, 4], [2, 2], [3, 4], [1, 1]], [[1, 2], [1, 2], [1, 2]],
             [[1, 1]], [[1, 100000]]]
    for ev in cases:
        a = Solution_1().maxEvents([e[:] for e in ev])
        b = Solution_2().maxEvents([e[:] for e in ev])
        assert a == b, (ev, a, b)
        print(f"{ev} -> {a}")

    for _ in range(800):
        n = random.randint(1, 8)
        ev = []
        for _ in range(n):
            s = random.randint(1, 8)
            ev.append([s, s + random.randint(0, 4)])
        a = Solution_1().maxEvents([e[:] for e in ev])
        b = Solution_2().maxEvents([e[:] for e in ev])
        assert a == b, (ev, a, b)
    print("随机对拍 800 组通过 ✓（堆版 == 逐天暴力贪心）")
