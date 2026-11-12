"""LC-0731 - My Calendar II     ★ 第二轮审核新增（把「在线重叠上限」从 1 推广到 k）

Level 1 · 05 离线区间查询与动态预订 —— **在线预订：允许二重，禁止三重**
题目在问：实现 `MyCalendarTwo`，`book(start, end)`（半开区间 `[start, end)`）。
         允许 **double booking**（某时刻最多 2 个预订），
         但**出现 triple booking 就必须拒绝**（且拒绝后不留痕迹）。

### 核心套路：维护两个列表

```
booked  : 所有已接受的区间
overlaps: 所有「已经二重」的区间（即任意两个已接受区间的交集）
```

`book(s, e)` 的判断：
1. **先看 `overlaps`**：如果 `[s,e)` 和任何一个二重区间相交 ⟹ 会变三重 ⟹ **拒绝**。
2. 否则接受。接受时要**把新产生的二重区间记下来**：
   对每个已接受的 `[bs, be)`，交集 `[max(s,bs), min(e,be))` 非空就塞进 `overlaps`。
3. 最后把 `[s,e)` 加进 `booked`。

**为什么「与 overlaps 相交」就等价于「三重」？**
`overlaps` 里每一段都已经被 2 个已接受区间覆盖。
新区间压上去 ⟹ 该段覆盖数变成 3。反过来，若新区间造成某点覆盖数达到 3，
那该点在新区间之前就已被 2 个区间覆盖 ⟹ 必在某个 `overlaps` 段内。∎

**为什么判断必须在修改之前全部做完？**
拒绝不能留下痕迹。所以**先全量检查 `overlaps`，确认通过后才写入** ——
如果边检查边往 `overlaps` 里塞，一旦后面发现要拒绝，状态就脏了。
**这是本题最容易写出的 bug。**

**为什么半开区间依然用严格不等号？**
`s < be and bs < e`。`[10,20)` 和 `[20,30)` 不算重叠，所以可以三个背靠背排下去。

### 与 LC-0729 / LC-0732 的关系（一条清晰的升级链）

| 题 | 上限 | 做法 | 单次复杂度 |
|---|---|---|---|
| [LC-0729 My Calendar I](<../01 - LC-0729 - My Calendar I>) | 1 | 一个列表，相交就拒 | O(n) |
| **LC-0731** 本题 | 2 | 两个列表：`booked` + `overlaps` | O(n) |
| LC-0732 My Calendar III | ∞（只问最大重叠数） | 差分 map / 动态开点线段树 | O(n) 或 O(log V) |

> 这个套路能推广到任意 k：维护 `k-1` 层列表（第 i 层是「已经 i 重」的区间），
> 但 k 一大就该换成**差分 map 直接算覆盖数**（解法 2），别再堆列表了。

### 解法 2（差分 map）为什么更通用

用 `delta[x]` 记录位置 `x` 的覆盖数变化，每次 `book` 先试加
`delta[s] += 1; delta[e] -= 1`，然后扫一遍前缀和看峰值是否 > 2；
超了就**回滚**。
这就是 [LC-1094 Car Pooling](<../../../04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/01 - LC-1094 - Car Pooling>)
的在线版本，把上限 2 换成 `capacity` 就是另一道题。
代价：每次要重扫整个 map ⟹ 单次 O(n log n)，比解法 1 慢，
但**改上限只要改一个数字**，而且直接推广到 LC-0732。

复杂度：解法 1 单次 **O(n)**、n 次共 O(n²)（本题 `n <= 1000`，完全够用）；
       解法 2 单次 **O(n log n)**（有序 map 遍历），胜在通用。
       真要 O(log V) 得上动态开点线段树 / 平衡树（见 LC-0732）。

边界：
  - `book(10,20)`、`book(50,60)`、`book(10,40)` → True, True, True
  - 再 `book(5,15)` → **False**（10~15 会变三重）
  - 再 `book(5,10)` → True（半开，不碰 10）
  - 被拒绝后状态不变：紧接着 `book(25,55)` 仍为 True
  - 完全相同的区间 book 三次 → True, True, False
"""

from collections import defaultdict
from typing import List, Tuple


##################################################################################################
##### ! Solution 1: 维护 booked + overlaps 两个列表，与 overlaps 相交即三重
##### ! 时间复杂度: 单次 book O(n)，n 次共 O(n^2)   空间复杂度: O(n^2) 最坏
##### ! 适用：本题 n <= 1000 的默认答案；思路最直接，面试首选
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class MyCalendarTwo_1:
    def __init__(self):
        self.booked: List[Tuple[int, int]] = []      # ! 所有已接受的区间
        self.overlaps: List[Tuple[int, int]] = []    # ! 已经「二重」的那些段

    def book(self, startTime: int, endTime: int) -> bool:
        # ! 第一步：只检查，不修改。碰到任何二重段 ⟹ 会变三重 ⟹ 拒绝
        for s, e in self.overlaps:
            if startTime < e and s < endTime:        # ! 半开区间相交：两边严格小于
                return False
        # ! 第二步：确认接受之后，才记录新产生的二重段
        for s, e in self.booked:
            lo, hi = max(startTime, s), min(endTime, e)
            if lo < hi:                              # ! 交集非空（半开 ⟹ 严格小于）
                self.overlaps.append((lo, hi))
        self.booked.append((startTime, endTime))
        return True


##################################################################################################
##### ! Solution 2: 差分 map + 试加/回滚（在线版的 LC-1094，改上限只需改一个数）
##### ! 时间复杂度: 单次 O(n log n)   空间复杂度: O(n)
##### ! 适用：上限 k 不固定、或要推广到 LC-0732「最大重叠数」时
##################################################################################################


class MyCalendarTwo_2:
    LIMIT = 2                                        # ! 改成 1 就是 LC-0729，改成 k 就是 k 重预订

    def __init__(self):
        self.delta = defaultdict(int)                # ! delta[x] = 位置 x 的覆盖数变化

    def book(self, startTime: int, endTime: int) -> bool:
        self.delta[startTime] += 1                   # ! 先试着加上去
        self.delta[endTime] -= 1
        cur = 0
        for x in sorted(self.delta):                 # ! 扫前缀和求峰值
            cur += self.delta[x]
            if cur > self.LIMIT:
                # ! 超了 ⟹ 回滚，必须让状态和没调用过完全一样
                self.delta[startTime] -= 1
                self.delta[endTime] += 1
                if self.delta[startTime] == 0:
                    del self.delta[startTime]
                if self.delta[endTime] == 0:
                    del self.delta[endTime]
                return False
        return True


##################################################################################################
##### ! Solution 3: 暴力基准（在单位段上直接数覆盖数，用于对拍）
##### ! 时间复杂度: 单次 O(V)   空间复杂度: O(V)
##### ! 适用：仅用于对拍。照定义「任何单位段的覆盖数不能超过 2」来写
##################################################################################################


class MyCalendarTwo_3:
    def __init__(self, limit: int = 2, size: int = 64):
        self.cnt = [0] * size                        # ! cnt[t] = 单位段 [t, t+1) 的覆盖数
        self.limit = limit

    def book(self, startTime: int, endTime: int) -> bool:
        if any(self.cnt[t] + 1 > self.limit for t in range(startTime, endTime)):
            return False                             # ! 先全量检查，再修改
        for t in range(startTime, endTime):
            self.cnt[t] += 1
        return True


if __name__ == "__main__":
    import random

    for cls in (MyCalendarTwo_1, MyCalendarTwo_2, MyCalendarTwo_3):
        c = cls()
        assert c.book(10, 20) is True
        assert c.book(50, 60) is True
        assert c.book(10, 40) is True
        assert c.book(5, 15) is False                # ! 10~15 会变三重
        assert c.book(5, 10) is True                 # ! 半开区间，不碰到 10
        assert c.book(25, 55) is True
        # ! 被拒绝不能污染状态：上面那次 False 之后一切照常
        c2 = cls()
        assert c2.book(1, 5) is True
        assert c2.book(1, 5) is True
        assert c2.book(1, 5) is False                # ! 第三次同样的区间 ⟹ 三重 ⟹ 拒绝
        assert c2.book(5, 9) is True                 # ! 端点相接，不算重叠

    c = MyCalendarTwo_1()
    for a, b in [(10, 20), (50, 60), (10, 40), (5, 15), (5, 10), (25, 55)]:
        print(f"book({a},{b}) ->", c.book(a, b))

    for _ in range(400):                             # ! 随机对拍：三种实现的 True/False 序列必须完全一致
        ops = []
        for _ in range(random.randint(1, 25)):
            a = random.randint(0, 20)
            b = a + random.randint(1, 6)
            ops.append((a, b))
        outs = []
        for cls in (MyCalendarTwo_1, MyCalendarTwo_2, MyCalendarTwo_3):
            c = cls()
            outs.append([c.book(a, b) for a, b in ops])
        assert outs[0] == outs[1] == outs[2], (ops, outs)
    print("随机对拍 400 组通过 ✓（booked+overlaps == 差分 map 试加回滚 == 单位段暴力）")
