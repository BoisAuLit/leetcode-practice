# 01 - 环检测与环入口

本目录**没有题目文件夹**。这组题的主归属是链表专题，按仓库「一题一个文件夹」的规矩不复制：

| | 题 | 位置 |
|---|---|---|
| **P0** | LC-0141 Linked List Cycle | [06-linked-list/Floyd's/LC-0141](<../../../06-linked-list (链表)/03 - Floyd 环检测与隐式函数图/01 - 链表环检测与环入口/01 - LC-0141 - Linked List Cycle>) |
| **P0** | LC-0142 Linked List Cycle II | [06-linked-list/Floyd's/LC-0142](<../../../06-linked-list (链表)/03 - Floyd 环检测与隐式函数图/01 - 链表环检测与环入口/02 - LC-0142 - Linked List Cycle II>) |
| P1 | LC-0287 Find the Duplicate Number（数组当函数图）| [01-arrays-hashing/04 - Array Index Mapping/04 - LC-0287](../../../01-arrays-hashing%20%28%E6%95%B0%E7%BB%84%E3%80%81%E5%93%88%E5%B8%8C%E8%A1%A8%29/04%20-%20Array%20Index%20Mapping%20%E4%B8%8E%20In-place%20Marking/04%20-%20LC-0287%20-%20Find%20the%20Duplicate%20Number) |
| P1 | LC-0202 Happy Number（抽象状态当节点）| [06-linked-list/Floyd's/LC-0202](<../../../06-linked-list (链表)/03 - Floyd 环检测与隐式函数图/02 - 隐式函数图与环检测/01 - LC-0202 - Happy Number>) |

## 1. 规则

`slow` 每次一步，`fast` 每次两步。fast 走到尽头 → 无环；两者相遇 → 有环。

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast:
        break            # 有环
else:
    return None          # 无环（fast 撞到了 None）
```

## 2. 为什么环里一定会相遇

两个指针都进环之后，把它们的距离看成环上的一个数 d。
每走一轮，fast 比 slow 多走一步，所以 **d 每轮减少恰好 1**（模环长）。
一个非负整数每轮减 1，必然在有限步内变成 0 —— 这就是相遇。

注意这个论证依赖「每轮差值变化恰好 1」。如果 fast 每次走 3 步，差值每轮减 2，
在环长为偶数、初始距离为奇数时就可能永远跨过去不相遇。**所以必须是 1 和 2。**

## 3. 为什么从头再走一遍就是环入口

设环外长度 a，入口到相遇点 b，环长 L。相遇时 slow 走了 `a + b`，fast 走了 `2(a + b)`，
而 fast 比 slow 多走了整数圈：`2(a+b) - (a+b) = a + b = kL`，于是 `a = kL - b`。

把一个新指针放回起点，两个指针同时**每次一步**：新指针走 a 步到入口，
slow 从相遇点走 a 步 = 走了 `kL - b` 步，正好也停在入口。所以它们在入口相遇。

```python
slow2 = head
while slow2 is not slow:
    slow2 = slow2.next
    slow = slow.next
return slow2             # 环入口
```

## 4. 这一套能用在什么地方

「下一步唯一确定」= 一张函数图，就能用 Floyd，**不需要真的是链表**：
- LC-0287：`i → nums[i]`，重复值就是环入口（而且**不许改数组**，所以标记法失效）
- LC-0202：`n → 各位平方和`，状态是抽象的数
- 更远的变体见 [06-linked-list/Floyd's 文件夹](<../../../06-linked-list (链表)/03 - Floyd 环检测与隐式函数图>)（LC-0457、LC-0957）

## 和本专题其他家族的区别

这是**同向、不同速**的两个指针，用来发现**结构性质**（有没有环、环在哪）。
Level 01 的对撞指针是**反向、同速**，用来**缩小搜索空间**。两者不要混为一个模板。
