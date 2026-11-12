"""LC-0381 - Insert Delete GetRandom O(1) - Duplicates allowed    ★ 第二轮审核新增

Level 1 · 03 Randomized Data Structures —— **swap-with-last + 下标集合**
API（**允许重复元素**）：
  - `insert(val) -> bool`：插入；返回「插入前集合里是否**不**含 val」
  - `remove(val) -> bool`：删除**一个** val；返回是否删掉了东西
  - `getRandom() -> int`：**按出现次数加权**均匀随机返回一个元素
全部要求 **平均 O(1)**。

---

## 为什么需要 swap-with-last（本 Level 1 的核心技巧）

要同时满足：
- `getRandom` **O(1)** ⟹ 必须有一个**紧凑数组**（`arr[randint(0, n-1)]`）
- `remove` **O(1)** ⟹ 不能用 `list.remove`（O(n) 搬移）

**解法**：把要删的元素和**最后一个**元素交换，然后 `pop()`。
```python
last = arr[-1]
arr[i] = last          # ! 把最后一个搬到坑里
arr.pop()              # ! O(1)
```
数组保持紧凑（没有空洞）⟹ `getRandom` 仍是 O(1)。
**代价**：元素顺序被打乱 —— 但本题不关心顺序。

---

## ⚠️ 允许重复之后，难点全在「下标表」

| | [LC-0380](<../01 - LC-0380 - Insert Delete GetRandom O(1) (学习索引 · 实体在 01-arrays-hashing)>)（不许重复） | **LC-0381** 本题（允许重复） |
|---|---|---|
| 下标表 | `val -> 唯一下标`（**一个 int**） | `val -> 下标集合`（**一个 set**） |
| `remove` | 直接查到下标 | 从 set 里**任取一个**下标 |
| 交换后要更新 | 1 个条目 | **2 个条目**（被删的 + 被搬来的） |
| 空集合 | 不存在 | **必须删掉 key**，否则 `insert` 的返回值会错 |

```python
self.arr = []                       # ! 紧凑数组，getRandom 直接按下标取
self.idx = defaultdict(set)         # ! val -> 它出现的所有下标
```

### 三个必须按顺序想清的坑

**坑 ①：三步的顺序是唯一正确的那一种**

```python
i = self.idx[val].pop()             # ! ① 先从 val 的集合里摘掉下标 i
last = self.arr[-1]
self.arr[i] = last                  # ! 把最后一个元素搬进坑 i
self.idx[last].add(i)               # ! ② 再把 i 记到 last 名下
self.idx[last].discard(len(self.arr) - 1)   # ! ③ last 不再占用原来的末尾下标
self.arr.pop()
```

**坑 ②：当 `val == last` 时，`idx[val]` 和 `idx[last]` 是同一个 set**

这时三步作用在**同一个集合**上，净效果必须是
「**去掉末尾下标，保留下标 i**」（因为位置 `i` 现在确实还放着一个 `val`）。

| 顺序 | `arr=[5,5]`、`idx[5]={0,1}`、`i=0` 的结果 | 对吗 |
|---|---|---|
| **① pop(i) → ② add(i) → ③ discard(tail)** | `{1}` → `{0,1}` → `{0}` | ✅ `arr=[5]`，下标 0 有效 |
| ① add(i) → ② discard(i) → ③ discard(tail) | `{0,1}` → `{1}` → `{}` | ❌ 集合空了，但 `arr[0]` 还有个 5 |

**第二行就是我第一版写错的顺序** —— 它在 `val == last` 时
把「还活着的那个下标」一起删掉了，于是
`remove(5)` 两次会在第二次返回 `False`（随机对拍立刻抓到）。

**特例 `i == len(arr) - 1`（要删的就在末尾）**：
`arr[i] = last` 是自赋值（无害），`add(i)` 之后 `discard(len(arr)-1) == discard(i)`
⟹ 恰好抵消 ⟹ 结果正确。**不需要任何 if 特判。**

**坑 ③：空集合必须删 key**

```python
if not self.idx[val]:
    del self.idx[val]
```
`insert` 的返回值是「插入前是否**不**含 val」，判断依据是 `val in self.idx`。
`defaultdict` 在读取时会**自动创建空 set** ⟹ 不删 key 的话
`val in self.idx` 会对一个「已全部删除」的 val 返回 True ⟹ **返回值错**。

> ⚠️ 用 `defaultdict(set)` 时，**读取就会建 key** ——
> `if self.idx[val]` 这种写法本身就会插入一个空 set。
> 本实现统一在改动后检查并清理。

---

## getRandom 为什么是「按出现次数加权」的均匀随机

`arr` 里每个**元素实例**各占一个位置（重复的 val 占多个位置）
⟹ `arr[randint(0, n-1)]` 选中值 `v` 的概率 = `count(v) / n`。

**这正是题目要的**：「每个元素被返回的概率与它的出现次数成正比」。
（LC-0380 不许重复，所以每个值的概率都是 `1/n`。）∎

---

## 复杂度（必须诚实说明「平均」）

| 操作 | 时间 | 说明 |
|---|---|---|
| `insert` | **O(1)** 平均 | 一次 append + 一次 set.add |
| `remove` | **O(1)** 平均 | `next(iter(set))` 是 O(1) |
| `getRandom` | **O(1)** 最坏 | 纯数组下标访问 |
| 空间 | **O(n)** | 数组 + 下标集合，总大小同阶 |

⚠️ 是「**平均** O(1)」：底层是哈希表和哈希集合，
最坏情况（全部碰撞）会退化。
`getRandom` 是唯一的**最坏 O(1)** 操作（只碰数组）。

⚠️ **`next(iter(a_set))` 是 O(1)** —— 它只取第一个桶里的元素，不遍历整个集合。
但注意它取的是**任意**一个（哈希顺序），不是「最早插入的」。本题不关心是哪个。

边界：
  - 删不存在的元素 → 返回 False，**不改变任何状态**
  - 插入重复元素 → 返回 **False**（插入前已含有）
  - 删到一个都不剩 → **必须删掉 key**
  - `val == arr[-1]`（要删的正好是末尾元素的值）→ **坑 ②**
  - `i == len(arr) - 1`（要删的就在末尾）→ 自赋值，无需特判
  - 全部元素相同 `[1,1,1]` → `getRandom` 恒返回 1
  - 空集合上 `remove` → False
"""

import random
from collections import defaultdict


##################################################################################################
##### ! Solution 1: 紧凑数组 + val -> 下标集合，remove 用 swap-with-last
##### ! 时间复杂度: insert / remove O(1) 平均，getRandom O(1) 最坏   空间复杂度: O(n)
##### ! 适用：所有「O(1) 插删 + 均匀随机」的设计题。顺序敏感，见坑 ②
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class RandomizedCollection_1:
    def __init__(self):
        self.arr = []                       # ! 紧凑数组（无空洞），getRandom 直接取下标
        self.idx = defaultdict(set)         # ! val -> 它出现的所有下标

    def insert(self, val: int) -> bool:
        had = val in self.idx and len(self.idx[val]) > 0
        self.idx[val].add(len(self.arr))
        self.arr.append(val)
        return not had                      # ! 返回「插入前是否不含 val」

    def remove(self, val: int) -> bool:
        if val not in self.idx or not self.idx[val]:
            if val in self.idx and not self.idx[val]:
                del self.idx[val]           # ! 顺手清掉 defaultdict 建出来的空 set
            return False                    # ! 不存在 ⟹ 不改变任何状态
        i = self.idx[val].pop()             # ! ① 先摘掉下标 i（O(1)，任取一个）
        last = self.arr[-1]
        self.arr[i] = last                  # ! 把最后一个元素搬进坑 i
        self.idx[last].add(i)               # ! ② 再把 i 记到 last 名下
        self.idx[last].discard(len(self.arr) - 1)   # ! ③ 清掉原来的末尾下标
        self.arr.pop()
        # ! 空集合必须删 key，否则 insert 的返回值会错（defaultdict 读取就会建 key）
        if not self.idx[val]:
            del self.idx[val]
        if last in self.idx and not self.idx[last]:
            del self.idx[last]
        return True

    def getRandom(self) -> int:
        # ! 每个元素实例占一个位置 ⟹ 概率与出现次数成正比
        return self.arr[random.randrange(len(self.arr))]


##################################################################################################
##### ! Solution 2: 同上，但显式处理 i == len-1 的情形（更啰嗦，但顺序坑被绕开）
##### ! 时间复杂度: insert / remove O(1) 平均   空间复杂度: O(n)
##### ! 适用：不想依赖「add 在 discard 之前」这个微妙顺序时的保守写法
##################################################################################################


class RandomizedCollection_2:
    def __init__(self):
        self.arr = []
        self.idx = defaultdict(set)

    def insert(self, val: int) -> bool:
        had = bool(self.idx.get(val))
        self.idx[val].add(len(self.arr))
        self.arr.append(val)
        return not had

    def remove(self, val: int) -> bool:
        if not self.idx.get(val):
            self.idx.pop(val, None)
            return False
        i = self.idx[val].pop()             # ! 直接 pop 掉一个下标
        tail = len(self.arr) - 1
        if i != tail:                       # ! 只有不在末尾时才需要搬
            last = self.arr[-1]
            self.arr[i] = last
            self.idx[last].discard(tail)
            self.idx[last].add(i)
        self.arr.pop()
        if not self.idx[val]:
            del self.idx[val]
        return True

    def getRandom(self) -> int:
        return self.arr[random.randrange(len(self.arr))]


##################################################################################################
##### ! Solution 3: 朴素基准（用 list，remove 是 O(n)，用于对拍）
##### ! 时间复杂度: insert O(1)，remove **O(n)**，getRandom O(1)   空间复杂度: O(n)
##### ! 适用：仅用于对拍。对比之下能看清 swap-with-last 省掉的是什么
##################################################################################################


class RandomizedCollection_3:
    def __init__(self):
        self.arr = []

    def insert(self, val: int) -> bool:
        had = val in self.arr               # ! O(n)
        self.arr.append(val)
        return not had

    def remove(self, val: int) -> bool:
        if val not in self.arr:
            return False
        self.arr.remove(val)                # ! O(n) 搬移
        return True

    def getRandom(self) -> int:
        return self.arr[random.randrange(len(self.arr))]


if __name__ == "__main__":
    for cls in (RandomizedCollection_1, RandomizedCollection_2, RandomizedCollection_3):
        c = cls()
        # ! LeetCode 官方样例
        assert c.insert(1) is True
        assert c.insert(1) is False         # ! 插入重复 ⟹ False
        assert c.insert(2) is True
        assert c.remove(1) is True
        assert c.remove(1) is True
        assert c.remove(1) is False         # ! 已经没有 1 了
        assert c.getRandom() == 2

        # ! 删到一个都不剩，再插入应返回 True
        e = cls()
        e.insert(5); e.insert(5)
        assert e.remove(5) is True and e.remove(5) is True
        assert e.insert(5) is True          # ! key 必须已被清掉

        # ! 要删的正好是末尾元素的值（坑 ②）
        t = cls()
        t.insert(1); t.insert(2); t.insert(2)
        assert t.remove(2) is True
        assert sorted(t.arr) == [1, 2]
        assert t.remove(2) is True
        assert sorted(t.arr) == [1]
        assert t.remove(2) is False

        # ! 全部元素相同
        s = cls()
        for _ in range(3):
            s.insert(7)
        assert all(s.getRandom() == 7 for _ in range(10))

        # ! 空集合上 remove
        z = cls()
        assert z.remove(1) is False

    c = RandomizedCollection_1()
    print("insert(1) ->", c.insert(1))
    print("insert(1) ->", c.insert(1), "(重复 ⟹ False)")
    print("insert(2) ->", c.insert(2))
    print("remove(1) ->", c.remove(1))
    print("getRandom ->", c.getRandom(), "/", c.getRandom())

    # ! 随机对拍：三种实现的返回序列 + 最终 multiset 必须完全一致
    for _ in range(3000):
        ops = []
        for _ in range(random.randint(1, 40)):
            if random.random() < 0.55:
                ops.append(("insert", random.randint(1, 5)))
            else:
                ops.append(("remove", random.randint(1, 5)))
        results, finals = [], []
        for cls in (RandomizedCollection_1, RandomizedCollection_2, RandomizedCollection_3):
            c = cls()
            seq = []
            for op, v in ops:
                seq.append(c.insert(v) if op == "insert" else c.remove(v))
            results.append(seq)
            finals.append(sorted(c.arr))
        assert results[0] == results[1] == results[2], (ops, results)
        assert finals[0] == finals[1] == finals[2], (ops, finals)
    print("随机对拍 3000 组通过 ✓（下标集合版 == 显式特判版 == list 朴素基准）")

    # ! 验证 getRandom 是「按出现次数加权」的均匀随机
    c = RandomizedCollection_1()
    c.insert(1); c.insert(2); c.insert(2); c.insert(2)      # ! 1 占 1/4，2 占 3/4
    from collections import Counter

    random.seed(42)
    tally = Counter(c.getRandom() for _ in range(40000))
    p1 = tally[1] / 40000
    assert abs(p1 - 0.25) < 0.02, (tally, p1)
    print(f"加权随机验证 ✓（[1,2,2,2] 中 1 出现概率 {p1:.4f} ≈ 0.25）")
