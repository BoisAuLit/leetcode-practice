# Level 1 · 02 — Cache 与 O(1) 淘汰策略（Cache Eviction in O(1)）

> **本层的统一目标：在 O(1) 时间内「找到该淘汰谁」并「把它踢掉」。**
> 两道题的区别只有一个：**按什么排序**（时间 vs 频率）。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **LRU（Least Recently Used）** | 淘汰**最久未使用**的 —— 只有「时间」一个维度 |
| **LFU（Least Frequently Used）** | 淘汰**使用次数最少**的；次数相同时淘汰最久未使用的 —— **两个维度** |
| **Doubly Linked List（双向链表）** | O(1) 的「摘除任意节点」和「插入头部」 |
| **Frequency Bucket（频率桶）** | `freq -> 该频率下的所有 key`（桶内保持 LRU 顺序） |

---

## 三个决定性观察

### ① 单一数据结构做不到，必须「链表管顺序 + 字典管定位」

| 要求 | 单用链表 | 单用字典 |
|---|---|---|
| O(1) 找到某个 key | ❌ 要遍历 O(n) | ✅ |
| O(1) 把它移到头部 | ✅（已知节点指针时） | ❌ 字典没有顺序 |
| O(1) 找到最旧的 | ✅ 尾部 | ❌ |

**两个一起用**：字典存 `key -> 节点指针`，链表存顺序。
```python
self.cache = {}                    # ! key -> node
self.head, self.tail = Node(), Node()   # ! 哨兵：head.next 最新，tail.prev 最旧
```

**为什么要用双向链表而不是单向？**
摘除节点 `x` 需要改 `x.prev.next`。
单向链表拿不到 `x.prev` ⟹ 只能从头遍历 ⟹ **O(n)**。
**双向链表让「已知节点指针 ⟹ O(1) 摘除」成立** —— 这是整个 LRU 的支点。

**为什么要用哨兵（dummy head / tail）？**
没有哨兵的话，「在头部插入」「删除尾部」「链表为空」要写三套 if。
有哨兵之后**永远不会碰到 None** ⟹ 插入删除各只有 4 行，**零特判**。

### ② LFU 比 LRU 多一个维度，所以多一整层桶

**LRU 只有「顺序」** ⟹ 一条链表就够。
**LFU 有「频率」和「顺序」两个维度** ⟹ **每个频率一条链表**（频率桶）。

```python
self.key_to_val  = {}                        # ! key -> value
self.key_to_freq = {}                        # ! key -> 使用次数
self.freq_to_keys = defaultdict(OrderedDict) # ! freq -> {key: None}，桶内保持 LRU 顺序
self.min_freq = 0                            # ! 当前最小的非空 freq
```

### ③ `min_freq` 不需要搜索 —— 因为 **freq 一次只 +1**

```
规则 A：put 一个新 key               ⟹  min_freq = 1
规则 B：把某 key 从 freq f 提到 f+1 后，
        若桶 f 空了且 f == min_freq  ⟹  min_freq += 1
```

**为什么规则 B 里 `min_freq` 只会 +1，不会跳更多？**
被提升的那个 key 现在在桶 `f+1` 里 ⟹ **桶 `f+1` 必然非空**
⟹ 新的最小非空 freq 不可能大于 `f+1`。∎

**为什么规则 A 直接设成 1 就对？**
新 key 的 freq 是 1，而 freq 的最小可能值就是 1 ⟹ 立刻是全局最小。∎

> **这两条规则是 LFU 的全部难点。**
> 想通「freq 一次只 +1」之后，`min_freq` 就不用搜索 ⟹ 所有操作 O(1)。

---

## 核心不变量

**LRU**：
> 链表从 `head.next` 到 `tail.prev` 是**按最近使用时间降序**排列的全部 key，
> 且 `cache[key]` 恒指向链表中那个 key 对应的节点。

**LFU**：
> 1. `freq_to_keys[f]` 恒为「当前使用次数恰为 `f`」的全部 key，桶内按**最久未使用在前**排列。
> 2. `min_freq` 恒为所有**非空**桶的最小键。
> 3. 三张表的 key 集合**始终一致**（`key_to_val`、`key_to_freq`、所有桶的并集）。

**淘汰时的推论**：
> `freq_to_keys[min_freq]` 的**第一个** key 就是
> 「次数最少、其中最久未使用」的那个 ⟹ `popitem(last=False)` 一步到位。

---

## 为什么 `get` 也要改状态

**两题的 `get` 都不是只读的**：
- LRU：命中 ⟹ 把节点**移到头部**（刷新「最近使用」）
- LFU：命中 ⟹ **freq +1 并换桶**

**未命中则必须完全不改状态** ——
返回 -1，不插入、不改 freq、不动链表。这是最常被忽略的语义。

---

## 简短正确性证明

### LRU 的淘汰永远是「最久未使用」

**不变量**：每次 `get` / `put` 命中都把该节点移到头部
⟹ 链表顺序 = 最近使用时间的降序。
⟹ `tail.prev` 恒为最久未使用的节点。∎

### LFU 的 `min_freq` 恒正确

初始时表为空，`min_freq` 无意义（不会被用到，因为淘汰只在表满时发生）。
归纳：
- **插入新 key**：它的 freq 是 1，而所有 freq `>= 1` ⟹ `min_freq = 1` 正确。
- **提升某 key 的 freq**（`f -> f+1`）：
  - 若桶 `f` 仍非空 ⟹ 最小非空 freq 不变 ⟹ 不动 `min_freq` 正确。
  - 若桶 `f` 空了且 `f != min_freq` ⟹ `min_freq` 对应的桶仍非空 ⟹ 不变正确。
  - 若桶 `f` 空了且 `f == min_freq` ⟹ 原来的最小桶没了；
    而桶 `f+1` 必然非空（刚放进去一个）⟹ 新的最小是 `f+1` ⟹ `+= 1` 正确。
- **淘汰**：从 `min_freq` 桶弹出一个；若桶空了，下一次插入会把 `min_freq` 重设为 1。∎

---

## Python 核心模板

### LRU（手搓双向链表版 —— 面试写 Java/C++ 的形态）

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}                                  # ! key -> node
        self.head, self.tail = Node(), Node()            # ! 哨兵，零特判
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):                             # ! O(1)（双向链表的支点）
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node):
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = self.head.next = node

    def get(self, key):
        if key not in self.cache:
            return -1                                    # ! 未命中 ⟹ 完全不改状态
        node = self.cache[key]
        self._remove(node); self._add_front(node)        # ! 刷新"最近使用"
        return node.val

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]; node.val = value
            self._remove(node); self._add_front(node)
            return                                        # ! 更新 ⟹ 不淘汰
        if len(self.cache) >= self.cap:
            old = self.tail.prev                          # ! 尾部 = 最久未使用
            self._remove(old); del self.cache[old.key]
        node = Node(); node.key, node.val = key, value
        self.cache[key] = node; self._add_front(node)
```

**Python 偷懒版**：`OrderedDict` + `move_to_end(key)` / `popitem(last=False)`。

### LFU（频率桶 + min_freq）

```python
def _touch(self, key):                                   # ! freq 从 f 提到 f+1
    f = self.key_to_freq[key]
    del self.freq_to_keys[f][key]
    if not self.freq_to_keys[f]:
        del self.freq_to_keys[f]                         # ! 空桶必须删
        if self.min_freq == f:
            self.min_freq = f + 1                        # ! 规则 B：只会 +1
    self.key_to_freq[key] = f + 1
    self.freq_to_keys[f + 1][key] = None                 # ! 放进新桶末尾（最新）

def put(self, key, value):
    if self.cap <= 0: return                             # ! capacity == 0 必须特判
    if key in self.key_to_val:
        self.key_to_val[key] = value; self._touch(key); return
    if len(self.key_to_val) >= self.cap:
        evict, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
        if not self.freq_to_keys[self.min_freq]:
            del self.freq_to_keys[self.min_freq]
        del self.key_to_val[evict]; del self.key_to_freq[evict]   # ! 三张表都要清
    self.key_to_val[key] = value
    self.key_to_freq[key] = 1
    self.freq_to_keys[1][key] = None
    self.min_freq = 1                                    # ! 规则 A
```

---

## 时间与空间复杂度

| 题 | get | put | 空间 | 备注 |
|---|---|---|---|---|
| LC-0146 LRU | **O(1)** | **O(1)** | O(capacity) | 链表操作是**最坏** O(1)；字典查找是平均 O(1) |
| LC-0460 LFU | **O(1) 平均** | **O(1) 平均** | O(capacity) | 多一层桶，但 `popitem(last=False)` 仍是 O(1) |

⚠️ 诚实说法：「**O(1) 平均**，因为底层是哈希表；
双向链表/OrderedDict 的调整本身是最坏 O(1)」。

---

## 代表题目

| # | 题 | 优先级 | 淘汰依据 | 核心结构 |
|---|---|---|---|---|
| 1 | [LC-0146 LRU Cache](<./01 - LRU Cache/01 - LC-0146 - LRU Cache>) | **P0** | **时间** | 双向链表 + 字典 |
| 2 | [LC-0460 LFU Cache](<./02 - LFU Cache 与频率桶/01 - LC-0460 - LFU Cache>) ★ | P1 | **频率**（平局按时间） | 频率桶 + `min_freq` + 两张字典 |

★ 第一轮新增。
LC-0146 的实体在本专题（曾与 `06-linked-list` 的副本冲突，已去重，本专题是主归属）。

---

## 典型边界情况

| 边界 | 期望 | 为什么容易错 |
|---|---|---|
| **`capacity == 0`** | `put` 无效果，`get` 恒 -1 | 不特判会在空桶/空链表上淘汰 ⟹ 崩溃 |
| **`capacity == 1`** | 每次 put 新 key 都淘汰旧的 | — |
| **`put` 已存在的 key** | **更新**，**不淘汰** | 当成插入会误删一个 key |
| `get` 不存在的 key | -1，**不改变任何状态** | 容易顺手插入一个空项 |
| 淘汰后再 `get` 被淘汰的 key | -1 | 三张表没清干净会返回脏数据 |
| LFU **freq 平局** | 淘汰**最久未使用**的 | 用 `set` 当桶就没有顺序 ⟹ 平局乱选 |
| LFU 桶**变空** | 必须 `del` 掉这个 freq | 留着空桶 ⟹ `min_freq` 指向空桶 ⟹ 淘汰时取不到 |
| 反复 `get` 同一个 key | LRU：顺序不变；LFU：freq 一直涨 | — |
| 先填满再全部 `get` 一遍再 put | 淘汰的应该是**第一个被 get 的** | 测「顺序刷新」是否生效 |

---

## 典型反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| 用**单向**链表 | 任意 | 摘除节点要 O(n) 找前驱 ❌ |
| 不用哨兵节点 | 链表空 / 只有一个节点 | 一堆 `None` 判空分支，容易漏 ⚠️ |
| LRU 的 `get` 不刷新顺序 | `put(1);put(2);get(1);put(3)` | 淘汰了 1，正确应淘汰 2 ❌ |
| `put` 已存在的 key 时触发淘汰 | `cap=2; put(1);put(2);put(1,9)` | 误删一个 key ❌ |
| LFU 桶用 `set` | freq 平局 | 没有顺序 ⟹ 平局时乱选 ❌ |
| LFU 空桶不删 | 淘汰后 | `min_freq` 指向空桶 ⟹ `popitem` 抛 `KeyError` ❌ |
| LFU 淘汰时只清 `key_to_val` | 任意 | `key_to_freq` 残留 ⟹ 该 key 再插入时 freq 不是 1 ❌ |
| LFU 用堆按 freq 排序 | 任意 | freq 会变，堆里是陈旧键 ⟹ 要懒删除，而且是 O(log n) ⚠️ |
| 不特判 `capacity == 0` | `LFUCache(0); put(1,1)` | 淘汰时对空桶操作 ⟹ 崩溃 ❌ |
| 声称是「最坏 O(1)」 | — | 字典是平均 O(1) ⚠️ |

---

## 容易混淆的 Pattern

### LRU vs LFU（本层的核心对照）

| | **LRU** | **LFU** |
|---|---|---|
| 维度 | **一个**（时间） | **两个**（频率 + 时间） |
| 结构 | 1 条双向链表 + 1 张字典 | **按 freq 分桶** + 2 张字典 + `min_freq` |
| `get` 做什么 | 移到头部 | **freq +1 并换桶** |
| 淘汰谁 | 链表尾部 | `min_freq` 桶的**队头** |
| Python 偷懒 | `OrderedDict.move_to_end` | **没有单一容器**，必须手搓 |
| 难点 | 双向链表的指针操作 | **`min_freq` 的维护** |

### 和 Level 1 · 03 的「两结构组合」是同一思想

| 题 | 管顺序/随机的结构 | 管定位的结构 |
|---|---|---|
| LC-0146 LRU | 双向链表 | `key -> node` |
| LC-0460 LFU | 频率桶（桶内有序） | `key -> val` + `key -> freq` |
| [LC-0380 GetRandom](<../03 - Randomized Data Structures/01 - O(1) 插入、删除与均匀随机访问/01 - LC-0380 - Insert Delete GetRandom O(1) (学习索引 · 实体在 01-arrays-hashing)>) | **紧凑数组** | `val -> 下标` |

> **字典几乎总是那个「负责定位」的角色。**
> 变的只是另一半：链表（要顺序）、数组（要随机）、桶（要分组）。

---

## 相关资料

- [设计题通用清单](<../_resources/design-checklist.md>) — 两结构组合 + 通用边界清单
- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q2 / Q3
