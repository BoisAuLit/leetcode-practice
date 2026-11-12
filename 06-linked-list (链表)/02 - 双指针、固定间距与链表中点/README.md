# Level 1 · 02 双指针、固定间距与链表中点

## 核心定义
链表**不能随机访问**，所以「第 n 个」「中间那个」「倒数第 k 个」
都要靠两个指针的相对关系一趟算出来。

## 三种双指针，不要混为一谈

| 类型 | 两指针的关系 | 解决什么 | 题 |
|---|---|---|---|
| **快慢**（速度不同） | 一步 vs 两步 | 找中点、判环 | 0876、0234、0143、0148、2095 |
| **固定间距**（速度相同） | 始终相差 n | 倒数第 n 个 | 0019 |
| **换头对齐**（速度相同） | 走完自己换到对方 | 两链交点 | 0160 |

**LC-0160 不是 Floyd**：两个指针速度一样，只是走的路径不同。
不要因为「用了两个指针」就把它归到环检测。

## 决定性观察

### 找中点（LC-0876）
```python
slow = fast = head
while fast and fast.next:
    slow, fast = slow.next, fast.next.next
```
- 奇数长度 → slow 正好在正中间。
- 偶数长度 → slow 在**第二个**中点。
- 想要**第一个**中点：条件改成 `while fast.next and fast.next.next`。

**这两种停法必须按题目选**：
LC-0143 Reorder 需要前半段不长于后半段；LC-0148 Sort 需要能切成非空的两半
（否则 `[1,2]` 会无限递归）。

### 固定间距（LC-0019）
```python
fast = dummy
for _ in range(n): fast = fast.next
slow = dummy
while fast.next:
    slow, fast = slow.next, fast.next
slow.next = slow.next.next
```
**从 dummy 出发**是关键：这样 slow 最终停在**待删节点的前驱**上，
`n == 链表长度`（删头节点）也不用特判。

### 换头对齐（LC-0160）
```python
a, b = headA, headB
while a is not b:
    a = a.next if a else headB
    b = b.next if b else headA
return a
```
**为什么一定会相遇**：a 走的总长是 `lenA + lenB`，b 走的是 `lenB + lenA`，
两者相等，所以它们一定在同一时刻到达同一个位置。
- 有交点 → 在交点相遇。
- 无交点 → 同时变成 `None`，循环以 `a is b is None` 结束。

**比较的是节点身份（`is`），不是 `val`** —— 两条链上值相同的节点不是交点。

## 03 小节：同一个骨架的三道题

```
1. 找中点
2. 反转后半段
3. 两半一起处理
```

| 题 | 第 3 步做什么 |
|---|---|
| LC-0234 Palindrome | 从两端往中间**逐个比较** |
| LC-0143 Reorder List | 两半**交替拼接** |
| LC-2130 Max Twin Sum | 两半**配对求和取最大** |

**这三道不需要记三套算法。** 写熟其中一道，另外两道只改最后一步。
LC-0234 可以讨论「要不要把链表恢复原状」—— 面试里主动提一句会加分
（恢复要再反转一次，O(n) 额外时间，但保持了函数无副作用）。

## 题目

| # | 题 | 优先级 |
|---|---|---|
| 01/01 | LC-0876 Middle of the Linked List | P0 |
| 01/02 | LC-0019 Remove Nth Node From End | P0 |
| 01/03 | LC-2095 Delete the Middle Node | P2（0876 的直接延伸） |
| 02/01 | LC-0160 Intersection of Two Linked Lists | P1 |
| 03/01 | LC-0234 Palindrome Linked List | P0 |
| 03/02 | LC-0143 Reorder List | P0 |
| 03/03 | LC-2130 Maximum Twin Sum | P1 |

## 常见错误
- `while fast and fast.next` 写成 `while fast.next and fast`（后者会 AttributeError）。
- LC-0019 不用 dummy ⟹ 删头节点时要写一堆特判。
- LC-0143 反转后忘记**切断前半段的尾巴** ⟹ 形成环。
- LC-0143 奇数长度时最后一个节点的 next 没置 None ⟹ 成环。
- LC-0160 比较 `a.val == b.val` 而不是 `a is b`。

## 复习时的 Pattern Recognition
> 「中间节点」「倒数第 n 个」「回文」「重排成 1-n-2-(n-1)」「两链交点」
> → 先确定用哪一种双指针：**速度不同？间距固定？还是换头？**
