"""LC-1229 - Meeting Scheduler     ★ 第二轮审核新增（填补「交集 + 长度约束」缺口）

Level 1 · 02 双指针区间交集与多路合并 —— **LC-0986 的交集模板 + 一个长度过滤**
题目在问：`slots1`、`slots2` 是两个人的空闲时间段（**闭区间**，组内互不相交），
         找出**最早**的、长度 `>= duration` 的公共时间段，返回 `[start, start+duration]`；
         找不到返回 `[]`。

### 这道题 = LC-0986 + 两行

[LC-0986 Interval List Intersections](<../01 - LC-0986 - Interval List Intersections>)
求出**所有**交集；本题只要**第一个长度够的**交集。所以：

```python
left  = max(a_start, b_start)
right = min(a_end,   b_end)
if right - left >= duration:          # ! ← 唯一的新增条件
    return [left, left + duration]
# 然后照旧：谁的 end 更早就移动谁
```

**为什么必须先排序？** 题目**不保证** `slots1` / `slots2` 已按时间排序
（这点和 LC-0986 不同，986 保证有序）。不排序直接双指针会漏解。
这是本题最容易被忽略的一行。

**为什么第一个满足的交集就是最早的？**
两个指针都只会右移，`left = max(a_start, b_start)` 随着扫描单调不减
（因为被弹掉的区间 end 更小，后续的 start 都更大）⟹ 第一个命中的 `left` 最小。∎

**为什么是 `right - left >= duration` 而不是 `> `？**
长度恰好等于 `duration` 的段也合法（开会刚好占满）。
注意这里是**长度**比较（差值），不是 LC-0986 里的**非空**判断 `left <= right`；
两者不要混。本题 `duration >= 1`，所以长度 `>= 1` 自动蕴含 `left < right`。

**指针移动的证明**（和 LC-0986 共享）：
若 `a_end < b_end`，则 `A[i]` 与 `B[j+1], B[j+2], ...` 都不可能相交 ——
它们的 start 都 `>= B[j].start`，而 B 组内互不相交 ⟹ `B[j+1].start > B[j].end > A[i].end`。
所以 `A[i]` 已经用尽，`i += 1` 不会丢解。∎

复杂度：**O(m log m + n log n)** 时间（排序主导；若已有序则 O(m+n)），O(1) 额外空间。

边界：
  - 无公共段 → `[]`
  - 公共段长度 < duration → `[]`
  - 长度恰好 == duration → 接受
  - 输入未排序 → 必须先 sort
  - 任一列表为空 → `[]`
"""

from typing import List


##################################################################################################
##### ! Solution 1: 排序 + 双指针求交集，首个长度 >= duration 的交集即答案
##### ! 时间复杂度: O(m log m + n log n)   空间复杂度: O(1) 额外
##### ! 适用：所有「两个有序区间序列求交集」的题；本题只是多了一个长度过滤
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minAvailableDuration(
        self, slots1: List[List[int]], slots2: List[List[int]], duration: int
    ) -> List[int]:
        slots1.sort()                             # ! 题目不保证有序 —— 这行不能省
        slots2.sort()
        i = j = 0
        while i < len(slots1) and j < len(slots2):
            left = max(slots1[i][0], slots2[j][0])
            right = min(slots1[i][1], slots2[j][1])
            if right - left >= duration:          # ! 长度够 ⟹ 因为 left 单调不减，这就是最早的
                return [left, left + duration]
            # ! 谁先结束就弹谁（它不可能再和对方后面的区间产生新交集）
            if slots1[i][1] < slots2[j][1]:
                i += 1
            else:
                j += 1
        return []


##################################################################################################
##### ! Solution 2: 先求出所有交集（复用 LC-0986），再挑第一个够长的
##### ! 时间复杂度: O(m log m + n log n)   空间复杂度: O(m + n)
##### ! 适用：想强调「本题就是 986 的下游」时；代价是多一份交集列表
##################################################################################################


class Solution_2:
    def _intersections(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        # ! 这就是 LC-0986 的原始模板，一字未改
        res: List[List[int]] = []
        i = j = 0
        while i < len(A) and j < len(B):
            lo, hi = max(A[i][0], B[j][0]), min(A[i][1], B[j][1])
            if lo <= hi:                          # ! 986 用的是「非空」判定（闭区间，所以 <=）
                res.append([lo, hi])
            if A[i][1] < B[j][1]:
                i += 1
            else:
                j += 1
        return res

    def minAvailableDuration(
        self, slots1: List[List[int]], slots2: List[List[int]], duration: int
    ) -> List[int]:
        slots1.sort()
        slots2.sort()
        for lo, hi in self._intersections(slots1, slots2):   # ! 交集本身已按时间升序
            if hi - lo >= duration:
                return [lo, lo + duration]
        return []


##################################################################################################
##### ! Solution 3: 事件扫描（把两人的空闲都丢进事件流，覆盖数 == 2 的段就是公共空闲）
##### ! 时间复杂度: O((m+n) log (m+n))   空间复杂度: O(m + n)
##### ! 适用：推广到 k 个人时（覆盖数 == k）；两人情况下不如解法 1 简洁
##################################################################################################


class Solution_3:
    def minAvailableDuration(
        self, slots1: List[List[int]], slots2: List[List[int]], duration: int
    ) -> List[int]:
        events: List[tuple] = []
        for s, e in slots1 + slots2:
            events.append((s, 1))
            events.append((e, -1))
        # ! tie-break：同一位置先 -1 再 +1，避免把 [1,2] 和 [2,3] 当成连续覆盖
        events.sort(key=lambda x: (x[0], x[1]))
        cur = 0
        both_start = None
        for pos, delta in events:
            if cur == 2 and both_start is not None and pos - both_start >= duration:
                return [both_start, both_start + duration]
            cur += delta
            both_start = pos if cur == 2 else None
        return []


##################################################################################################
##### ! Solution 4: 暴力基准（枚举所有可能的起点，检查两人是否都空闲，用于对拍）
##### ! 时间复杂度: O(V · (m + n))   空间复杂度: O(1)
##### ! 适用：仅用于对拍。直接照定义「存在一段长 duration 的时间两人都空」来写
##################################################################################################


class Solution_4:
    def minAvailableDuration(
        self, slots1: List[List[int]], slots2: List[List[int]], duration: int
    ) -> List[int]:
        if not slots1 or not slots2:
            return []
        lo = min(s for s, _ in slots1 + slots2)
        hi = max(e for _, e in slots1 + slots2)
        for t in range(lo, hi + 1):
            if t + duration > hi:
                break
            in1 = any(s <= t and t + duration <= e for s, e in slots1)
            in2 = any(s <= t and t + duration <= e for s, e in slots2)
            if in1 and in2:
                return [t, t + duration]
        return []


if __name__ == "__main__":
    import random

    for cls in (Solution_1, Solution_2, Solution_3, Solution_4):
        s = cls()
        assert s.minAvailableDuration([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 70]], 8) == [60, 68]
        assert s.minAvailableDuration([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 70]], 12) == []
        # ! 长度恰好相等也要接受
        assert s.minAvailableDuration([[0, 10]], [[5, 10]], 5) == [5, 10]
        assert s.minAvailableDuration([[0, 10]], [[20, 30]], 1) == []
        assert s.minAvailableDuration([], [[1, 5]], 1) == []
        # ! 输入未排序
        assert s.minAvailableDuration([[60, 120], [10, 50]], [[60, 70], [0, 15]], 8) == [60, 68]

    print("slots1=[[10,50],[60,120],[140,210]] slots2=[[0,15],[60,70]] d=8 ->",
          Solution_1().minAvailableDuration([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 70]], 8))

    for _ in range(600):                          # ! 随机对拍（组内不相交，顺序打乱）
        def gen():
            t = random.randint(0, 3)
            out = []
            for _ in range(random.randint(0, 4)):
                a = t + random.randint(0, 2)
                b = a + random.randint(1, 4)
                out.append([a, b])
                t = b
            random.shuffle(out)
            return out

        s1, s2 = gen(), gen()
        d = random.randint(1, 4)
        outs = [cls().minAvailableDuration([x[:] for x in s1], [x[:] for x in s2], d)
                for cls in (Solution_1, Solution_2, Solution_3, Solution_4)]
        assert outs[0] == outs[1] == outs[2] == outs[3], (s1, s2, d, outs)
    print("随机对拍 600 组通过 ✓（双指针 == 复用 986 == 事件扫描 == 枚举起点暴力）")
