"""LC-2402 - Meeting Rooms III

Level 1 · 05 Heap + Scheduling —— **两个堆**：空闲房间 + 占用中房间
题目在问：n 个房间，会议 `[start, end]`。规则：
  - 优先用**编号最小的空闲房间**；
  - 没有空闲房间就**等**，等到最早结束的那个；等待时会议时长不变（延后开始和结束）；
  - 多个会议等待时，**原 start 早的先开**。
求举办会议最多的房间编号（平局取编号最小）。

决定性观察 —— **为什么需要两个堆**：
  1. 「优先编号最小的空闲房间」⟹ 需要一个**按房间编号排序的最小堆** `free`。
  2. 「等最早结束的那个」⟹ 需要一个**按结束时间排序的最小堆** `busy`，
     元素是 `(end_time, room_id)`。
  3. 每处理一个会议前，先把 `busy` 里所有 `end <= start` 的房间**释放回 `free`**。
     这一步是两个堆之间的「搬运」，是本题的核心循环。

两种情况：
```python
if free:                              # 有空房：直接用编号最小的
    room = heappop(free)
    heappush(busy, (end, room))
else:                                 # 没空房：等最早结束的那个
    e, room = heappop(busy)
    heappush(busy, (e + (end - start), room))    # ★ 时长不变，整体后移
count[room] += 1
```

**最容易写错的一行**：等待时的新结束时间是 `e + (end - start)`，
      **不是 `end`**，也不是 `e + end`。会议时长 `end - start` 必须保持不变。

**为什么按 start 排序就能满足「原 start 早的先开」**：
      我们顺序处理会议，所以 start 早的自然先被分配房间。排序是必须的
      （题目给的 meetings 不保证有序）。

复杂度：**O(m log m + m log n)** —— m 个会议排序 + 每个会议常数次堆操作。空间 O(n)。

和 LC-0253 Meeting Rooms II 的区别（必须分清）：
  - **LC-0253** 只问「最少需要几个房间」⟹ 一个堆存 end 就够，不关心房间编号。
  - **LC-2402** 房间数固定、要**具体分配**、还要**排队等待** ⟹ 需要两个堆。
  LC-0253 的实体目录在 [14-intervals](<../../../14-intervals (区间)/>)（跨专题索引）。

边界：
  - n == 1（所有会议排成一列）
  - 会议完全不重叠 → 全在 0 号房
  - 多个房间计数相同 → 取编号最小
  - 会议之间恰好首尾相接（`end == 下一个 start`，此时房间算空闲）
"""

import heapq
from typing import List


##################################################################################################
##### ! Solution 1: 两个堆 —— free（按房间号）+ busy（按结束时间）
##### ! 时间复杂度: O(m log m + m log n)   空间复杂度: O(n)
##### ! 适用：「固定数量的资源 + 排队等待 + 指定分配规则」类调度
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort()                               # ! 按 start 升序：保证「原 start 早的先开」
        free = list(range(n))                         # ! 空闲房间的最小堆（按编号）
        heapq.heapify(free)
        busy: List[tuple] = []                        # ! (end_time, room_id) 的最小堆
        count = [0] * n
        for start, end in meetings:
            while busy and busy[0][0] <= start:       # ! 释放所有已结束的房间
                _, room = heapq.heappop(busy)
                heapq.heappush(free, room)
            if free:
                room = heapq.heappop(free)            # ! 编号最小的空闲房间
                heapq.heappush(busy, (end, room))
            else:
                e, room = heapq.heappop(busy)         # ! 等最早结束的那个
                heapq.heappush(busy, (e + (end - start), room))   # ! 时长不变，整体后移
            count[room] += 1
        return count.index(max(count))                # ! index 天然返回最小下标


##################################################################################################
##### ! Solution 2: 朴素模拟 —— 每个会议线性扫描所有房间（基准答案，用来对拍）
##### ! 时间复杂度: O(m · n)   空间复杂度: O(n)
##### ! 适用：正确性参照；n 小时完全够用，也最贴近题面描述
##################################################################################################


class Solution_2:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort()
        avail = [0] * n          # ! 每个房间下一次可用的时间
        count = [0] * n
        for start, end in meetings:
            idle = [i for i in range(n) if avail[i] <= start]
            if idle:
                room = idle[0]                         # ! 编号最小的空闲房间
                avail[room] = end
            else:
                earliest = min(avail)
                room = avail.index(earliest)           # ! 最早结束的；平局取编号最小
                avail[room] = earliest + (end - start)
            count[room] += 1
        return count.index(max(count))


if __name__ == "__main__":
    import random

    cases = [(2, [[0, 10], [1, 5], [2, 7], [3, 4]]),
             (3, [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]]),
             (1, [[0, 1], [1, 2]]), (2, [[0, 1]]), (4, [[18, 19], [3, 12], [17, 19], [2, 13], [7, 10]])]
    for n, m in cases:
        a = Solution_1().mostBooked(n, [x[:] for x in m])
        b = Solution_2().mostBooked(n, [x[:] for x in m])
        assert a == b, (n, m, a, b)
        print(f"n={n}, meetings={m} -> {a}")

    for _ in range(1000):
        n = random.randint(1, 4)
        cnt = random.randint(1, 8)
        m = []
        for _ in range(cnt):
            s = random.randint(0, 12)
            m.append([s, s + random.randint(1, 6)])
        # ! 题目保证 start 互不相同
        seen, uniq = set(), []
        for s, e in m:
            while s in seen:
                s += 1
            seen.add(s)
            uniq.append([s, max(e, s + 1)])
        a = Solution_1().mostBooked(n, [x[:] for x in uniq])
        b = Solution_2().mostBooked(n, [x[:] for x in uniq])
        assert a == b, (n, uniq, a, b)
    print("随机对拍 1000 组通过 ✓（双堆 == 朴素模拟）")
