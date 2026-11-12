# 09 · Heap / Priority Queue（堆、优先队列）

> 堆只做**一件事**：**O(log n) 维护「当前最优」**。
> 它**不能**做的事同样重要：不能查任意元素、不能查前驱后继、不能按区间查询。
> 本专题所有题都是在回答：**「最优」怎么定义，以及堆里该放什么。**

本专题共 **26 道题** + 2 条跨专题索引，7 个 Level 1。

## 一、Python heapq 的三个必知点

```python
heapq.heapify(lst)          # O(n) 原地建堆 —— 比逐个 push 的 O(n log n) 好
heapq.heappushpop(h, x)     # 先 push 再 pop，比分开调用快
heapq.heapreplace(h, x)     # 先 pop 再 push（堆必须非空）
```

1. **只有最小堆**。要最大堆就**把值取负**（`heappush(h, -x)`）。
   值是字符串时没法取负 ⟹ 需要包装类（见 LC-0692）。
2. **元组按字典序比较**。所以 `(priority, tie_breaker, payload)` 要保证
   **payload 永远比不到** —— 否则遇到不可比较的对象（如 ListNode）会 `TypeError`。
   常用 tie-breaker：下标 `i` 或 `id(obj)`。
3. **堆不支持删除任意元素** ⟹ 需要 **Lazy Deletion**（见 LC-0480、LC-3408）。

## 二、目录地图

| Level 1 | 主题 | 题数 | README |
|---|---|---|---|
| 01 | Heap 基础与 Top K | 5 | [→](<01 - Heap 基础与 Top K/README.md>) |
| 02 | K-way Merge 与候选扩展 | 3 | [→](<02 - K-way Merge 与候选扩展/README.md>) |
| 03 | Two Heaps 与动态中位数 | 2 | [→](<03 - Two Heaps 与动态中位数/README.md>) |
| 04 | Heap + Greedy 资源优化与选择 | 6 | [→](<04 - Heap + Greedy 资源优化与选择/README.md>) |
| 05 | Heap + Scheduling 任务调度 | 3 + 1 索引 | [→](<05 - Heap + Scheduling 任务调度/README.md>) |
| 06 | Heap + Hash Map 数据结构设计 | 2 | [→](<06 - Heap + Hash Map 数据结构设计/README.md>) |
| 07 | 跨专题与低优先级存档 | 2 | [→](<07 - 跨专题与低优先级存档/README.md>) |

```
01 Heap 基础与 Top K/
  01 基础 Heap 与反复取极值/     01 LC-1046(NC→)
  02 Kth Largest 与固定大小 Heap/ 01 LC-0703(NC→) 02 LC-0215(NC→) 03 LC-0973(NC→)
  03 Top K Frequency 与 Tie Breaking/ 01 LC-0692←新    （LC-0347 跨专题索引）
02 K-way Merge 与候选扩展/
  01 多路有序序列合并/           01 LC-0378        （LC-0023 跨专题索引）
  02 有序候选集合的按需扩展/     01 LC-0373←新
  03 多路指针与覆盖区间/         01 LC-0632←新₂
03 Two Heaps 与动态中位数/
  01 动态中位数与双堆平衡/       01 LC-0295
  02 窗口中位数与 Lazy Deletion/ 01 LC-0480←新₂
04 Heap + Greedy 资源优化与选择/
  01 Optimal Merge Pattern/      01 LC-1167
  02 有限资源的最优分配/         01 LC-1642
  03 频率重排与边际收益/         01 LC-0767  02 LC-1792
  04 排序与 Heap 的组合选择/     01 LC-0502←新  02 LC-2542←新
05 Heap + Scheduling 任务调度/
  01 Frequency Scheduling/       01 LC-0621(NC→)
  02 动态任务与事件优先级/       01 LC-1834←新  02 LC-2402←新   （LC-1353 跨专题索引 → 13-greedy）
06 Heap + Hash Map 数据结构设计/
  01 社交信息流与多路合并/       01 LC-0355(NC→)
  02 动态优先级与 Lazy Deletion/ 01 LC-3408
07 跨专题与低优先级存档/         01 LC-1337  02 LC-2817
_resources/ introduction/（7 份堆入门资料）top-k-theory/（11 份 Top-K 讲义）utils/（3 张图）
```

## 三、六个核心模板

**T1 · Top K（大小为 k 的堆）**
```python
heap = []
for x in items:
    heapq.heappush(heap, x)      # 求 Top-K 大 → 最小堆；求 Top-K 小 → 最大堆（取负）
    if len(heap) > k:
        heapq.heappop(heap)      # 弹掉「最差」的那个
```
O(n log k) 时间、O(k) 空间。
**什么时候反而该全量建堆**：k 接近 n 时，`heapify` + 弹 k 次是 O(n + k log n)，更优。

**T2 · K-way Merge（每路只放一个候选）**
```python
heap = [(每路的第一个, 路编号, 路内下标) for 每一路]
heapq.heapify(heap)
while heap:
    val, i, j = heapq.heappop(heap)
    使用 val
    if 该路还有下一个:
        heapq.heappush(heap, (下一个, i, j+1))
```
**绝不要把所有候选一次性入堆** —— 这是 LC-0373 的核心（否则 10¹⁰ 个数对）。

**T3 · Two Heaps（动态中位数）**
```python
small  # 最大堆（存负），较小的一半
large  # 最小堆，较大的一半
不变量：len(small) == len(large) 或 len(small) == len(large) + 1
中位数：奇数 → small 顶；偶数 → (small 顶 + large 顶) / 2
```

**T4 · 排序 + 堆（两个维度分工）**
```python
按维度 A 排序          # 用来「解锁」或「枚举边界」
维度 B 进堆            # 用来「选最优」或「踢最差」
```
复用：LC-0502（capital 排序 / profit 最大堆）、LC-2542（nums2 降序 / nums1 最小堆）、
LC-1834（enqueueTime 排序 / processingTime 最小堆）。

**T5 · 事件驱动调度（时间跳跃）**
```python
while 还有任务:
    把所有 到达时间 <= now 的任务入堆
    if 堆空: now = 下一个任务的到达时间      # ★ 跳跃，不要逐秒推进
    else:    取堆顶执行, now += 耗时
```

**T6 · Lazy Deletion（惰性删除）**
```python
to_delete[x] += 1                 # 不真删，只记账
while heap and to_delete[heap[0]] > 0:   # 等它浮到堆顶再真删
    to_delete[heap[0]] -= 1
    heapq.heappop(heap)
```
**代价**：`len(heap)` 不再等于有效元素数 ⟹ 必须**另外维护逻辑 size**。
**陷阱**（LC-0480 实测踩到）：两个堆都可能含同一个值时，
删除标记必须**分边记**，否则会被错误的那一边消费掉。

| 模板 | 时间 | 空间 |
|---|---|---|
| T1 Top-K | O(n log k) | O(k) |
| T2 K-way Merge | O(N log k) | O(k) |
| T3 Two Heaps | 每次 O(log n) | O(n) |
| T4 排序 + 堆 | O(n log n + n log k) | O(k) |
| T5 事件调度 | O(n log n) | O(n) |
| T6 Lazy Deletion | 摊还 O(log n) | O(n) |

## 四、堆**不能**做什么（Level 1 `07` 存在的理由）

| 需求 | 堆能做吗 | 该用什么 |
|---|---|---|
| 取全局最小 / 最大 | **能**，O(log n) | 堆 |
| 查任意元素是否存在 | **不能** | Hash Set |
| 查「最接近 x 的元素」/ 前驱后继 | **不能** | **Ordered Set / 平衡 BST / SortedList** |
| 按区间查询 | **不能** | 线段树 / 树状数组 |
| 删除任意元素 | **不能直接删** | Lazy Deletion（T6） |

**LC-2817** 就是典型：它要在动态集合里找「最接近当前元素的数」，
这是 **predecessor / successor 查询**，堆给不了 —— 必须用 Ordered Set 或二分 + 有序结构。
它被放进存档区正是因为**它不是堆题**。

**LC-1337** 则相反：它能用堆，但「算每行士兵数 + 按 `(count, index)` 排序」更简单直接。
**不要因为题目能用堆就用堆。**

## 五、P0 / P1 / P2

**P0** LC-1046、LC-0703、LC-0215、LC-0973、LC-0295、LC-0621、LC-0355、LC-0767
**P1** LC-0692、LC-0378、LC-0373、LC-1167、LC-1642、LC-0502、LC-2542、LC-1834、LC-1353、LC-2402、LC-3408
**P2** LC-1792、LC-0480、LC-0632、LC-1337、LC-2817

### 推荐学习顺序
```
A 基础取极值   1046 → 703 → 215 → 973 → 692
B K-way Merge  378 → 373 → 632          （023 见 06-linked-list）
C 双堆         295 → 480
D 贪心 + 堆    1167 → 1642 → 767 → 1792 → 502 → 2542
E 调度         621 → 1834 → 1353 → 2402
F 设计         355 → 3408
G 存档         1337 → 2817
```

## 六、跨专题索引

| LC | 关系 | 实体目录 |
|---|---|---|
| LC-0347 Top K Frequent Elements | 和 LC-0692 同族，但**无 tie-breaking** ⟹ 可以 Bucket Sort 做到 O(n) | [01-arrays-hashing](<../01-arrays-hashing (数组、哈希表)/>) |
| LC-0023 Merge k Sorted Lists | K-way Merge 的链表版 | [06-linked-list](<../06-linked-list (链表)/04 - 链表归并与排序/02 - K 条有序链表归并/01 - LC-0023 - Merge k Sorted Lists>) |
| LC-0253 Meeting Rooms II | 「最少几个房间」，只需一个堆；对比本专题 LC-2402 | [14-intervals](<../14-intervals (区间)/>) |
| LC-1353 Maximum Events | Primary Pattern 是 **Greedy (EDF)**，堆只是加速器 | [13-greedy](<../13-greedy (贪心)/04 - 区间调度与有序集合/01 - 最早截止时间优先/01 - LC-1353 - Maximum Number of Events That Can Be Attended>)（补充解法已并入那份 solution.py） |
| LC-0378 | 也可以**值域二分 + 计数** | **实体目录在本专题**；[05-binary-search 的 `03/04`](<../05-binary-search (二分查找)/03 - 二分答案与可行性判断 (Binary Search on Answer)/04 - 值域二分与计数可行性/README.md>) 只建索引，二分解法已并入本专题的 solution.py |

## 七、NC / LC 处理结果

6 个 NC 来源**全部是孤儿**（仓库里没有对应 LC 目录），按规则**升格**，
`practice` 原样保留，solution.py 一字未改：

| 原 NC | 升格为 | practice |
|---|---|---|
| NC - Last Stone Weight | LC-1046 | 0 条 |
| NC - Kth Largest Element in a Stream | LC-0703 | 0 条 |
| NC - Kth Largest Element in an Array | LC-0215 | 0 条 |
| NC - K Closest Points to Origin | LC-0973 | 0 条 |
| NC - Task Scheduler | LC-0621 | 0 条 |
| NC - Design Twitter | LC-0355 | **保留 2 条** |

**没有 LC / NC 重复，因此没有删除任何目录。**

## 八、第二轮独立审核结果

**自主新增 2 道**：

| 题 | Pattern | 为什么值得加 |
|---|---|---|
| **LC-0480** Sliding Window Median | 双堆 + **Lazy Deletion** | LC-0295 只加不删；窗口一滑动就要「删堆中间的任意元素」，而堆**做不到**。这逼出 Lazy Deletion 这个通用技巧（LC-3408 也用它）。实测还暴露了一个隐蔽陷阱：重复值跨越中位线时，**删除标记必须分边记** |
| **LC-0632** Smallest Range Covering K Lists | k 路指针 + **堆管下界、变量管上界** | LC-0378/0373 只关心堆顶（弹第 t 小）。本题要同时盯住「当前最小（堆顶）」和「当前最大（外部变量）」，是 k-way merge 的另一个用法 |

**审核过、决定不加（Future Candidates）**

| 题 | 理由 |
|---|---|
| LC-0857 / LC-2462 Hire K Workers | 和新增的 LC-2542 都是「排序一个维度 + 堆维护 Top-K 和」，技能点重合 |
| LC-0253 Meeting Rooms II | 14-intervals 已有实体目录；而且它比 LC-2402 简单，被后者覆盖 |
| LC-0347 Top K Frequent Elements | 01-arrays-hashing 已有；无 tie-breaking，最优解是 Bucket Sort 而不是堆 |

## 九、原有资料与修复
- `introduction (堆入门)`（7 份）、`top-k (Top K)` 下的 11 份讲义和
  `kth-largest-smallest` 子目录、`utils`（3 张图）全部搬到 [`_resources/`](<_resources>)，**内容未改**。
- **修复了 1 个原本跑不起来的文件**：`LC-0355 - Design Twitter` 底部有一行
  `print(twitter.followedBy)`，引用了类里并不存在的属性，导致整个文件 `AttributeError`。
  已注释掉那一行并写明原因，**没有改动任何解法代码**。
- **LC-0378 的重复已修复**：本次重构早期我误以为仓库里没有 LC-0378，
  在 05-binary-search 新建了一份。发现后已把那份的「值域二分 + 阶梯计数」解法
  **并入本专题这道题的 solution.py**（用户原有的堆解法保留为 `Solution_0`），
  并删除了 05 的重复目录，改为索引 README。现在全仓库只有一个 LC-0378 实体目录。
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`。

完整校验见 [_audit/post-migration-report.md](<_audit/post-migration-report.md>)。
