"""LC-1834 - Single-Threaded CPU

Level 1 · 05 Heap + Scheduling —— **事件驱动模拟**（按时间推进 + 可用任务进堆）
题目在问：每个任务有 `(enqueueTime, processingTime)`，单线程 CPU：
         空闲时在**已入队**的任务里选**处理时间最短**的（平局选**下标最小**的）；
         没有可用任务就跳到下一个任务的入队时间。返回任务执行顺序。

决定性观察（和 LC-0502 IPO 是同一个骨架）：
  1. 两个维度又一次分开：
     - **按 enqueueTime 排序** ⟹ 一个指针顺序「释放」已到达的任务。
     - **已到达的任务进最小堆**，键是 `(processingTime, index)` ⟹ 平局自动按下标。
  2. 维护一个当前时间 `now`。每一轮：
     - 把所有 `enqueueTime <= now` 的任务推进堆；
     - 堆空 ⟹ CPU 空转 ⟹ **把 `now` 直接跳到下一个未入队任务的 enqueueTime**
       （不能一秒一秒地走，否则时间范围 10⁹ 会 TLE）；
     - 否则弹出堆顶执行，`now += processingTime`。

**「时间跳跃」是本题最关键的一步**：
      `now = max(now, tasks[i].enqueueTime)` —— 不要用循环逐秒推进。

**排序必须保留原始下标**：输出的是**原始下标**的顺序，而且平局规则就是按下标。
      所以排序前要先 `enumerate`。

复杂度：**O(n log n)** —— 排序 + 每个任务各进出堆一次。空间 O(n)。

和 LC-0502 的对照：
  - 502：按 capital 排序解锁，堆里取 **profit 最大**。
  - 1834：按 enqueueTime 排序解锁，堆里取 **processingTime 最小**。
  **同一个「排序解锁 + 堆选最优」骨架**，只是解锁条件和最优方向不同。
  区别在于 1834 多了一个「时间」状态需要推进。

边界：
  - 所有任务同时入队 → 退化成「按 (processingTime, index) 排序」
  - 任务之间有空档（CPU 需要跳跃等待）
  - processingTime 相同（必须按下标）
  - 单个任务
"""

import heapq
from typing import List


##################################################################################################
##### ! Solution 1: 按入队时间排序 + (processingTime, index) 最小堆 + 时间跳跃
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：所有「任务陆续到达、空闲时从已到达的里面挑最优」的调度模拟
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        # ! 必须带上原始下标：输出要下标，平局也按下标
        indexed = sorted((enq, proc, i) for i, (enq, proc) in enumerate(tasks))
        res, heap = [], []
        now, i, n = 0, 0, len(indexed)
        while len(res) < n:
            while i < n and indexed[i][0] <= now:        # ! 释放所有已到达的任务
                enq, proc, idx = indexed[i]
                heapq.heappush(heap, (proc, idx))        # ! 键自带平局规则
                i += 1
            if not heap:
                now = max(now, indexed[i][0])            # ! 时间跳跃，不要逐秒推进
                continue
            proc, idx = heapq.heappop(heap)
            now += proc
            res.append(idx)
        return res


##################################################################################################
##### ! Solution 2: 朴素模拟 —— 每轮线性扫描所有未完成任务（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：正确性参照；直接翻译题面规则，不做任何优化
##################################################################################################


class Solution_2:
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        n = len(tasks)
        done = [False] * n
        res, now = [], 0
        for _ in range(n):
            avail = [(tasks[i][1], i) for i in range(n) if not done[i] and tasks[i][0] <= now]
            if not avail:
                now = min(tasks[i][0] for i in range(n) if not done[i])   # ! 跳到下一个到达时间
                avail = [(tasks[i][1], i) for i in range(n) if not done[i] and tasks[i][0] <= now]
            proc, idx = min(avail)
            done[idx] = True
            now += proc
            res.append(idx)
        return res


if __name__ == "__main__":
    import random

    cases = [[[1, 2], [2, 4], [3, 2], [4, 1]],
             [[7, 10], [7, 12], [7, 5], [7, 4], [7, 2]],
             [[1, 2]], [[5, 1], [1, 1]], [[1, 1], [1, 1], [1, 1]]]
    for tasks in cases:
        a = Solution_1().getOrder(tasks)
        b = Solution_2().getOrder(tasks)
        assert a == b, (tasks, a, b)
        print(f"{tasks} -> {a}")

    for _ in range(1000):
        n = random.randint(1, 8)
        tasks = [[random.randint(1, 8), random.randint(1, 5)] for _ in range(n)]
        assert Solution_1().getOrder(tasks) == Solution_2().getOrder(tasks), tasks
    print("随机对拍 1000 组通过 ✓（含大量 processingTime 相同的平局）")
