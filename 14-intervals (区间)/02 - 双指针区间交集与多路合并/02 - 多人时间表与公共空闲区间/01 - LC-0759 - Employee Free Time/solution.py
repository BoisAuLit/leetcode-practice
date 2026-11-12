"""LC-0759 - Employee Free Time  (LeetCode Premium)

Level 1 · 02 双指针区间交集与多路合并 —— **「所有人共同空闲」= 忙碌并集的 Gap**
题目在问：`schedule[i]` 是第 i 个员工的工作区间列表（**已排序、组内互不相交**）。
         返回**所有员工共同空闲**的有限区间列表（正长度，按任意/升序）。

### 决定性观察（整道题就这一句）

> **某一时刻所有人都空闲 ⟺ 该时刻不被任何一个工作区间覆盖。**
> 所以：**把所有人的工作区间合并成并集，并集相邻两段之间的缝隙就是答案。**

于是题目退化成 **LC-0056 Merge Intervals + 取 Gap**，和「有几个员工」毫无关系 ——
这是本题最容易想反的地方（很多人一开始去求「交集的交集」，方向错了）。

必须说清的四个 why：

1. **为什么先合并所有员工的忙碌时间？**
   「共同空闲」是个**全局**条件：只要有**一个**人在忙，这一刻就不算共同空闲。
   所以只需要知道「忙碌时间的并集」，不需要区分是谁在忙。
   求「空闲的交集」等价于求「忙碌的并集」再取补集（德摩根律）。

2. **为什么并集中两个相邻区间之间的正长度间隔代表所有人都空闲？**
   设并集排序后相邻两段为 `[.., a]` 和 `[b, ..]` 且 `a < b`。
   若 `(a, b)` 内某点 `t` 被某个工作区间覆盖，那这个区间会在合并时
   与 `[.., a]` 或 `[b, ..]` 相连（或自成一段落在中间），
   与「它们在并集里相邻」矛盾 ⟹ `(a, b)` 不被任何区间覆盖 ⟹ 全员空闲。∎

3. **为什么零长度 Gap 不输出？**
   `[1,2]` 和 `[2,3]` 之间的「空闲」是 `[2,2]`，长度 0 —— 没有任何一个瞬间是空的。
   代码上就是 `if prev_end < start`（**严格小于**，不是 `<=`）。
   写成 `<=` 会吐出一堆 `[x,x]` 垃圾区间。**这是本题唯一的实现坑。**

4. **为什么不输出 `(-inf, 第一段开始)` 和 `(最后一段结束, +inf)`？**
   题目要求的是**有限（finite）**空闲区间。两端的无界区间长度无穷，
   既不可表示也不是题意（员工日程之外的时间不在讨论范围内）。

### 两种解法

| | A. Flatten + Sort + Merge | B. K-way Merge + Min Heap |
|---|---|---|
| 思路 | 把所有区间倒进一个数组，排序后合并 | 把**每个员工的时间表当成一个有序 Interval Stream**，堆里只留 k 个队头 |
| 时间 | O(N log N) | O(N log k) |
| 空间 | O(N) | O(k) |
| 何时用 | 默认写法，面试够用 | k 很小而 N 很大，或时间表是**流式**读不进内存 |

`N` = 区间总数，`k` = 员工数。
解法 B 和 **LC-0023 Merge k Sorted Lists** 完全同构：
堆里存 `(区间起点, 员工下标, 该员工内部下标)`，弹出一个就把该员工的下一个区间推进去。
这就是「把每个员工的时间表视为一个有序 Interval Stream」的含义 ——
我们从不需要同时持有全部区间，只需要**每条流当前的队头**。

### 跨专题联系

- [LC-0056 Merge Intervals](<../../../01 - 区间合并、插入与范围整理/01 - 标准区间合并与插入/01 - LC-0056 - Merge Intervals>) —— 本题的内核就是它
- [LC-0986 Interval List Intersections](<../../01 - 两个有序区间序列求交集>) —— 两条流求**交集**；本题是 k 条流求**并集的补**
- LC-0023 Merge k Sorted Lists（`06-linked-list`）—— 解法 B 的堆结构原型
- [LC-0253 Meeting Rooms II](<../../../04 - 重叠计数、扫描线与资源分配/01 - 最少会议室与最大并发数/01 - LC-0253 - Meeting Rooms II>)
  —— 也可以用「覆盖数降到 0 的那段」来找 Gap（解法 3）

### 题面来源说明

LC-0759 是 **LeetCode Premium** 题目，本仓库无法合法抓取官方题面，
因此该文件夹**没有 `problem.pdf` / `problem_dark.pdf`**，`metadata.json` 的 `link`
指向官方题目页（可访问性取决于账号权限）。本文件的题意描述为公开通行表述，
解法与证明均为自撰，未复制官方题面。

复杂度：解法 1 **O(N log N)** / O(N)；解法 2 **O(N log k)** / O(k)。

边界：
  - 零长度 Gap：`[[[1,2]],[[2,3]]]` → `[]`
  - 单个员工单个区间 → `[]`
  - 完全重叠：`[[[1,10]],[[2,3]]]` → `[]`
  - 嵌套不产生 Gap：`[[[1,10]],[[2,3],[4,5]]]` → `[]`
  - 正常：`[[[1,2],[5,6]],[[1,3]],[[4,10]]]` → `[[3,4]]`
"""

import heapq
from typing import List


class Interval:
    """LeetCode 官方给的 Interval 类（Premium 题目用的签名）。"""

    def __init__(self, start: int = 0, end: int = 0):
        self.start = start
        self.end = end

    # ! 下面三个不是题目要求的，只是为了本地测试好读
    def __repr__(self) -> str:
        return f"[{self.start},{self.end}]"

    def __eq__(self, other) -> bool:
        return (self.start, self.end) == (other.start, other.end)

    def as_pair(self) -> tuple:
        return (self.start, self.end)


##################################################################################################
##### ! Solution 1: Flatten + Sort + Merge，合并后取相邻段之间的正长度 Gap
##### ! 时间复杂度: O(N log N)   空间复杂度: O(N)   N = 区间总数
##### ! 适用：默认写法。内核就是 LC-0056 Merge Intervals，只是把「合并结果」换成「缝隙」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def employeeFreeTime(self, schedule: List[List["Interval"]]) -> List["Interval"]:
        # ! 第一步：把 k 个员工的区间全部摊平（谁的区间已经不重要了）
        flat = [(iv.start, iv.end) for emp in schedule for iv in emp]
        if not flat:
            return []
        flat.sort()                               # ! 按 start 升序（end 顺序不影响合并结果）

        res: List[Interval] = []
        prev_end = flat[0][1]                     # ! prev_end = 当前已合并并集的右边界
        for start, end in flat[1:]:
            if start > prev_end:
                # ! 严格大于 ⟹ 中间有正长度的缝 ⟹ 全员空闲
                res.append(Interval(prev_end, start))
                prev_end = end
            else:
                # ! 相交或刚好接上（start == prev_end，零长度缝，不输出）⟹ 继续合并
                prev_end = max(prev_end, end)
        return res


##################################################################################################
##### ! Solution 2: K-way Merge + Min Heap（每个员工是一条有序 Interval Stream）
##### ! 时间复杂度: O(N log k)   空间复杂度: O(k)
##### ! 适用：k 远小于 N，或时间表是流式数据读不进内存；与 LC-0023 同构
##################################################################################################


class Solution_2:
    def employeeFreeTime(self, schedule: List[List["Interval"]]) -> List["Interval"]:
        # ! 堆里只放每条流的「队头」：(start, end, 员工下标, 该员工内部下标)
        heap: List[tuple] = []
        for e, emp in enumerate(schedule):
            if emp:
                heap.append((emp[0].start, emp[0].end, e, 0))
        if not heap:
            return []
        heapq.heapify(heap)

        res: List[Interval] = []
        _, prev_end, _, _ = heap[0]
        while heap:
            start, end, e, i = heapq.heappop(heap)
            if start > prev_end:                  # ! 同样是严格大于
                res.append(Interval(prev_end, start))
                prev_end = end
            else:
                prev_end = max(prev_end, end)
            # ! 弹掉一个就把同一员工的下一个区间补进来 —— 永远只持有 k 个区间
            if i + 1 < len(schedule[e]):
                nxt = schedule[e][i + 1]
                heapq.heappush(heap, (nxt.start, nxt.end, e, i + 1))
        return res


##################################################################################################
##### ! Solution 3: 扫描线 / 差分事件（覆盖数从 1 降到 0、再从 0 升到 1 之间就是空闲）
##### ! 时间复杂度: O(N log N)   空间复杂度: O(N)
##### ! 适用：想和 LC-0253 Meeting Rooms II 用同一套事件扫描肌肉记忆
##################################################################################################


class Solution_3:
    def employeeFreeTime(self, schedule: List[List["Interval"]]) -> List["Interval"]:
        events: List[tuple] = []
        for emp in schedule:
            for iv in emp:
                events.append((iv.start, 1))
                events.append((iv.end, -1))
        if not events:
            return []
        # ! tie-break：同一位置先 +1 再 -1，这样 [1,2] 与 [2,3] 之间不会出现 0 覆盖的瞬间
        events.sort(key=lambda x: (x[0], -x[1]))

        res: List[Interval] = []
        cur = 0
        gap_start = None
        for pos, delta in events:
            if cur == 0 and gap_start is not None and pos > gap_start:
                res.append(Interval(gap_start, pos))   # ! 空闲段结束
                gap_start = None
            cur += delta
            if cur == 0:
                gap_start = pos                        # ! 覆盖数归零 ⟹ 空闲段开始
        return res


##################################################################################################
##### ! Solution 4: 暴力基准（在离散点上逐段判断是否全员空闲，用于对拍）
##### ! 时间复杂度: O(V · N)   空间复杂度: O(V)
##### ! 适用：仅用于对拍。直接照着定义「这一段没有任何人在忙」来写
##################################################################################################


class Solution_4:
    def employeeFreeTime(self, schedule: List[List["Interval"]]) -> List["Interval"]:
        flat = [(iv.start, iv.end) for emp in schedule for iv in emp]
        if not flat:
            return []
        lo = min(s for s, _ in flat)
        hi = max(e for _, e in flat)
        # ! busy[t] = 单位段 [t, t+1) 是否有人在忙
        busy = [False] * (hi - lo + 1)
        for s, e in flat:
            for t in range(s, e):
                busy[t - lo] = True
        res: List[Interval] = []
        t = 0
        while t < hi - lo:
            if not busy[t]:
                j = t
                while j < hi - lo and not busy[j]:
                    j += 1
                res.append(Interval(t + lo, j + lo))
                t = j
            else:
                t += 1
        return res


if __name__ == "__main__":
    import random

    def mk(groups):
        return [[Interval(s, e) for s, e in g] for g in groups]

    for cls in (Solution_1, Solution_2, Solution_3, Solution_4):
        s = cls()
        assert s.employeeFreeTime(mk([[(1, 2), (5, 6)], [(1, 3)], [(4, 10)]])) == [Interval(3, 4)]
        assert s.employeeFreeTime(mk([[(1, 3), (6, 7)], [(2, 4)], [(2, 5), (9, 12)]])) == [
            Interval(5, 6),
            Interval(7, 9),
        ]
        # ! 零长度 Gap 不输出
        assert s.employeeFreeTime(mk([[(1, 2)], [(2, 3)]])) == []
        assert s.employeeFreeTime(mk([[(1, 10)], [(2, 3)]])) == []
        assert s.employeeFreeTime(mk([[(1, 10)], [(2, 3), (4, 5)]])) == []
        assert s.employeeFreeTime(mk([[(1, 2)]])) == []
        assert s.employeeFreeTime(mk([[]])) == []

    print("schedule =", [[(1, 2), (5, 6)], [(1, 3)], [(4, 10)]],
          "->", Solution_1().employeeFreeTime(mk([[(1, 2), (5, 6)], [(1, 3)], [(4, 10)]])))

    for _ in range(500):                          # ! 随机对拍：每个员工内部必须有序且不相交
        k = random.randint(1, 4)
        groups = []
        for _ in range(k):
            t = random.randint(0, 12)
            g = []
            for _ in range(random.randint(0, 3)):
                s0 = t + random.randint(0, 2)
                e0 = s0 + random.randint(1, 3)
                g.append((s0, e0))
                t = e0
            groups.append(g)
        if not any(groups):
            continue
        outs = [
            [iv.as_pair() for iv in cls().employeeFreeTime(mk(groups))]
            for cls in (Solution_1, Solution_2, Solution_3, Solution_4)
        ]
        for o in outs[1:]:
            assert sorted(o) == sorted(outs[0]), (groups, outs)
    print("随机对拍 500 组通过 ✓（Flatten+Merge == K-way Heap == 扫描线 == 单位段暴力）")
