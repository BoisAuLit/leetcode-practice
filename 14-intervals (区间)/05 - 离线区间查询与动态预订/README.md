# Level 1 · 05 — 离线区间查询与动态预订（Offline Queries / Lazy Removal / Dynamic Booking）

> **本层的统一目标：区间不再是一次性处理完，而是要反复「被问」或「被加」。**
> 两种模式：**Offline（离线）** —— 所有查询先拿到手，可以重排顺序；
> **Online（在线）** —— 必须立刻回答，无法预知未来。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Offline Query（离线查询）** | 所有查询**事先已知** ⟹ **可以重新排序**，这是本层的核心武器 |
| **Online Query（在线查询）** | 必须立刻回答，无法重排 ⟹ 需要真正的动态数据结构 |
| **Active Interval（活动区间）** | 当前查询点**仍被覆盖**的区间，`start <= q <= end` |
| **Lazy Removal（懒删除）** | 不主动删过期元素，只在**读堆顶时**才把失效的弹掉 |
| **Dynamic Booking** | 在线插入区间，冲突时拒绝；**拒绝不能留下任何痕迹** |

---

## 两个决定性观察

### ① 查询可以重排 —— 这是整个 LC-1851 的钥匙

查询点**无序**时，每个查询都要重新扫一遍所有区间 ⟹ O(n·q)。
但查询**事先全部已知** ⟹ **按坐标升序排好再处理**：
- 区间也按 start 升序，用一个指针单向推进 ⟹ 每个区间**只入堆一次**。
- 查询点右移时，已入堆的区间只会**失效**，不会「重新生效」⟹ 可以放心丢。

最后把答案按**原始下标**写回。
**总复杂度 O((n + q) log n)** —— 而且这是本专题唯一一道「离线」题。

> **记忆点**：看到「for each query」+「可以离线」⟹ **把查询排序**。

### ② 懒删除：不要试图主动维护「当前有效集合」

堆按**区间长度**排序（要最短的），但过期判断用的是**区间的 end**
—— 两个不同的键，没法让堆自动保持有效性。

解决办法：**只在读堆顶时清理**。

```python
while heap and heap[0][1] < q:          # ! heap[0][1] = 该区间的 end
    heapq.heappop(heap)                  # ! 堆顶过期了才弹
ans = heap[0][0] if heap else -1         # ! 清理后堆顶才是答案
```

**⚠️ 这不代表堆里所有元素都有效** —— 堆中间完全可能躺着一堆过期区间。
**正确的不变量只有一条**：

> **回答查询之前，堆顶必须是「当前仍覆盖该查询点」的最短候选区间。**

**为什么只清堆顶就够？**
假设清理后堆顶是 `(len, end)` 且 `end >= q`。
任何堆中更深的元素长度都 `>= len`。
- 若那个更深的元素有效，它也不会比堆顶更优（长度更大）。
- 若它无效，留着也不影响答案。

所以堆顶的 `len` 就是答案，**中间的垃圾不影响正确性**。
而且每个区间**最多被弹一次** ⟹ 总摊还代价 O(n log n)。∎

**为什么过期的区间不会「重新生效」？**
查询点单调右移，而区间的 end 是固定的。
一旦 `end < q`，对后续更大的 `q'` 必然还有 `end < q'` ⟹ **永久失效**。
这正是「查询必须先排序」的理由。∎

---

## 核心不变量

**LC-1851（离线 + 懒删除堆）**：
> 处理查询 `q` 时：
> 1. 所有 `start <= q` 的区间都已入堆（指针单向推进保证）；
> 2. 清理后，堆顶是所有「覆盖 `q`」的区间中**最短**的那个。
>
> 两条合起来 ⟹ 堆顶长度就是答案。

**LC-0729 / LC-0731（在线预订）**：
> 任意时刻，已接受的区间集合满足「任意坐标的覆盖数 `<= LIMIT`」。
> 且 —— **被拒绝的 `book` 调用不改变任何状态**（幂等于未调用）。

---

## 为什么这样排序

| 对象 | 排序键 | 为什么 |
|---|---|---|
| 查询 | **坐标升序**（记下原始下标） | 让区间指针能单向推进，过期区间能永久丢弃 |
| 区间 | **start 升序** | 和查询点同向推进；`start <= q` 的全部入堆 |
| 堆 | **(长度, end)** | 要的是**最短**的覆盖区间 |

> **三个不同的排序键用在三个不同的地方** —— 这是本题比前四层复杂的地方。

---

## ⚠️ 在线预订：半开区间 + 严格不等号

半开区间 `[s, e)` 的相交条件：

```python
s1 < e2 and s2 < e1              # ! 两边都是严格小于
# 等价的「不相交」（更好记）：
e1 <= s2 or e2 <= s1             # ! 「我整个在你前面，或你整个在我前面」
```

**为什么必须严格？** `[10,20)` 的占用是 `10 <= t < 20`，`[20,30)` 是 `20 <= t < 30`
⟹ **没有公共的 `t`** ⟹ 可以背靠背预订。
写成 `<=` 会把 `s2 == e1`（`20 <= 20`）判成冲突 ⟹ **误拒**。

现实类比：10:00–11:00 的会和 11:00–12:00 的会当然可以连着开。

---

## 复杂度必须如实说明（本层的诚实要求）

### LC-1851

**O((n + q) log n)** 时间 —— **不是 O(n log n)**。
`n` 个区间排序 O(n log n) + `q` 个查询排序 O(q log q) +
每个区间最多一次入堆一次出堆 O(n log n) + `q` 次读堆顶。
空间 O(n + q)。

### LC-0729 / LC-0731

| 方案 | 单次 `book` | n 次总计 | 备注 |
|---|---|---|---|
| 线性扫描列表 | **O(n)** | O(n²) | 本题 `n <= 1000` ⟹ **推荐** |
| 有序列表 + `bisect` | 查 O(log n) + **插入 O(n)** | **O(n²)** | 比较次数少了，总体没变 |
| 平衡 BST / Ordered Map | **O(log n)** | O(n log n) | Java `TreeMap`，Python 需 `sortedcontainers` |

> ⚠️ **不能因为调用了 `bisect` 就宣称动态插入是 O(log n)。**
> `bisect.insort` 底层是 `list.insert`，要整体搬移后续元素 ⟹ **O(n)**。
> Python 没有内置平衡树；真要 O(log n) 得用第三方 `SortedList`
> 或自己写 BST / 动态开点线段树。
>
> **对本题给定的有限操作次数（`n <= 1000`），单次 O(n) 检查就是合理且推荐的基础方案。**
> 面试里先写线性扫描，再口述升级路径。

---

## Python 模板

### Template 8：Offline Query + Min Heap（LC-1851）

```python
def minInterval(intervals, queries):
    intervals.sort(key=lambda x: x[0])                 # ! 区间按 start 升序
    order = sorted(range(len(queries)), key=lambda i: queries[i])   # ! 查询按坐标升序
    ans = [-1] * len(queries)
    heap, i = [], 0                                    # ! heap: (长度, end)
    for qi in order:
        q = queries[qi]
        while i < len(intervals) and intervals[i][0] <= q:
            l, r = intervals[i]
            heapq.heappush(heap, (r - l + 1, r))       # ! 闭区间长度 = r-l+1
            i += 1
        while heap and heap[0][1] < q:                 # ! 懒删除：只清堆顶
            heapq.heappop(heap)
        ans[qi] = heap[0][0] if heap else -1           # ! 写回原始下标
    return ans
```
**O((n + q) log n)** 时间、O(n + q) 空间。

### Template 9：Dynamic Booking（LC-0729）

```python
class MyCalendar:
    def __init__(self):
        self.booked = []
    def book(self, s, e):
        for bs, be in self.booked:
            if s < be and bs < e:                      # ! 半开 ⟹ 严格小于
                return False                           # ! 拒绝，不改任何状态
        self.booked.append((s, e))
        return True
```
单次 **O(n)**、空间 O(n)。

### Template 9'：上限推广到 k（LC-0731）

```python
class MyCalendarTwo:
    def __init__(self):
        self.booked, self.overlaps = [], []
    def book(self, s, e):
        for os, oe in self.overlaps:                   # ! ① 先全量检查，不修改
            if s < oe and os < e:
                return False                           # ! 会变三重 ⟹ 拒绝
        for bs, be in self.booked:                     # ! ② 确认接受后才记录新二重段
            lo, hi = max(s, bs), min(e, be)
            if lo < hi:
                self.overlaps.append((lo, hi))
        self.booked.append((s, e))
        return True
```
**⚠️ 检查必须在修改之前全部做完** —— 边检查边写 `overlaps`，
一旦后面要拒绝，状态就脏了。**这是本题最容易写出的 bug。**

### 差分 map（上限可配，直通 LC-0732）

```python
class MyCalendarK:
    LIMIT = 2                                          # ! 改成 1 就是 729，改成 k 就是 k 重
    def __init__(self):
        self.delta = defaultdict(int)
    def book(self, s, e):
        self.delta[s] += 1; self.delta[e] -= 1         # ! 先试加
        cur = 0
        for x in sorted(self.delta):
            cur += self.delta[x]
            if cur > self.LIMIT:
                self.delta[s] -= 1; self.delta[e] += 1 # ! 超了就回滚
                return False
        return True
```
单次 **O(n log n)**（排序 map），胜在**改上限只要改一个数字**。

---

## 代表题目

| # | 题 | 优先级 | 模式 | 端点 | 数据结构 |
|---|---|---|---|---|---|
| 1 | [LC-1851 Minimum Interval to Include Each Query](<./01 - 最短覆盖区间的离线查询/01 - LC-1851 - Minimum Interval to Include Each Query>) | **P0** | **Offline** | 闭 | 懒删除 Min Heap |
| 2 | [LC-0729 My Calendar I](<./02 - 在线插入与区间冲突检测/01 - LC-0729 - My Calendar I>) | P1 | **Online** | **半开** | 列表 / BST |
| 3 | [LC-0731 My Calendar II](<./02 - 在线插入与区间冲突检测/02 - LC-0731 - My Calendar II>) | P1+ | **Online** | **半开** | 双列表 / 差分 map |

---

## 典型边界情况

| 边界 | 例子 | 期望 |
|---|---|---|
| 查询点正好在端点上 | `intervals=[[1,4]], queries=[1,4]` | `[4,4]`（闭区间，两端都算覆盖） |
| 查询点无任何覆盖 | `intervals=[[2,3]], queries=[1]` | `[-1]` |
| 完全包含 | `intervals=[[1,10],[2,3]], queries=[2]` | `[2]`（取**更短**的 `[2,3]`） |
| 完全相同的区间 | `intervals=[[1,2],[1,2]], queries=[1]` | `[2]` |
| 空区间列表 | `intervals=[], queries=[1]` | `[-1]` |
| 完全无重叠 | `intervals=[[1,2],[5,6]], queries=[3]` | `[-1]` |
| 查询**乱序** | `queries=[5,1,3]` | 必须按原始下标写回 |
| 端点相接（半开） | `book(10,20)` 后 `book(20,30)` | **`True`** |
| 完全相同 | `book(10,20)` 后 `book(10,20)` | `False` |
| 被包含 | `book(10,20)` 后 `book(12,15)` | `False` |
| 包含对方 | `book(10,20)` 后 `book(5,30)` | `False` |
| **拒绝后状态不脏** | 上一行 False 后再 `book(20,30)` | **`True`** |
| LC-0731 三次同区间 | `book(1,5)` ×3 | `True, True, False` |

---

## 错误策略反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| LC-1851 查询**不排序** | — | O(n·q)，大数据 TLE |
| LC-1851 试图主动维护「有效集合」 | — | 堆按长度排、过期按 end 判，两个键无法同步 |
| LC-1851 认为「堆里所有元素都有效」 | — | 概念错误；中间确实有垃圾，只保证**清理后的堆顶**有效 |
| LC-1851 答案按**排序后**顺序返回 | `queries=[5,1,3]` | 顺序全错，必须按原始下标写回 |
| LC-1851 长度算成 `r - l` | `[[1,4]], q=1` | 得 3，正确 4（闭区间是 `r-l+1`） |
| LC-0729 用 `s <= be and bs <= e` | `book(10,20)` 后 `book(20,30)` | 误拒（半开区间端点相接不冲突） |
| LC-0729 先插入再检查 | — | 拒绝时状态已脏 |
| LC-0731 边检查边写 `overlaps` | 后续需要拒绝的用例 | 状态被污染，后面全错 |
| 声称 `bisect` 让插入变 O(log n) | — | `list.insert` 是 O(n)，总体仍 O(n²) |
| 为了 O(log n) 硬上线段树 | `n <= 1000` | 过度设计；O(n) 单次完全够用 |

---

## 相邻 Pattern 对比

| | [Level 1 · 04](<../04 - 重叠计数、扫描线与资源分配>) | **本层（05）** |
|---|---|---|
| 处理方式 | **一次扫完** | **反复查询 / 反复插入** |
| Heap 里存什么 | 区间的 **end**（为了复用资源） | 区间的**长度 + end**（为了回答查询） |
| 需要懒删除？ | ❌（堆顶过期就直接 replace） | ✅（两个排序键无法同步） |
| 查询 | 无 | 有（离线可重排 / 在线不可） |
| 输出 | 一个计数 / 一条数组 | **每个查询一个答案** / 每次插入一个 bool |

**和 Level 04 的衔接**：
- 04 的 Heap：按 end 排序，堆顶过期就 `heapreplace` ⟹ **堆里永远全是有效元素**。
- 05 的 Heap：按长度排序，过期判断看 end ⟹ **必须懒删除**，堆里有垃圾。

**同一个 `heapq`，两种完全不同的不变量。** 这是本层最该带走的认识。

**跨专题血缘**：
- 懒删除堆的套路 = `09-heap` 的「两个堆 + 懒删除」（LC-0480 Sliding Window Median）
- 在线数据结构设计 = `17-design` 专题
- LC-0731 的差分 map 解法 = Level 04 的 [LC-1094 Car Pooling](<../04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/01 - LC-1094 - Car Pooling>) 的在线版本

---

## 相关资料

- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q10 / Q11
- [Endpoint Semantics Cheat Sheet](<../_resources/endpoint-semantics-cheat-sheet.md>) — 半开区间的严格不等号
- [Interval Algorithm Comparison Table](<../_resources/interval-algorithm-comparison.md>) — 模板 8 / 9
- [P0 / P1 / P2 Roadmap](<../_resources/p0-p1-p2-roadmap.md>)
