"""LC-1146 - Snapshot Array     ★ 第二轮审核新增（Versioned Array / Snapshot）

Level 1 · 05 有状态 API、缓冲区与模拟 —— **版本链 + 二分查找**
API：
  - `SnapshotArray(length)`：一个长度 `length` 的数组，初值全 0
  - `set(index, val)`：把 `index` 位置设为 `val`
  - `snap() -> int`：拍一张快照，返回快照 id（第一次返回 0，之后依次 +1）
  - `get(index, snap_id) -> int`：返回**第 `snap_id` 张快照**时 `index` 的值

---

## 决定性观察：**绝不要真的复制整个数组**

朴素做法是 `snap()` 时 `copy.deepcopy(arr)` ⟹
每次快照 **O(length)** 时间和空间。
`length <= 5*10^4`、`snap` 最多 `5*10^4` 次 ⟹ **25 亿** ⟹ MLE + TLE。

**关键洞察**：
> **一次 `snap()` 之后，绝大多数位置根本没变。**
> 所以**按「位置」存历史，而不是按「快照」存数组。**

```python
self.history = [[(-1, 0)] for _ in range(length)]   # ! 每个 index 一条版本链
self.snap_id = 0
```
每条链里是 `(快照id, 值)` 的**升序**序列，只在**值真的改变时**追加一项。

| | 朴素复制 | **版本链** |
|---|---|---|
| `snap()` | **O(length)** | **O(1)** —— 只是 `snap_id += 1` |
| `set()` | O(1) | **O(1)** 均摊 |
| `get()` | O(1) | **O(log k)** —— 对该位置的版本链二分 |
| 空间 | **O(length × snaps)** | **O(set 的调用次数)** |

> **用 `get` 的 O(log k) 换掉 `snap` 的 O(length)。**
> 这是「**把成本从频繁操作挪到稀少操作**」的典型交易 ——
> 和本 Level 1 其他题「把查询成本挪到更新时」正好是**反方向**的同一思想。

---

## 三个必须想清的点

### ① `get(index, snap_id)` 为什么是「找最后一个 `id <= snap_id` 的项」？

版本链里记录的是**变更点**。若链是 `[(-1,0), (2,5), (7,9)]`：

| 查询 `snap_id` | 答案 | 为什么 |
|---|---|---|
| 0, 1 | **0** | 第一次变更发生在快照 2 之后，所以快照 0/1 时还是初值 |
| 2, …, 6 | **5** | 在快照 2 之后设成 5，直到快照 7 之后才再变 |
| 7 以后 | **9** | — |

所以要找的是「**不超过 `snap_id` 的最大 id**」对应的值
⟹ 经典的 **upper_bound - 1**：

```python
j = bisect_right(chain, (snap_id, float('inf'))) - 1
return chain[j][1]
```

**为什么用 `bisect_right` 而不是 `bisect_left`？**
`bisect_left(chain, (snap_id, ...))` 找的是「第一个 `>= snap_id`」的位置 ——
若链里**恰好有** `snap_id` 这一项，它会停在那一项上，`-1` 之后就**少取了一项**。
`bisect_right` 找「第一个 `> snap_id`」，`-1` 之后正好是最后一个 `<= snap_id` 的项。✓

**为什么元组第二项要用 `inf`？**
比较元组时 Python 先比第一项、相等再比第二项。
用 `(snap_id, inf)` 保证它排在**所有** `(snap_id, 任意值)` 之后
⟹ `bisect_right` 会跳过同 id 的全部项。

### ② 为什么哨兵要用 `(-1, 0)`？

快照 id 从 **0** 开始。若在第一次 `snap()` **之前**就 `get(i, 0)`
（题目保证 `snap_id` 已存在，所以至少 `snap()` 过一次），
那时该位置若从未被 `set`，链里只有哨兵。
用 `-1` 作为哨兵 id ⟹ 它比任何真实 `snap_id` 都小
⟹ 二分**一定能找到它** ⟹ 返回初值 0，**不会越界**。

用 `0` 当哨兵 id 会和真实的快照 0 混淆。**`-1` 是必须的。**

### ③ 同一个快照周期内多次 `set` 同一位置，怎么办？

```python
def set(self, index, val):
    chain = self.history[index]
    if chain[-1][0] == self.snap_id:
        chain[-1] = (self.snap_id, val)      # ! 同一周期内 ⟹ 原地覆盖
    else:
        chain.append((self.snap_id, val))    # ! 新周期 ⟹ 追加
```

**为什么必须覆盖而不是一直追加？**
功能上追加也对（二分会取到最后一个同 id 项……**如果** `bisect_right` 用了 `inf`）。
但**空间会白涨**：同一周期内 `set` 一万次就留一万个同 id 条目。
**覆盖让「链长 = 该位置真正跨越的快照数」**，这才是 O(set 次数) 空间上界的来源。

> ⚠️ 若选择「一直追加」，那 `bisect` **必须**用 `(snap_id, inf)` 的写法，
> 否则会取到同 id 的**第一项**而不是最后一项 ⟹ 值错。
> 本实现**两个保险都上了**。

---

## 和 LC-0981 Time Based Key-Value Store 的区别（条件 D 的说明）

[LC-0981](<../../../05-binary-search (二分查找)/04 - 二分查找与数据结构设计 (Binary Search Design)/01 - 按时间戳检索历史版本/01 - LC-0981 - Time Based Key-Value Store>)
（实体在 `05-binary-search`）确实也是「版本 + 二分」，但：

| | LC-0981 Time Based KV | **LC-1146** 本题 |
|---|---|---|
| 版本号来自 | 调用方**传入**的 timestamp | 系统**自增**的 snap_id |
| 版本粒度 | 每次 `set` 都是一个新版本 | **一次 `snap()` 才切一个版本** |
| 核心难点 | 二分找 `<= timestamp` 的最新值 | **同一周期内要覆盖** + 哨兵 `-1` + `snap` 必须 O(1) |
| 要解决的性能问题 | 无（天然就是版本链） | **避免 O(length) 的整数组复制** |
| Primary Pattern | **Binary Search** | **Design / 版本链结构** |

> **LC-0981 教的是「怎么二分找版本」；LC-1146 教的是
> 「怎么设计存储让 snap 变成 O(1)」。**
> 二分只是本题的**手段**，不是考点 —— 这就是它归在 Design 而不是 Binary Search 的理由。

---

## 复杂度

| 操作 | 时间 | 空间 |
|---|---|---|
| `__init__` | **O(length)** | O(length) |
| `set` | **O(1)** 均摊 | 每次最多 +1 个条目 |
| `snap` | **O(1)** | 0 |
| `get` | **O(log k)** | — （`k` = 该位置的版本链长度） |
| 总空间 | — | **O(length + set 调用次数)** |

⚠️ `get` **不是 O(1)** —— 不要声称「全部 O(1)」。
⚠️ 总空间**不是** O(length × snaps)，这正是版本链的收益。

边界：
  - 从未 `set` 过的位置 → 返回 **0**（哨兵生效）
  - `get(i, 0)`（第一张快照） → 哨兵 `-1 <= 0` ⟹ 能找到
  - `snap()` 之间**没有任何** `set` → 两张快照的值相同，链不增长
  - 同一快照周期内多次 `set` 同一位置 → **只留最后一次**
  - `set` 之后**没有** `snap` 就结束 → 那些值不属于任何已有快照
  - `length = 1`
  - 连续多次 `snap()` → id 依次递增
  - 把同一位置设成相同的值 → 实现仍会记一条（题目不要求去重）
"""

from bisect import bisect_right
from typing import List, Tuple


##################################################################################################
##### ! Solution 1: 每个 index 一条 (snap_id, val) 版本链 + get 时二分
##### ! 时间复杂度: set O(1) 均摊，snap O(1)，get O(log k)   空间复杂度: O(length + set 次数)
##### ! 适用：所有「版本快照 / 历史回溯」设计题。关键是 snap 必须 O(1)
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class SnapshotArray_1:
    def __init__(self, length: int):
        # ! 哨兵 (-1, 0)：-1 比任何真实 snap_id 都小 ⟹ 二分一定能找到 ⟹ 返回初值 0
        self.history: List[List[Tuple[int, int]]] = [[(-1, 0)] for _ in range(length)]
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        chain = self.history[index]
        if chain[-1][0] == self.snap_id:
            chain[-1] = (self.snap_id, val)        # ! 同一快照周期内 ⟹ 原地覆盖（省空间）
        else:
            chain.append((self.snap_id, val))      # ! 跨到新周期 ⟹ 追加一个版本

    def snap(self) -> int:
        self.snap_id += 1                          # ! O(1)：不复制任何数据
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        chain = self.history[index]
        # ! 找最后一个 id <= snap_id 的项（upper_bound - 1）
        j = bisect_right(chain, (snap_id, float("inf"))) - 1
        return chain[j][1]


##################################################################################################
##### ! Solution 2: 两个平行数组（ids / vals）版本链，避免元组比较
##### ! 时间复杂度: 同上   空间复杂度: 同上
##### ! 适用：想避免 (snap_id, inf) 这种元组技巧时；对 ids 直接二分更直白
##################################################################################################


class SnapshotArray_2:
    def __init__(self, length: int):
        self.ids: List[List[int]] = [[-1] for _ in range(length)]      # ! 版本号，升序
        self.vals: List[List[int]] = [[0] for _ in range(length)]      # ! 对应的值
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        if self.ids[index][-1] == self.snap_id:
            self.vals[index][-1] = val             # ! 同周期覆盖
        else:
            self.ids[index].append(self.snap_id)
            self.vals[index].append(val)

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        # ! 直接对纯 int 列表二分，不需要 inf 技巧
        j = bisect_right(self.ids[index], snap_id) - 1
        return self.vals[index][j]


##################################################################################################
##### ! Solution 3: 朴素基准（每次 snap 真的复制整个数组，用于对拍）
##### ! 时间复杂度: snap O(length)，get O(1)   空间复杂度: O(length × snaps)
##### ! 适用：仅用于对拍。length=5*10^4 且 snap 5*10^4 次 ⟹ 25 亿 ⟹ MLE/TLE
##################################################################################################


class SnapshotArray_3:
    def __init__(self, length: int):
        self.arr = [0] * length
        self.snaps: List[List[int]] = []

    def set(self, index: int, val: int) -> None:
        self.arr[index] = val

    def snap(self) -> int:
        self.snaps.append(self.arr[:])             # ! O(length) —— 这就是要优化掉的部分
        return len(self.snaps) - 1

    def get(self, index: int, snap_id: int) -> int:
        return self.snaps[snap_id][index]


if __name__ == "__main__":
    import random

    for cls in (SnapshotArray_1, SnapshotArray_2, SnapshotArray_3):
        # ! LeetCode 官方样例
        s = cls(3)
        s.set(0, 5)
        assert s.snap() == 0
        s.set(0, 6)
        assert s.get(0, 0) == 5                    # ! 快照 0 时 index 0 是 5

        # ! 从未 set 过的位置 ⟹ 0（哨兵生效）
        a = cls(3)
        assert a.snap() == 0
        assert a.get(1, 0) == 0 and a.get(2, 0) == 0

        # ! 同一快照周期内多次 set 同一位置 ⟹ 只留最后一次
        b = cls(1)
        b.set(0, 1); b.set(0, 2); b.set(0, 3)
        assert b.snap() == 0
        assert b.get(0, 0) == 3

        # ! snap 之间没有任何 set ⟹ 两张快照值相同
        c = cls(2)
        c.set(0, 9)
        assert c.snap() == 0
        assert c.snap() == 1
        assert c.get(0, 0) == 9 and c.get(0, 1) == 9

        # ! 跨多个快照
        d = cls(1)
        d.set(0, 10); d.snap()        # id 0: 10
        d.snap()                       # id 1: 10
        d.set(0, 20); d.snap()        # id 2: 20
        d.snap()                       # id 3: 20
        d.set(0, 30); d.snap()        # id 4: 30
        assert [d.get(0, i) for i in range(5)] == [10, 10, 20, 20, 30]

        # ! length = 1，连续 snap
        e = cls(1)
        assert [e.snap() for _ in range(3)] == [0, 1, 2]

    s = SnapshotArray_1(3)
    s.set(0, 5)
    print("set(0,5); snap() ->", s.snap())
    s.set(0, 6)
    print("set(0,6) 之后 get(0, 0) =", s.get(0, 0), "(快照 0 的值仍是 5)")
    print("版本链 history[0] =", s.history[0])

    for _ in range(3000):                          # ! 随机对拍（三种实现必须完全一致）
        n = random.randint(1, 5)
        ops = []
        snaps_made = 0
        for _ in range(random.randint(1, 40)):
            r = random.random()
            if r < 0.45:
                ops.append(("set", random.randrange(n), random.randint(0, 50)))
            elif r < 0.7:
                ops.append(("snap", 0, 0))
                snaps_made += 1
            elif snaps_made > 0:
                ops.append(("get", random.randrange(n), random.randrange(snaps_made)))
        outs = []
        for cls in (SnapshotArray_1, SnapshotArray_2, SnapshotArray_3):
            s = cls(n)
            seq = []
            for op, a, b in ops:
                if op == "set":
                    s.set(a, b); seq.append(None)
                elif op == "snap":
                    seq.append(s.snap())
                else:
                    seq.append(s.get(a, b))
            outs.append(seq)
        assert outs[0] == outs[1] == outs[2], (n, ops, outs)
    print("随机对拍 3000 组通过 ✓（元组版本链 == 平行数组版本链 == 真复制快照基准）")

    # ! 验证空间收益：10000 长的数组、100 次 snap、只 set 过 3 次 ⟹ 链总长远小于 10000*100
    s = SnapshotArray_1(10000)
    for _ in range(100):
        s.snap()
    s.set(5, 1); s.set(6, 2); s.set(7, 3)
    total_entries = sum(len(ch) for ch in s.history)
    assert total_entries == 10000 + 3, total_entries        # ! 10000 个哨兵 + 3 次变更
    print(f"空间验证 ✓（10000 长 + 100 次 snap + 3 次 set ⟹ 仅 {total_entries} 个条目，"
          f"而真复制需要 {10000 * 100} 个）")
