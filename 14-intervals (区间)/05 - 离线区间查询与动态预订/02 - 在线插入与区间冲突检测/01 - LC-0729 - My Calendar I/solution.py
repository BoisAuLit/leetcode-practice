"""LC-0729 - My Calendar I

Level 1 · 05 离线区间查询与动态预订 —— **半开区间的在线冲突检测**
题目在问：实现 `MyCalendar`，`book(startTime, endTime)` 尝试加入半开区间
         `[startTime, endTime)`。只有**不与已接受的任何区间重叠**时才接受并返回
         `True`，否则拒绝并返回 `False`（**被拒绝的预订不能留下任何痕迹**）。

### 重叠判定（整道题的核心，必须背下来）

两个半开区间 `[s1, e1)` 和 `[s2, e2)` 相交 ⟺
```python
s1 < e2 and s2 < e1        # ! 两个都是严格小于
```

**为什么必须用严格不等号 `<` 而不是 `<=`？**
  半开区间 `[s, e)` **不包含** `e`。
  `[10,20)` 的实际占用是 `10 <= t < 20`；`[20,30)` 是 `20 <= t < 30`。
  两者没有任何公共的 `t` ⟹ 不冲突。
  若写成 `s1 <= e2 and s2 <= e1`，`s2 == e1`（即 `20 <= 20`）会判成冲突 ⟹ 误拒。

**为什么端点相等不冲突？**
  端点 `e` 是「结束的瞬间」，不属于这个区间。
  现实类比：10:00–11:00 的会和 11:00–12:00 的会可以背靠背开。
  → **做区间题第一步永远是确认端点语义**；本题是半开，
    [LC-2406](<../../../04 - 重叠计数、扫描线与资源分配/01 - 最少会议室与最大并发数/02 - LC-2406 - Divide Intervals Into Minimum Number of Groups>)
    是闭区间，两者的不等号正好差一个 `=`。

**不冲突的等价写法**（反过来更好记）：
```python
e1 <= s2 or e2 <= s1       # ! 要么我整个在你前面，要么你整个在我前面
```

### 三种方案的复杂度必须如实说明

| | 方案 | 单次 `book` | n 次总计 | 备注 |
|---|---|---|---|---|
| 1 | 线性扫描列表 | **O(n)** | O(n²) | 本题 `n <= 1000` ⟹ 完全够用，**默认答案** |
| 2 | 有序列表 + `bisect` | 查 **O(log n)** + **插入 O(n)** | O(n²) | 比较次数降了，但**总体没变** |
| 3 | 平衡 BST / Ordered Map（`sortedcontainers`、红黑树） | **O(log n)** | O(n log n) | 真正的对数级；Java 用 `TreeMap.floorKey/ceilingKey` |

> ⚠️ **不能因为调用了 `bisect` 就宣称动态插入是 O(log n)。**
> `bisect.insort` 内部是 `list.insert`，要把后面的元素整体搬移 ⟹ **O(n)**。
> Python 没有内置平衡树；要真正的 O(log n) 得用第三方
> `sortedcontainers.SortedList`，或自己写一棵 BST / 线段树（动态开点）。
> 本题给定 `n <= 1000`，**单次 O(n) 检查就是合理且推荐的基础方案**，
> 面试里先写解法 1，再口述解法 3 的升级路径。

### 解法 2 的两个邻居为什么就够

有序列表里已接受的区间**两两不相交**，所以按 start 排序后 end 也是升序。
对新区间 `[s, e)`：
  - 用 `bisect_right(starts, s) - 1` 找到**最后一个 start <= s** 的区间 → 左邻居
  - 它的下一个就是**第一个 start > s** 的区间 → 右邻居
只需检查这两个：左邻居的 `end > s`？右邻居的 `start < e`？
更远的区间因为单调性必然不可能相交。∎

### 跨专题联系

- [LC-0057 Insert Interval](<../../../01 - 区间合并、插入与范围整理/01 - 标准区间合并与插入/02 - LC-0057 - Insert Interval>)
  —— 同样是「往有序不相交列表里插一个」，但 57 是**合并**，本题是**拒绝**
- [LC-0253 Meeting Rooms II](<../../../04 - 重叠计数、扫描线与资源分配/01 - 最少会议室与最大并发数/01 - LC-0253 - Meeting Rooms II>)
  —— 离线版的「最大重叠数」；本题是在线把重叠数限制在 1
- `LC-0731 My Calendar II` —— 同一框架，上限放宽到 2（见本 Level 2 的第二题）
- `17-design` 的设计题 —— 在线数据结构的通用套路

复杂度：解法 1 单次 **O(n)**、总 O(n²)；解法 2 同为 O(n²)（插入搬移主导）；
       解法 3 单次 **O(log n)**、总 O(n log n)。

边界：
  - `book(10,20)` 后 `book(20,30)` → **True**（半开区间，端点相接不冲突）
  - `book(10,20)` 后 `book(15,25)` → False
  - `book(10,20)` 后 `book(10,20)` → False（完全相同）
  - `book(10,20)` 后 `book(12,15)` → False（被包含也算重叠）
  - `book(10,20)` 后 `book(5,30)` → False（包含对方）
  - 被拒绝后再 `book(20,30)` 仍然 True（**拒绝不能污染状态**）
"""

import bisect
from typing import List, Tuple


##################################################################################################
##### ! Solution 1: 线性扫描已接受区间，用 s < e2 and s2 < e 判重叠
##### ! 时间复杂度: 单次 book O(n)，n 次共 O(n^2)   空间复杂度: O(n)
##### ! 适用：n <= 1000 的本题。最清晰、最不容易写错，面试的默认答案
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class MyCalendar_1:
    def __init__(self):
        self.booked: List[Tuple[int, int]] = []

    def book(self, startTime: int, endTime: int) -> bool:
        for s, e in self.booked:
            # ! 半开区间的相交条件：两边都是严格小于
            if startTime < e and s < endTime:
                return False                      # ! 冲突 ⟹ 拒绝，且不改动任何状态
        self.booked.append((startTime, endTime))
        return True


##################################################################################################
##### ! Solution 2: 有序列表 + bisect 只检查左右两个邻居
##### ! 时间复杂度: 查找 O(log n)，但 insort 搬移 O(n) ⟹ 单次仍是 O(n)，n 次共 O(n^2)
##### ! 适用：比较次数敏感时；也用来讲清「bisect 不等于 O(log n) 插入」这件事
##################################################################################################


class MyCalendar_2:
    def __init__(self):
        self.starts: List[int] = []               # ! 已接受区间的 start，升序
        self.ends: List[int] = []                 # ! 对应的 end（因为互不相交，也是升序）

    def book(self, startTime: int, endTime: int) -> bool:
        i = bisect.bisect_right(self.starts, startTime)
        # ! 左邻居（最后一个 start <= startTime）：它的 end 伸过来了吗？
        if i > 0 and self.ends[i - 1] > startTime:
            return False
        # ! 右邻居（第一个 start > startTime）：它的 start 被我盖住了吗？
        if i < len(self.starts) and self.starts[i] < endTime:
            return False
        self.starts.insert(i, startTime)          # ! O(n) 搬移 —— 总复杂度卡在这里
        self.ends.insert(i, endTime)
        return True


##################################################################################################
##### ! Solution 3: 自写平衡性无保证的 BST（按 start 组织，Java 对应 TreeMap）
##### ! 时间复杂度: 期望 O(log n)，最坏（有序插入退化成链）O(n)
##### ! 适用：讲清 Ordered Map 方案的形状；真要保证 O(log n) 得用红黑树 / SortedList
##################################################################################################


class _Node:
    __slots__ = ("s", "e", "left", "right")

    def __init__(self, s: int, e: int):
        self.s, self.e = s, e
        self.left = self.right = None


class MyCalendar_3:
    def __init__(self):
        self.root = None

    def book(self, startTime: int, endTime: int) -> bool:
        node = _Node(startTime, endTime)
        if self.root is None:
            self.root = node
            return True
        cur = self.root
        while True:
            if endTime <= cur.s:                  # ! 我整个在它左边（<= 不冲突）⟹ 往左走
                if cur.left is None:
                    cur.left = node
                    return True
                cur = cur.left
            elif startTime >= cur.e:              # ! 我整个在它右边 ⟹ 往右走
                if cur.right is None:
                    cur.right = node
                    return True
                cur = cur.right
            else:
                return False                      # ! 既不在左也不在右 ⟹ 相交 ⟹ 拒绝


if __name__ == "__main__":
    import random

    for cls in (MyCalendar_1, MyCalendar_2, MyCalendar_3):
        c = cls()
        assert c.book(10, 20) is True
        assert c.book(15, 25) is False
        assert c.book(20, 30) is True             # ! 半开区间：20 这一点不冲突
        assert c.book(10, 20) is False
        assert c.book(12, 15) is False
        assert c.book(5, 30) is False
        assert c.book(0, 10) is True              # ! 刚好贴在 10 左边

    c = MyCalendar_1()
    print("book(10,20) ->", c.book(10, 20))
    print("book(15,25) ->", c.book(15, 25))
    print("book(20,30) ->", c.book(20, 30))

    for _ in range(400):                          # ! 随机对拍：三种实现必须给出完全一致的 True/False 序列
        ops = []
        for _ in range(random.randint(1, 25)):
            a = random.randint(0, 15)
            b = a + random.randint(1, 4)
            ops.append((a, b))
        res = []
        for cls in (MyCalendar_1, MyCalendar_2, MyCalendar_3):
            c = cls()
            res.append([c.book(a, b) for a, b in ops])
        assert res[0] == res[1] == res[2], (ops, res)
        # ! 独立基准：用「已接受集合」重新验一遍语义
        acc = []
        ref = []
        for a, b in ops:
            ok = all(b <= s or e <= a for s, e in acc)
            ref.append(ok)
            if ok:
                acc.append((a, b))
        assert ref == res[0], (ops, ref, res[0])
    print("随机对拍 400 组通过 ✓（线性扫描 == bisect 邻居 == BST == 语义基准）")
