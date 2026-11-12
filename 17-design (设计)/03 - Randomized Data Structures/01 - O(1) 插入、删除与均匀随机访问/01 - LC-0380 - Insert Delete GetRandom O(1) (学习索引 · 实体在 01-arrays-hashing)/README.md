# LC-0380 - Insert Delete GetRandom O(1)（学习索引）

> ⚠️ **这里没有 `solution.py` / `metadata.json` / PDF，只有这份索引。**
> 本仓库铁律：**一道题只能有一个实体文件夹**，否则复习队列会重复叫号。

**👉 实体位置：**
[01-arrays-hashing (数组、哈希表)/01 - Hash Set 与 Hash Map 基础/08 - LC-0380 - Insert Delete GetRandom O(1)](<../../../../01-arrays-hashing (数组、哈希表)/01 - Hash Set 与 Hash Map 基础/08 - LC-0380 - Insert Delete GetRandom O(1)>)

| 字段 | 值 |
|---|---|
| **Primary Pattern** | **Array + Hash Map**（这是它归在 `01-arrays-hashing` 的理由） |
| **Secondary Patterns** | Randomized O(1) Operations、**swap-with-last**、Data Structure Design |
| **Recommended Algorithm** | 紧凑数组 + `val -> 下标` 字典；删除时与**最后一个**元素交换再 `pop` |
| **Alternative Algorithm** | 无更优方案（这是最优解） |
| **Cross-topic Reference** | 本专题 Level 1 · 03 / Level 2 · 01（与 LC-0381 配对） |

---

## 为什么它在本专题里占一个位置

它是 **Randomized Data Structures 这一层的奠基题** ——
不把它列出来，[LC-0381](<../02 - LC-0381 - Insert Delete GetRandom O(1) - Duplicates allowed>)
（允许重复的进阶版）就没有起点。
指令也明确：**已有完整主归属 ⟹ 建立跨专题索引，避免无意义的重复生成。**

---

## 核心：三个要求互相冲突，所以必须用两个结构

| 要求 | 单用数组 | 单用哈希集合 |
|---|---|---|
| `insert` O(1) | ✅ append | ✅ |
| `remove` O(1) | ❌ `list.remove` 是 O(n) | ✅ |
| `getRandom` 均匀 O(1) | ✅ `arr[randrange(n)]` | ❌ **set 不支持按下标随机访问** |

**单独任何一个都不够** ⟹ 两个一起用：

```python
self.arr = []        # ! 紧凑数组（无空洞）—— 只为 getRandom 存在
self.idx = {}        # ! val -> 它在 arr 中的下标 —— 只为 O(1) 定位存在
```

### swap-with-last：把 O(n) 删除变成 O(1)

```python
def remove(self, val):
    if val not in self.idx:
        return False
    i = self.idx[val]
    last = self.arr[-1]
    self.arr[i] = last          # ! 把最后一个元素搬进坑 i
    self.idx[last] = i          # ! 更新它的下标
    self.arr.pop()              # ! O(1)
    del self.idx[val]
    return True
```

**为什么必须和「最后一个」交换？**
因为 `pop()` 只有对**末尾**才是 O(1)。
把要删的元素挪到末尾 ⟹ 数组保持**紧凑**（没有空洞）
⟹ `getRandom` 的 `randrange(len(arr))` 仍然均匀且 O(1)。

**代价**：元素顺序被打乱。本题不关心顺序，所以免费。

### ⚠️ 两个顺序陷阱

```python
self.arr[i] = last
self.idx[last] = i          # ! 必须在 del self.idx[val] 之前或之后都行…
self.arr.pop()
del self.idx[val]           # ! …但若 val == last，这一行会把刚写的 idx[last] 删掉！
```

**当 `val == last`（要删的正好是最后一个元素）时**：
`self.idx[last] = i` 和 `del self.idx[val]` 操作的是**同一个 key**
⟹ 顺序写反就会留下一个指向已 pop 位置的死条目。

**最稳的写法是先删再写，或者显式特判 `i == len(arr) - 1`。**
（LC-0381 的下标**集合**版把这个陷阱放大了一层 —— 见那道题的「坑 ②」对照表。）

---

## getRandom 的均匀性证明

`arr` 是紧凑的（下标 `0 .. n-1` 全部有效，且每个元素恰好占一个位置）
⟹ `random.randrange(n)` 以 `1/n` 的概率选中每个下标
⟹ 每个元素被返回的概率都是 `1/n`。∎

**这就是为什么数组必须紧凑** —— 有空洞的话要么概率不均，要么得重试。

---

## 复杂度

| 操作 | 时间 | 说明 |
|---|---|---|
| `insert` | **O(1)** 平均 | append + 一次字典写 |
| `remove` | **O(1)** 平均 | swap + pop + 两次字典操作 |
| `getRandom` | **O(1)** **最坏** | 纯数组下标访问，不碰哈希 |
| 空间 | **O(n)** | 数组 + 字典 |

⚠️ `insert` / `remove` 是**平均** O(1)（哈希表），
只有 `getRandom` 是**最坏** O(1)。面试要诚实区分。

---

## 和 LC-0381 的对照（本 Level 2 的学习路径）

| | **LC-0380** 本题 | [LC-0381](<../02 - LC-0381 - Insert Delete GetRandom O(1) - Duplicates allowed>) |
|---|---|---|
| 允许重复 | ❌ | ✅ |
| 下标表 | `val -> 一个 int` | `val -> 一个 **set**` |
| `remove` 取下标 | 直接读 | 从 set 里**任取一个** |
| 空集合 | 不存在 | **必须删 key**，否则 `insert` 返回值错 |
| `getRandom` 概率 | 每个值 `1/n` | **按出现次数加权** |

**先把 LC-0380 练到肌肉记忆，再做 LC-0381** ——
指令也这么说：「LC-381 是 LC-380 允许重复元素的进阶变体，应先掌握 LC-380」。

---

## 和本专题其他设计题的共同主题

| 题 | 用两个结构解决什么冲突 |
|---|---|
| **LC-0380** | 数组给随机访问，字典给 O(1) 定位 |
| [LC-0146 LRU Cache](<../../../02 - Cache 与 O(1) 淘汰策略/01 - LRU Cache/01 - LC-0146 - LRU Cache>) | 双向链表给 O(1) 移动，字典给 O(1) 定位 |
| [LC-0460 LFU Cache](<../../../02 - Cache 与 O(1) 淘汰策略/02 - LFU Cache 与频率桶/01 - LC-0460 - LFU Cache>) | 频率桶给 O(1) 淘汰，两张字典给 O(1) 定位 |

> **设计题的通用套路：**
> **单一数据结构做不到的事，用「一个负责顺序/随机、一个负责定位」的组合做到。**
> 字典几乎总是那个「负责定位」的角色。
