"""LC-0460 - LFU Cache

Level 1 · 02 Cache 与 O(1) 淘汰策略 —— **频率桶（Frequency Buckets）**
API：
  - `LFUCache(capacity)`
  - `get(key) -> int`：命中返回值并**使用次数 +1**，否则返回 -1
  - `put(key, value)`：插入/更新；满了就淘汰**使用次数最少**的 key；
    **次数相同时淘汰最久未使用的**（LFU 内部按 LRU 打破平局）
要求所有操作 **平均 O(1)**。

---

## 为什么需要「频率桶」这个结构

朴素想法是「扫一遍找最小 freq」⟹ **O(n)**，不满足要求。
用堆按 freq 排序 ⟹ **O(log n)**，而且 freq 会变（堆里改键很麻烦）。

**关键观察**：
> **freq 只会 +1，一次一步。** 所以不需要「排序」，
> 只需要维护一个 **`min_freq` 指针**，以及按 freq 分桶的链表。

### 三个结构（缺一不可）

```python
self.key_to_val  = {}                      # ! key -> value
self.key_to_freq = {}                      # ! key -> 当前使用次数
self.freq_to_keys = defaultdict(OrderedDict)   # ! freq -> {key: None}，保持插入顺序
self.min_freq = 0                          # ! 当前最小的非空 freq
```

**为什么每个桶要用 `OrderedDict` 而不是 `set`？**
因为「freq 相同时淘汰最久未使用的」—— 需要**顺序**。
`OrderedDict` 的 `popitem(last=False)` 是 **O(1)** 弹出最旧的。
（等价实现：每个桶一个**双向链表** + `key -> node` 的字典。）

---

## 两个决定性不变量

### ① `min_freq` 的维护只需要两条规则

```
规则 A：put 一个新 key  ⟹  min_freq = 1
规则 B：把某个 key 从 freq f 提升到 f+1 之后，
        若桶 f 变空且 f == min_freq  ⟹  min_freq += 1
```

**为什么规则 B 里 `min_freq` 只会 +1，不会跳更多？**
因为被提升的那个 key 现在在桶 `f+1` 里 ⟹ **桶 `f+1` 必然非空**
⟹ 新的最小非空 freq 不可能大于 `f+1`。∎

**为什么规则 A 把 `min_freq` 直接设成 1 是对的？**
新 key 的 freq 是 1，而 freq 的最小可能值就是 1 ⟹ 立刻就是全局最小。∎

> **这两条规则是整道题的核心。** 想通「freq 一次只 +1」之后，
> `min_freq` 就不需要搜索 ⟹ **全部操作 O(1)**。

### ② 淘汰时 `min_freq` 桶的队头就是答案

> `freq_to_keys[min_freq]` 的**第一个** key 就是
> 「使用次数最少、且其中最久未使用」的那个。

因为：桶按 freq 分（次数最少已满足），桶内按插入/提升顺序排（最久未使用在最前）。
⟹ `popitem(last=False)` 一步到位。∎

---

## ⚠️ 四个必须处理的边界（最容易漏的）

| 边界 | 为什么容易错 |
|---|---|
| **`capacity == 0`** | 任何 `put` 都应该**什么都不做**，`get` 恒返回 -1。<br>不特判会在淘汰时对空桶 `popitem` ⟹ `KeyError` |
| **`put` 已存在的 key** | 这是**更新**，不是插入 ⟹ **不能淘汰**，但**要涨 freq** |
| **淘汰后要清理三张表** | `key_to_val`、`key_to_freq`、桶 —— 漏一张就会内存泄漏 / 逻辑错 |
| **空桶要删掉** | 否则 `min_freq` 指向一个存在但为空的桶 ⟹ 淘汰时取不到东西 |

---

## LRU vs LFU（本 Level 1 的核心对照）

| | [LC-0146 LRU Cache](<../../01 - LRU Cache/01 - LC-0146 - LRU Cache>) | **LC-0460 LFU Cache** |
|---|---|---|
| 淘汰谁 | **最久未使用**（时间） | **使用次数最少**（频率），平局时最久未使用 |
| 核心结构 | 1 个双向链表 + 1 个哈希 | **按 freq 分桶**的多个有序结构 + 2 个哈希 |
| 需要额外维护 | 无 | **`min_freq` 指针** + `key -> freq` |
| `get` 做什么 | 把节点**移到头部** | **freq +1 并换桶** |
| Python 偷懒写法 | `OrderedDict.move_to_end` | 无单一容器可用，必须手搓分桶 |
| 复杂度 | **O(1)** 最坏 | **O(1)** 平均（哈希） |

> **LRU 只有「顺序」一个维度；LFU 有「频率」和「顺序」两个维度。**
> 这就是为什么 LFU 要多出一整层桶结构。

---

## 复杂度

| 操作 | 时间 | 说明 |
|---|---|---|
| `get` | **O(1)** 平均 | 两次字典查 + 一次桶迁移 |
| `put`（更新） | **O(1)** 平均 | 同上 |
| `put`（插入 + 淘汰） | **O(1)** 平均 | `popitem(last=False)` 是 O(1) |
| 空间 | **O(capacity)** | 三张表的总大小与 capacity 同阶 |

⚠️ **是「平均 O(1)」而不是「最坏 O(1)」**：底层是哈希表，
最坏情况（全部碰撞）会退化。面试要诚实说「哈希的均摊/平均 O(1)」。
对比 LRU 用双向链表 + 哈希，链表操作本身是**最坏 O(1)**，
只有哈希查找是平均 O(1)。

边界：
  - `capacity = 0` → 所有 `get` 返回 -1，`put` 无效果
  - `capacity = 1` → 每次 `put` 新 key 都淘汰旧的
  - `put` 已存在的 key → 更新值 + freq +1，**不淘汰**
  - freq 平局 → 淘汰**最久未使用**的
  - `get` 不存在的 key → -1，且**不改变任何状态**
  - 淘汰后再 `get` 被淘汰的 key → -1
"""

from collections import OrderedDict, defaultdict


##################################################################################################
##### ! Solution 1: 三张表 + freq 分桶 OrderedDict + min_freq 指针
##### ! 时间复杂度: get / put 均 O(1) 平均   空间复杂度: O(capacity)
##### ! 适用：LFU 的标准实现。核心是「freq 一次只 +1 ⟹ min_freq 不需要搜索」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class LFUCache_1:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.key_to_val = {}                                  # ! key -> value
        self.key_to_freq = {}                                 # ! key -> 使用次数
        self.freq_to_keys = defaultdict(OrderedDict)          # ! freq -> {key: None}，有序
        self.min_freq = 0                                     # ! 当前最小的非空 freq

    def _touch(self, key: int) -> None:
        """把 key 的 freq 从 f 提升到 f+1，并维护 min_freq。"""
        f = self.key_to_freq[key]
        del self.freq_to_keys[f][key]                         # ! 从旧桶摘掉
        if not self.freq_to_keys[f]:
            del self.freq_to_keys[f]                          # ! 空桶必须删掉
            if self.min_freq == f:
                self.min_freq = f + 1                         # ! 规则 B：只会 +1
        self.key_to_freq[key] = f + 1
        self.freq_to_keys[f + 1][key] = None                  # ! 放进新桶的末尾（最新）

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1                                         # ! 不存在 ⟹ 不改变任何状态
        self._touch(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.cap <= 0:
            return                                            # ! capacity == 0 必须特判
        if key in self.key_to_val:
            # ! 已存在 ⟹ 这是更新，不淘汰，但要涨 freq
            self.key_to_val[key] = value
            self._touch(key)
            return
        if len(self.key_to_val) >= self.cap:
            # ! 淘汰 min_freq 桶里最旧的那个
            evict, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]
            del self.key_to_val[evict]                        # ! 三张表都要清
            del self.key_to_freq[evict]
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1                                     # ! 规则 A：新 key 的 freq 是 1


##################################################################################################
##### ! Solution 2: 手搓双向链表版（不依赖 OrderedDict，面试写 Java/C++ 时的形态）
##### ! 时间复杂度: get / put 均 O(1) 平均   空间复杂度: O(capacity)
##### ! 适用：说明 OrderedDict 只是「哈希 + 双向链表」的封装，不是魔法
##################################################################################################


class _Node:
    __slots__ = ("key", "val", "freq", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key, self.val, self.freq = key, val, 1
        self.prev = self.next = None


class _DList:
    """带哨兵的双向链表：头部是最新，尾部是最旧。"""

    def __init__(self):
        self.head, self.tail = _Node(), _Node()
        self.head.next, self.tail.prev = self.tail, self.head
        self.size = 0

    def push_front(self, node: _Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None
        self.size -= 1

    def pop_back(self) -> _Node:
        node = self.tail.prev                                 # ! 尾部 = 最旧
        self.remove(node)
        return node


class LFUCache_2:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.nodes = {}                                       # ! key -> _Node
        self.buckets = defaultdict(_DList)                    # ! freq -> 双向链表
        self.min_freq = 0

    def _touch(self, node: _Node) -> None:
        f = node.freq
        self.buckets[f].remove(node)
        if self.buckets[f].size == 0:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq = f + 1
        node.freq = f + 1
        self.buckets[f + 1].push_front(node)                  # ! 头部 = 最新

    def get(self, key: int) -> int:
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self._touch(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.cap <= 0:
            return
        if key in self.nodes:
            node = self.nodes[key]
            node.val = value
            self._touch(node)
            return
        if len(self.nodes) >= self.cap:
            old = self.buckets[self.min_freq].pop_back()      # ! 最小 freq 桶的尾部
            if self.buckets[self.min_freq].size == 0:
                del self.buckets[self.min_freq]
            del self.nodes[old.key]
        node = _Node(key, value)
        self.nodes[key] = node
        self.buckets[1].push_front(node)
        self.min_freq = 1


##################################################################################################
##### ! Solution 3: 朴素基准（每次扫一遍找 (freq, 插入序) 最小的，用于对拍）
##### ! 时间复杂度: get O(1) / put 淘汰时 O(n)   空间复杂度: O(capacity)
##### ! 适用：仅用于对拍。照定义「次数最少，平局取最久未使用」直接写
##################################################################################################


class LFUCache_3:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.data = {}                                        # ! key -> (value, freq, 最近使用序号)
        self.tick = 0

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        v, f, _ = self.data[key]
        self.tick += 1
        self.data[key] = (v, f + 1, self.tick)
        return v

    def put(self, key: int, value: int) -> None:
        if self.cap <= 0:
            return
        self.tick += 1
        if key in self.data:
            _, f, _ = self.data[key]
            self.data[key] = (value, f + 1, self.tick)
            return
        if len(self.data) >= self.cap:
            # ! 按 (freq 升序, 使用序号升序) 找最该淘汰的
            evict = min(self.data, key=lambda k: (self.data[k][1], self.data[k][2]))
            del self.data[evict]
        self.data[key] = (value, 1, self.tick)


if __name__ == "__main__":
    import random

    for cls in (LFUCache_1, LFUCache_2, LFUCache_3):
        # ! LeetCode 官方样例
        c = cls(2)
        c.put(1, 1)
        c.put(2, 2)
        assert c.get(1) == 1
        c.put(3, 3)                        # ! 淘汰 key 2（freq 1，而 key1 的 freq 是 2）
        assert c.get(2) == -1
        assert c.get(3) == 3
        c.put(4, 4)                        # ! key1 和 key3 的 freq 都是 2 ⟹ 淘汰更旧的 key1
        assert c.get(1) == -1
        assert c.get(3) == 3
        assert c.get(4) == 4

        # ! capacity == 0
        z = cls(0)
        z.put(1, 1)
        assert z.get(1) == -1

        # ! capacity == 1
        o = cls(1)
        o.put(1, 1)
        assert o.get(1) == 1
        o.put(2, 2)
        assert o.get(1) == -1 and o.get(2) == 2

        # ! put 已存在的 key 是更新，不淘汰
        u = cls(2)
        u.put(1, 1)
        u.put(2, 2)
        u.put(1, 100)                      # ! 更新 ⟹ 不该淘汰任何东西
        assert u.get(1) == 100 and u.get(2) == 2

    c = LFUCache_1(2)
    c.put(1, 1); c.put(2, 2)
    print("get(1) =", c.get(1))
    c.put(3, 3)
    print("put(3,3) 后 get(2) =", c.get(2), "(freq 最小的 key 2 被淘汰)")

    for _ in range(3000):                  # ! 随机对拍：三种实现的返回序列必须完全一致
        cap = random.randint(0, 4)
        ops = []
        for _ in range(random.randint(1, 30)):
            if random.random() < 0.45:
                ops.append(("get", random.randint(1, 6), 0))
            else:
                ops.append(("put", random.randint(1, 6), random.randint(1, 100)))
        outs = []
        for cls in (LFUCache_1, LFUCache_2, LFUCache_3):
            c = cls(cap)
            seq = []
            for op, k, v in ops:
                if op == "get":
                    seq.append(c.get(k))
                else:
                    c.put(k, v)
                    seq.append(None)
            outs.append(seq)
        assert outs[0] == outs[1] == outs[2], (cap, ops, outs)
    print("随机对拍 3000 组通过 ✓（freq 桶 OrderedDict == 手搓双向链表 == 朴素 min 基准）")
