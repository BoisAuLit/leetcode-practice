# Level 1 · 03 Floyd 环检测与隐式函数图

> **Floyd's Cycle Detection（龟兔赛跑）和 Floyd-Warshall（全源最短路）是完全不同的两个算法**，
> 只是碰巧同一个人姓 Floyd。不要混。

## 核心定义
一个**确定性的后继函数** `next(x)` 反复作用在一个**有限状态集**上，
序列必然进入循环（鸽巢原理）。Floyd 用两个不同速度的指针，
在 O(1) 额外空间内找出「有没有环」和「环从哪里开始」。

## 决定性观察

### 为什么快慢指针一定会相遇
进入环之后，快指针每轮比慢指针多走 1 步，
它们的距离每轮减少 1，所以**一定会在有限步内重合**（距离不会跳过 0）。
这也是为什么必须是 1 步 vs 2 步 —— 速度差恰好是 1。

### 为什么第二阶段能找到环入口（必须会推）
设：起点到环入口距离 `a`，环入口到相遇点距离 `b`，相遇点回到环入口距离 `c`（环长 `L = b + c`）。

相遇时：
- 慢指针走了 `a + b`
- 快指针走了 `a + b + kL`（k ≥ 1，多绕了 k 圈）
- 快是慢的两倍：`2(a + b) = a + b + kL`
  ⟹ `a + b = kL`
  ⟹ `a = kL - b = (k-1)L + c`

**`a = (k-1)L + c`** 的含义：从 head 走 `a` 步到环入口，
和从相遇点走 `c` 步（再绕 k-1 圈）到环入口，**步数相同**。
所以让一个指针从 head、一个从相遇点，**都每次一步**，它们会在环入口相遇。∎

```python
slow = fast = head
while fast and fast.next:
    slow, fast = slow.next, fast.next.next
    if slow is fast:                      # 有环
        p = head
        while p is not slow:
            p, slow = p.next, slow.next
        return p                          # 环入口
return None                               # fast 走到 None = 无环
```

### 隐式函数图（本章最有价值的迁移）
只要能写出一个**确定性的 `next(x)`**，就能用同一套 Floyd，哪怕根本没有链表：

| 题 | 状态是什么 | `next(x)` 是什么 |
|---|---|---|
| LC-0141/0142 | 链表节点 | `node.next` |
| LC-0202 Happy Number | 一个正整数 | 各位数字的平方和 |
| LC-0287 Find the Duplicate | 下标 | `nums[i]` |
| LC-0457 Circular Array Loop | 下标 | `(i + nums[i]) % n` |

**LC-0287 的精妙之处**：数组有 n+1 个数、值域是 `[1, n]`，
所以 `i -> nums[i]` 这个函数图里**一定有环**，而**环的入口就是重复的那个数**
（因为它被至少两个不同的下标指向，是唯一的「汇合点」）。
这样就能在**不修改数组、O(1) 额外空间**下解决 —— 这正是题目的两个硬约束。

## 题目

| # | 题 | 优先级 | 独有的东西 |
|---|---|---|---|
| 01/01 | LC-0141 Linked List Cycle | P0 | 判环；终止条件 `fast and fast.next` |
| 01/02 | LC-0142 Linked List Cycle II | P0 | 找环入口；必须会推 `a = (k-1)L + c` |
| 02/01 | LC-0202 Happy Number | P1 | 状态是整数，`next` 是数位平方和；也可以用 set |
| 02/02 | LC-0457 Circular Array Loop | P2 | 最复杂的变体，见下 |
| — | LC-0287 Find the Duplicate Number | P0 | **跨专题索引** → [01-arrays-hashing](<../../01-arrays-hashing (数组、哈希表)/04 - Array Index Mapping 与 In-place Marking/04 - LC-0287 - Find the Duplicate Number>) |

## LC-0457 为什么标 P2
它要同时处理四件事，每一件都容易错：
- **方向必须一致**：整个环里的 `nums[i]` 必须同号，中途变号就不算合法环。
- **环长必须 > 1**：`nums[i] % n == 0` 的自环要排除。
- **下标取模要处理负数**：Python 的 `%` 对负数返回非负，这点正好有利，但在别的语言要小心。
- **多起点**：要对每个起点都试一次，并把走过的无效路径标记掉以免重复扫描。

它是环检测的综合应用，**不需要为它单独记一套模板** —— 理解前面三道就够了。

## 常见错误
- 终止条件写成 `while fast.next and fast` ⟹ `fast` 为 None 时崩。
- LC-0142 第二阶段让两个指针速度不同 ⟹ 推导不成立，找不到入口。
- 把 Floyd Cycle Detection 和 Floyd-Warshall 搞混。
- LC-0202 不用 Floyd 而用 set 也完全正确（O(n) 空间），
  面试里应该先说 set、再给 Floyd 作为 O(1) 空间的改进。

## 复习时的 Pattern Recognition
> 「链表有没有环 / 环从哪开始」
> 「反复应用一个固定函数，会不会循环」
> 「数组里找唯一重复的数，不能改数组、只能 O(1) 空间」
> → Floyd。先写出 `next(x)`，剩下的就是模板。
