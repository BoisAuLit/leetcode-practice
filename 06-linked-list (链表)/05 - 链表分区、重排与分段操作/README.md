# Level 1 · 05 链表分区、重排与分段操作

## 核心定义
把一条链**拆开**、**重排**、**再接回去**。
共同骨架只有一个：**多条子链各带一个 dummy 和一个 tail，最后拼接。**

## 决定性观察

### 通用骨架（LC-0086 / LC-0328 完全共用）
```python
d1 = t1 = ListNode(); d2 = t2 = ListNode()
cur = head
while cur:
    if 分组条件: t1.next = cur; t1 = cur
    else:        t2.next = cur; t2 = cur
    cur = cur.next
t2.next = None               # ★★★ 必须切断
t1.next = d2.next            # 拼接
return d1.next
```

**`t2.next = None` 是这类题的头号 bug。**
第二条链的最后一个节点仍然挂着它在原链里的旧 `next`，
不切断就会**形成环**，或者把已经搬到第一条链的节点重新接回来。
（LC-0086 的 solution.py 里专门写了一个 `has_cycle` 检查来抓这个错。）

两题的唯一区别：
- **LC-0086**：分组条件是 `cur.val < x`（按**值**）。
- **LC-0328**：分组条件是**位置**的奇偶。
  注意是「第几个节点」，**不是节点值的奇偶** —— 这是最常见的读题错误。

两题都要求**组内保持原相对顺序**，而尾插天然稳定，所以不用做任何额外的事。

### LC-0025 K 个一组反转
它是 **LC-0024（k=2）的推广**，也是 LC-0092 的分组版本。5 个变量：
```
group_prev —— 上一组的尾（第一组是 dummy）
kth        —— 本组的第 k 个节点（不足 k 个就直接返回）
group_next —— 下一组的第一个 = kth.next
prev, curr —— 组内反转用的标准双指针
```
流程：
1. 从 `group_prev` 往后数 k 个，拿到 `kth`；**不足 k 个就结束**（题目要求尾部不反转）。
2. `group_next = kth.next`。
3. 以 `group_next` 为初始 `prev` 反转这 k 个 —— 反转完这一组的尾自动接上了下一组。
4. `tmp = group_prev.next`（它反转后变成了本组的尾）；`group_prev.next = kth`；`group_prev = tmp`。

**不要靠背赋值顺序来做这道题** —— 画一次图，把 5 个变量指到哪里标清楚，就能自己推出来。

### LC-0061 Rotate List
```
1. 数长度 n，同时走到尾节点
2. k %= n（k 可能远大于 n）；k == 0 直接返回
3. 尾接头形成环
4. 从 head 走 n - k - 1 步到新尾，断开
```
**这不是 Floyd 环检测** —— 这里的环是我们**主动造出来**的临时结构，
目的是让「找新头」变成一次简单的步数计算。用完立刻断开。

### LC-0725 Split Linked List in Parts
`base, extra = divmod(n, k)`：前 `extra` 段长 `base+1`，其余长 `base`。
这一行同时满足了题目的两个要求（长度相差 ≤ 1、前面的不短于后面的）。
`n < k` 时 `base == 0`，多出来的段自然是 None，**不需要特判**。
切断时：**先走到段尾、记下 `cur` 已前进到下一段，再把段尾的 next 置 None**。

## 题目

| # | 题 | 优先级 | 独有的东西 |
|---|---|---|---|
| 01/01 | LC-0086 Partition List | P1 | 按值分两组；`t2.next = None` |
| 01/02 | LC-0328 Odd Even Linked List | P1 | 按**位置**奇偶分组（不是值） |
| 02/01 | LC-0025 Reverse Nodes in k-Group | P0 | 5 个变量；不足 k 不反转 |
| 03/01 | LC-0061 Rotate List | P1 | `k %= n`；主动成环再断开 |
| 03/02 | LC-0725 Split Linked List in Parts | P2 | `divmod` 算段长；精确切断 |

## 常见错误
- 忘记 `t2.next = None` ⟹ 成环（LC-0086 / 0328）。
- LC-0328 按**值**的奇偶分组（读题错）。
- LC-0025 不足 k 个时还反转了。
- LC-0061 忘了 `k %= n` ⟹ k 很大时超时甚至死循环。
- LC-0725 切断的顺序反了 ⟹ 后面整条链丢失。

## 复习时的 Pattern Recognition
> 「按条件把链表分成两组且保序」「每 k 个反转一次」「整体旋转」「切成 k 段」
> → 多条子链 + dummy + tail，**最后别忘了切断**。
