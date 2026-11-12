# Level 1 · 01 — Hash Structures 与稀疏数据设计（Hash Structures / Sparse Representation）

> **本层的统一目标：理解哈希表的内部构造，以及「只存有用的东西」这件事。**
> 这是整个 Design 专题的地基 —— 后面每一层都要用字典做「O(1) 定位」。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Separate Chaining（链地址法）** | 固定数量的桶，每桶挂一条链表；碰撞的 key 挂在同一桶里 |
| **Hash Collision（哈希碰撞）** | 两个不同 key 落到同一个桶 |
| **Load Factor（装载因子）** | `元素数 / 桶数`，决定链的平均长度 |
| **Sparse Representation（稀疏表示）** | 只存非零项，不存整个向量 |

---

## 两个决定性观察

### ① 哈希表 = 「数组给 O(1) 随机访问」+ 「链表处理碰撞」

```python
self.buckets = [[] for _ in range(769)]       # ! 769 是质数
def _idx(self, key):
    return hash(key) % len(self.buckets)
```

**为什么桶数要选质数？**
若桶数是 `2^k`，`hash(key) % 2^k` 等于**只取 hash 的低 k 位** ——
而很多哈希函数的低位分布不如高位均匀（例如整数 key 直接用自身当 hash
时，所有偶数会挤在偶数桶）。
**质数**让取模用上 hash 的全部位 ⟹ 分布更均匀。

**为什么链表长度决定复杂度？**
- 查找一个 key：定位桶 O(1) + **遍历该桶的链** O(链长)
- 平均链长 = **装载因子** `n / buckets`
⟹ 装载因子为常数时，操作是 **O(1) 平均**；
   最坏情况（全部碰撞到一个桶）退化成 **O(n)**。

> **这就是为什么本专题后面所有「O(1)」都要说「平均 O(1)」。**
> 字典不是魔法，它是「数组 + 链表 + 一个好的哈希函数」。

### ② 稀疏数据：**只存非零项**，而且求内积要用**双指针**

一个长度 `10^5` 的向量里只有 3 个非零 ⟹ 存整个数组是 `10^5` 的浪费。

```python
self.pairs = [(i, v) for i, v in enumerate(nums) if v]    # ! 只存非零，按下标升序
```

**求内积为什么用双指针而不是字典查找？**

| 做法 | 时间 | 说明 |
|---|---|---|
| 遍历较短的一方，在另一方的**字典**里查 | **O(min(k1, k2))** 平均 | 需要哈希，常数更大 |
| **双指针**同步扫两个有序列表 | **O(k1 + k2)** 最坏 | 纯数组访问，**无哈希开销** |

两者都远优于 O(n)。双指针的好处是**最坏情况也有保证**，
而且和 [14-intervals 的双指针求交集](<../../14-intervals (区间)/02 - 双指针区间交集与多路合并/01 - 两个有序区间序列求交集/01 - LC-0986 - Interval List Intersections (学习索引 · 实体在 02-two-pointers)>)
是同一个骨架：**下标小的那边前进**。

```python
i = j = 0
total = 0
while i < len(a) and j < len(b):
    if a[i][0] == b[j][0]:
        total += a[i][1] * b[j][1]; i += 1; j += 1
    elif a[i][0] < b[j][0]:
        i += 1                      # ! 只有一边非零 ⟹ 乘积是 0，跳过
    else:
        j += 1
```

---

## 核心不变量

**Separate Chaining**：
> `buckets[_idx(key)]` 恒包含**所有**哈希到该桶的 key-value 对，
> 且同一个 key 在整张表里**最多出现一次**。

**Sparse Vector**：
> `self.pairs` 恒为「所有非零项」按**下标升序**排列，
> 未出现的下标其值**必然为 0**。

**双指针内积**：
> 任意时刻，`a[0..i-1]` 和 `b[0..j-1]` 中所有「下标相同」的配对都已累加完毕。

---

## 为什么用这些结构

### 为什么 `put` 要先查再改（而不是直接 append）？

```python
for k, (ek, ev) in enumerate(bucket):
    if ek == key:
        bucket[k] = (key, value)       # ! 已存在 ⟹ 更新
        return
bucket.append((key, value))             # ! 不存在 ⟹ 追加
```
不先查就直接 append ⟹ 同一个 key 在桶里出现**两次**
⟹ `get` 取到旧值、`remove` 只删一个 ⟹ **不变量被破坏**。

### 为什么 `remove` 用 swap-with-last 或 `del`？

桶内顺序无关 ⟹ 可以 swap-with-last（O(1)）。
但桶很短（平均 O(1) 个元素），`list.remove` 的 O(链长) 也是 O(1) 平均
⟹ **本题两种都行**，不必过度优化。
（真正需要 swap-with-last 的是 [Level 1 · 03](<../03 - Randomized Data Structures>) 的大数组。）

---

## 简短正确性证明

### 为什么装载因子为常数时操作是 O(1) 平均

假设哈希函数把 `n` 个 key **均匀**散布到 `m` 个桶
⟹ 每个桶的期望元素数是 `n/m`（装载因子 `α`）。
一次操作 = 定位桶 O(1) + 遍历链 O(α)
⟹ 当 `α = O(1)` 时，总共 **O(1) 平均**。∎

**最坏情况**：所有 key 碰撞到一个桶 ⟹ 链长 `n` ⟹ **O(n)**。
（真实的 Python `dict` 用开放寻址 + 动态扩容把 `α` 维持在 2/3 以下。）

### 为什么稀疏内积只需扫非零项

内积 `Σ a[i] * b[i]`。
若 `a[i] == 0` 或 `b[i] == 0`，该项贡献为 **0** ⟹ 可以跳过。
所以只需考虑「**两边都非零**」的下标 ⟹ 扫两个非零列表的交集即可。∎

---

## Python 核心模板

### Separate Chaining（LC-0705 / LC-0706）

```python
class MyHashMap:
    def __init__(self):
        self.size = 769                      # ! 质数，降低碰撞聚集
        self.buckets = [[] for _ in range(self.size)]

    def _idx(self, key):
        return key % self.size               # ! 整数 key 直接取模

    def put(self, key, value):
        b = self.buckets[self._idx(key)]
        for i, (k, _) in enumerate(b):
            if k == key:
                b[i] = (key, value); return  # ! 已存在 ⟹ 更新（不能 append）
        b.append((key, value))

    def get(self, key):
        for k, v in self.buckets[self._idx(key)]:
            if k == key:
                return v
        return -1                            # ! 不存在的哨兵值

    def remove(self, key):
        b = self.buckets[self._idx(key)]
        for i, (k, _) in enumerate(b):
            if k == key:
                b.pop(i); return
```
**O(1) 平均**（装载因子为常数时）、**O(size + n)** 空间。

### 稀疏向量 + 双指针内积（LC-1570）

```python
class SparseVector:
    def __init__(self, nums):
        self.pairs = [(i, v) for i, v in enumerate(nums) if v]   # ! 只存非零

    def dotProduct(self, vec):
        a, b = self.pairs, vec.pairs
        i = j = total = 0
        while i < len(a) and j < len(b):
            if a[i][0] == b[j][0]:
                total += a[i][1] * b[j][1]; i += 1; j += 1
            elif a[i][0] < b[j][0]:
                i += 1                        # ! 下标小的那边前进
            else:
                j += 1
        return total
```
构造 **O(n)**、内积 **O(k1 + k2)**、空间 **O(k)**（`k` = 非零个数）。

---

## 时间与空间复杂度

| 题 | 操作 | 时间 | 空间 |
|---|---|---|---|
| LC-0705 Design HashSet | add / contains / remove | **O(1) 平均**，最坏 O(n) | O(size + n) |
| LC-0706 Design HashMap | put / get / remove | **O(1) 平均**，最坏 O(n) | O(size + n) |
| LC-1570 Sparse Vector | 构造 | **O(n)** | **O(k)** |
| | dotProduct | **O(k1 + k2)** | O(1) |

⚠️ **哈希表是「平均 O(1)」，不是「最坏 O(1)」** —— 这是本层最该带走的认识。

---

## 代表题目

| # | 题 | 优先级 | 核心 |
|---|---|---|---|
| 1 | [LC-0705 Design HashSet](<./01 - HashSet 与 HashMap 基础实现/01 - LC-0705 - Design HashSet>) | P1 | Separate Chaining |
| 2 | [LC-0706 Design HashMap](<./01 - HashSet 与 HashMap 基础实现/02 - LC-0706 - Design HashMap>) | P1 | Separate Chaining（存 KV） |
| 3 | [LC-1570 Dot Product of Two Sparse Vectors](<./02 - Sparse Representation 与高效内积/01 - LC-1570 - Dot Product of Two Sparse Vectors>) | **P0** | 只存非零 + 双指针 |

⚠️ **LC-1570 是 LeetCode Premium 题目**（本仓库已有完整的原始资料，全部保留）。

---

## 典型边界情况

| 边界 | 期望 |
|---|---|
| `get` 不存在的 key | 返回 **-1**（不是抛异常） |
| `remove` 不存在的 key | **no-op**，不改变任何状态 |
| `put` 已存在的 key | **更新**，桶里不能出现两份 |
| 大量碰撞（如 key 都是 `769 * i`） | 功能仍对，但退化成 O(n) |
| key = 0 / key 为负数（若题目允许） | 取模要注意 Python 的负数取模 |
| 稀疏向量**全是 0** | `pairs` 为空 ⟹ 内积 0 |
| 两个稀疏向量**无公共非零下标** | 内积 0（双指针不会累加任何项） |
| 稀疏向量**完全不稀疏** | 退化成 O(n)，但仍正确 |
| 自己和自己做内积 | 等于各项平方和 |

---

## 典型反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| `put` 不先查就 append | `put(1,1); put(1,2)` | 桶里两份 key 1 ⟹ `get` 可能取到旧值 ❌ |
| 桶数用 `2^k`（如 1024） | key 都是偶数 | 全挤在偶数桶 ⟹ 严重碰撞 ⚠️ |
| 声称哈希表是「最坏 O(1)」 | — | 面试会被追问；应说「平均 O(1)」❌ |
| 稀疏向量存整个数组 | `n = 10^5`，3 个非零 | 空间 O(n) 而非 O(k) ⚠️ |
| 稀疏内积用「遍历 n 个下标」 | 同上 | O(n) 而非 O(k1+k2) ⚠️ |
| 双指针两边都自增（不管下标） | 下标不对齐的向量 | 配错项 ❌ |
| `pairs` 没按下标排序 | — | 双指针前提被破坏 ❌ |

---

## 容易混淆的 Pattern

### Separate Chaining vs Open Addressing

| | **链地址法**（本层） | 开放寻址（Python `dict` 的做法） |
|---|---|---|
| 碰撞处理 | 挂在同一桶的链上 | 探测下一个空位 |
| 删除 | 直接从链里删 | 需要**墓碑标记**（不能直接清空，否则探测链断裂） |
| 缓存友好 | 差（链表跳指针） | 好（连续数组） |
| 实现难度 | **简单**（面试首选） | 中（墓碑 + 扩容很绕） |

LeetCode 的 LC-0705 / LC-0706 **只要求链地址法**。

### 稀疏表示的两种形态

| | `(下标, 值)` **有序列表** | `下标 -> 值` **字典** |
|---|---|---|
| 内积 | **双指针 O(k1+k2)** 最坏 | 遍历短的那个 + 查另一个，O(min) **平均** |
| 需要有序 | ✅ | ❌ |
| 常数 | 更小（无哈希） | 更大 |
| 随机单点查询 | O(log k) 二分 | **O(1) 平均** |

**选哪个取决于主要操作**：只做内积 ⟹ 有序列表；要频繁单点查 ⟹ 字典。

---

## 相邻 Pattern 对比

| | **本层（01）** | [Level 1 · 02](<../02 - Cache 与 O(1) 淘汰策略>) | [Level 1 · 03](<../03 - Randomized Data Structures>) |
|---|---|---|---|
| 字典的角色 | **它本身就是被实现的对象** | O(1) **定位**（配合链表） | O(1) **定位**（配合数组） |
| 另一个结构 | 链表（处理碰撞） | **双向链表**（管顺序） | **紧凑数组**（管随机访问） |
| 要解决的冲突 | 随机访问 vs 碰撞 | O(1) 查找 vs O(1) 顺序调整 | O(1) 删除 vs 均匀随机 |

> **本层把字典拆开给你看；后面几层把字典当积木用。**
> 先理解「它只是数组 + 链表」，后面所有「O(1) 平均」的说法才站得住。

---

## 相关资料

- [设计题通用清单](<../_resources/design-checklist.md>) — 开场五步 + 六个套路 + 复杂度用词
- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q1 / Q13
