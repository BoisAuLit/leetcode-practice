# Level 1 · 03 — Randomized Data Structures（随机化数据结构）

> **本层的统一目标：同时做到 O(1) 插入、O(1) 删除、O(1) 均匀随机访问。**
> 三个要求互相冲突 —— 解法是**紧凑数组 + 字典**，外加一个叫 **swap-with-last** 的技巧。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Compact Array（紧凑数组）** | 下标 `0..n-1` 全部有效、**没有空洞**的数组 |
| **swap-with-last** | 删除时把目标元素与**末尾**交换，再 `pop()` ⟹ O(1) 且保持紧凑 |
| **Index Map（下标表）** | `val -> 它在数组中的位置`；允许重复时变成 `val -> 下标集合` |
| **Weighted Uniform Random** | 按出现次数加权的均匀随机（重复元素被选中的概率更高） |

---

## 两个决定性观察

### ① 三个要求互相冲突，所以必须用两个结构

| 要求 | 单用数组 | 单用哈希集合 |
|---|---|---|
| `insert` O(1) | ✅ `append` | ✅ |
| `remove` O(1) | ❌ `list.remove` 是 **O(n)**（要搬移） | ✅ |
| `getRandom` 均匀 O(1) | ✅ `arr[randrange(n)]` | ❌ **set 不支持按下标随机访问** |

**数组会随机但不会删，集合会删但不会随机** ⟹ **两个一起用**：

```python
self.arr = []        # ! 紧凑数组 —— 只为 getRandom 存在
self.idx = {}        # ! val -> 下标 —— 只为 O(1) 定位存在
```

### ② swap-with-last：把 O(n) 删除变成 O(1)

```python
i = self.idx[val]
last = self.arr[-1]
self.arr[i] = last          # ! 把最后一个搬进坑 i
self.idx[last] = i          # ! 更新它的下标
self.arr.pop()              # ! O(1)（只有对末尾 pop 才是 O(1)）
del self.idx[val]
```

**为什么必须和「最后一个」交换？**
`list.pop()` 只有对**末尾**才是 O(1)（中间 pop 要搬移后面所有元素）。
把要删的挪到末尾 ⟹ 数组保持**紧凑**（无空洞）
⟹ `getRandom` 的 `randrange(len(arr))` 仍然均匀且 O(1)。

**代价**：**元素顺序被打乱**。本题不关心顺序 ⟹ 免费。
（如果题目要求保序，这个技巧就不能用。）

---

## 核心不变量

> 1. **`arr` 始终紧凑**：下标 `0 .. len(arr)-1` 每一个都放着一个有效元素。
> 2. **`idx` 与 `arr` 始终一致**：
>    - 不许重复时：`arr[idx[v]] == v`
>    - 允许重复时：`idx[v]` 恰好等于 `{i : arr[i] == v}`
> 3. **空集合必须从 `idx` 里删掉 key**（允许重复的版本）。

**不变量 1 保证 `getRandom` 均匀；不变量 2 保证 `remove` 能 O(1) 定位。**

---

## 为什么 getRandom 是均匀的（证明）

`arr` 紧凑 ⟹ 每个**元素实例**恰好占一个下标，共 `n` 个下标。
`random.randrange(n)` 以 `1/n` 的概率选中每个下标
⟹ 值 `v` 被返回的概率 = `count(v) / n`。

- **LC-0380（不许重复）**：每个值 `count == 1` ⟹ 概率都是 `1/n`。
- **LC-0381（允许重复）**：概率与出现次数成正比 —— **这正是题目要的**。∎

> **这就是为什么数组必须紧凑**：有空洞的话要么概率不均，要么得重试。

---

## ⚠️ 允许重复之后，坑全在「下标表」

| | [LC-0380](<./01 - O(1) 插入、删除与均匀随机访问/01 - LC-0380 - Insert Delete GetRandom O(1) (学习索引 · 实体在 01-arrays-hashing)>) | [LC-0381](<./01 - O(1) 插入、删除与均匀随机访问/02 - LC-0381 - Insert Delete GetRandom O(1) - Duplicates allowed>) |
|---|---|---|
| 下标表 | `val -> 一个 int` | `val -> 一个 **set**` |
| `remove` 取下标 | 直接读 | 从 set 里**任取一个**（`set.pop()` 是 O(1)） |
| 交换后要更新 | 1 个条目 | **2 个条目**（被删的 + 被搬来的） |
| 空集合 | 不存在 | **必须 `del` 掉 key** |
| `getRandom` 概率 | 每个值 `1/n` | **按出现次数加权** |

### 三步的顺序是唯一正确的那一种

```python
i = self.idx[val].pop()                      # ! ① 先从 val 的集合里摘掉下标 i
last = self.arr[-1]
self.arr[i] = last
self.idx[last].add(i)                        # ! ② 再把 i 记到 last 名下
self.idx[last].discard(len(self.arr) - 1)    # ! ③ last 不再占用原末尾下标
self.arr.pop()
```

**当 `val == last` 时，`idx[val]` 和 `idx[last]` 是同一个 set**，
三步作用在同一个集合上，净效果必须是「**去掉末尾下标，保留 i**」：

| 顺序 | `arr=[5,5]`、`idx[5]={0,1}`、`i=0` | 对吗 |
|---|---|---|
| **① pop(i) → ② add(i) → ③ discard(tail)** | `{1}` → `{0,1}` → `{0}` | ✅ `arr=[5]`，下标 0 有效 |
| ① add(i) → ② discard(i) → ③ discard(tail) | `{0,1}` → `{1}` → `{}` | ❌ 集合空了，但 `arr[0]` 还有个 5 |

> **第二行是本次实现最初写错的顺序** —— 官方样例和手写边界用例**全部通过**，
> 只有**随机操作序列对拍**抓到了它（`remove(5)` 两次时第二次返回 `False`）。
> 这就是为什么设计题必须做序列级别的随机对拍。

### 空集合必须删 key

`insert` 的返回值是「插入前是否**不**含 val」，判断依据是 `val in self.idx`。
用 `defaultdict(set)` 时**读取就会建一个空 set** ⟹ 不删 key 的话
`val in self.idx` 会对一个「已全部删除」的 val 返回 True ⟹ **返回值错**。

---

## Python 核心模板

```python
class RandomizedSet:                 # LC-0380（不许重复）
    def __init__(self):
        self.arr, self.idx = [], {}

    def insert(self, val):
        if val in self.idx: return False
        self.idx[val] = len(self.arr); self.arr.append(val); return True

    def remove(self, val):
        if val not in self.idx: return False
        i, last = self.idx[val], self.arr[-1]
        self.arr[i] = last; self.idx[last] = i      # ! swap-with-last
        self.arr.pop(); del self.idx[val]           # ! val == last 时顺序敏感
        return True

    def getRandom(self):
        return self.arr[random.randrange(len(self.arr))]
```

```python
class RandomizedCollection:          # LC-0381（允许重复）
    def __init__(self):
        self.arr, self.idx = [], defaultdict(set)

    def insert(self, val):
        had = bool(self.idx.get(val))
        self.idx[val].add(len(self.arr)); self.arr.append(val)
        return not had                              # ! 插入前是否不含 val

    def remove(self, val):
        if not self.idx.get(val):
            self.idx.pop(val, None); return False
        i = self.idx[val].pop()                     # ! ①
        last = self.arr[-1]
        self.arr[i] = last
        self.idx[last].add(i)                       # ! ②
        self.idx[last].discard(len(self.arr) - 1)   # ! ③
        self.arr.pop()
        if not self.idx[val]: del self.idx[val]     # ! 空集合必须删 key
        if last in self.idx and not self.idx[last]: del self.idx[last]
        return True
```

---

## 时间与空间复杂度

| 操作 | LC-0380 | LC-0381 | 说明 |
|---|---|---|---|
| `insert` | **O(1) 平均** | **O(1) 平均** | 哈希写 |
| `remove` | **O(1) 平均** | **O(1) 平均** | `set.pop()` 是 O(1) |
| `getRandom` | **O(1) 最坏** | **O(1) 最坏** | 纯数组访问，**不碰哈希** |
| 空间 | **O(n)** | **O(n)** | 数组 + 下标表 |

⚠️ `getRandom` 是本专题里**少数真正的「最坏 O(1)」** —— 值得在面试里点出来。
⚠️ `next(iter(a_set))` / `set.pop()` 都是 **O(1)**（只碰第一个桶），不是 O(k)。

---

## 代表题目

| # | 题 | 优先级 | 允许重复 | 核心 |
|---|---|---|---|---|
| 1 | [LC-0380 Insert Delete GetRandom O(1)](<./01 - O(1) 插入、删除与均匀随机访问/01 - LC-0380 - Insert Delete GetRandom O(1) (学习索引 · 实体在 01-arrays-hashing)>) ↗️ | **P0** | ❌ | 数组 + 字典 + swap-with-last |
| 2 | [LC-0381 … Duplicates allowed](<./01 - O(1) 插入、删除与均匀随机访问/02 - LC-0381 - Insert Delete GetRandom O(1) - Duplicates allowed>) ★ | P1 | ✅ | 下标变**集合** + 顺序陷阱 |

↗️ **LC-0380 的实体在 `01-arrays-hashing`**（Primary Pattern 是 Array + Hash Map，
它更早入库）⟹ 本层只放学习索引（含完整模板和证明）。
★ 第二轮审核新增。

**学习顺序**：**先把 LC-0380 练到肌肉记忆，再做 LC-0381** ——
指令也这么说：「LC-381 是 LC-380 的进阶变体，应先掌握 LC-380」。

---

## 典型边界情况

| 边界 | 期望 |
|---|---|
| `remove` 不存在的元素 | `False`，**不改变任何状态** |
| `insert` 重复元素（LC-0381） | **`False`**（插入前已含有），但**确实要插进去** |
| 删到一个都不剩 | **必须删掉 `idx` 里的 key** |
| **`val == arr[-1]`**（要删的正好是末尾元素的值） | 顺序陷阱，见上面的对照表 |
| `i == len(arr) - 1`（要删的就在末尾） | 自赋值无害，**不需要 if 特判** |
| 全部元素相同 `[1,1,1]` | `getRandom` 恒返回 1 |
| 空集合上 `remove` | `False` |
| 只有一个元素时 `remove` 它 | 数组变空，`idx` 清空 |
| 加权随机的分布 | `[1,2,2,2]` ⟹ 1 的概率应 ≈ 0.25（本题用 40000 次抽样验证） |

---

## 典型反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| 用 `list.remove(val)` | 大 n | **O(n)** 搬移 ⟹ 不满足要求 ❌ |
| 删除时留下空洞（不 swap） | 任意 | `getRandom` 可能取到空洞 ⟹ 概率不均 / 要重试 ❌ |
| swap 后忘记更新 `idx[last]` | `remove` 非末尾元素 | 下标表指向错误位置 ⟹ 后续全错 ❌ |
| LC-0380 中 `val == last` 时先写 `idx[last]=i` 再 `del idx[val]` | `remove` 末尾元素 | 把刚写的条目删掉 ⟹ 死条目 ❌ |
| **LC-0381 用 add-then-discard 的顺序** | `insert(5);insert(5);remove(5);remove(5)` | 第二次返回 `False` ❌（**随机对拍抓到的真实 bug**） |
| LC-0381 空集合不删 key | 删光后再 `insert` | 返回 `False`（应为 `True`）❌ |
| 用 `set` 代替数组 | 任意 | **无法 O(1) 均匀随机**（set 不支持下标）❌ |
| 为了保序而不用 swap-with-last | 任意 | 删除退化成 O(n) ⚠️ |

---

## 容易混淆的 Pattern

### `x & (x-1)` 式的「清掉最低位」不在这里 —— 别和位运算混

本层的 swap-with-last 是**数组技巧**，和 `16-bit-manipulation` 的位技巧无关。

### 紧凑数组 vs 逻辑删除

| | **swap-with-last**（本层） | **逻辑删除**（LC-1472） |
|---|---|---|
| 数组内容 | 保持**紧凑**（真的移动元素） | 保留旧内容，只缩「有效长度」 |
| 顺序 | **被打乱** | 保持 |
| 适用 | 不关心顺序 + 要随机访问 | **关心顺序**（前进/后退） |

**两个都是 O(1)「删除」，但代价不同** —— 选哪个取决于要不要保序。

### 和 Level 1 · 02 的「两结构组合」同源

| 题 | 管顺序/随机 | 管定位 |
|---|---|---|
| **LC-0380 / 0381** | **紧凑数组** | `val -> 下标(集合)` |
| LC-0146 LRU | 双向链表 | `key -> node` |
| LC-0460 LFU | 频率桶 | `key -> val` / `key -> freq` |

---

## 相关资料

- [设计题通用清单](<../_resources/design-checklist.md>) — swap-with-last + Stateful API 怎么测
- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q4


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-0528 Random Pick with Weight](<./02 - 加权随机、蓄水池采样与洗牌/01 - LC-0528 - Random Pick with Weight>) | `03 - Randomized Data Structures/02 - 加权随机、蓄水池采样与洗牌` | 前缀和 + 二分：权重铺在数轴上，随机数落在哪段就选哪个；randint(1,total) 配 bisect_left | 随机 / 采样族的入口 |
| [LC-0382 Linked List Random Node](<./02 - 加权随机、蓄水池采样与洗牌/02 - LC-0382 - Linked List Random Node>) | `03 - Randomized Data Structures/02 - 加权随机、蓄水池采样与洗牌` | 蓄水池采样 k=1：第 i 个以 1/i 概率替换，P=1/n 的约分证明要能口述 | 流式 / 长度未知 |
| [LC-0398 Random Pick Index](<./02 - 加权随机、蓄水池采样与洗牌/03 - LC-0398 - Random Pick Index>) | `03 - Randomized Data Structures/02 - 加权随机、蓄水池采样与洗牌` | 对「等于 target 的下标」这条子流做蓄水池采样；哈希表版 O(1) pick 是空间换时间 | LC-0382 同算法 |
| [LC-0384 Shuffle an Array](<./02 - 加权随机、蓄水池采样与洗牌/04 - LC-0384 - Shuffle an Array>) | `03 - Randomized Data Structures/02 - 加权随机、蓄水池采样与洗牌` | Fisher–Yates：j ∈ [0, i] 而不是 [0, n-1]；文件里用 χ² 把错误写法的 4/27 vs 5/27 偏差量化出来 | n! 条等概率路径 |
| [LC-0470 Implement Rand10() Using Rand7()](<./02 - 加权随机、蓄水池采样与洗牌/05 - LC-0470 - Implement Rand10() Using Rand7()>) | `03 - Randomized Data Structures/02 - 加权随机、蓄水池采样与洗牌` | 拒绝采样：7×7=49 格留 40，期望 2.45 次；回收 41..49 当 rand9 可降到 2.19 | 均匀性只能来自乘法组合 + 拒绝 |

### 本次新开的 Level 2

- **02 - 加权随机、蓄水池采样与洗牌** — 原来这一层只有「O(1) 插入删除 + 均匀随机」一个 Level 2；加权随机、蓄水池采样、Fisher–Yates、拒绝采样是大厂（Meta / Google）常年考的另一半，之前全库 0 道，所以新开一层把五道放在一起：它们共用「怎样证明分布是均匀的」这一个问题。

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
