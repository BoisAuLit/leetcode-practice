# 02 - 固定间距与倒数定位

本目录**没有题目文件夹**。主归属在链表专题：

| | 题 | 位置 |
|---|---|---|
| **P0** | LC-0019 Remove Nth Node From End of List | [06-linked-list/fast-slow-pointers/04-LC-0019](<../../../06-linked-list (链表)/02 - 双指针、固定间距与链表中点/01 - 寻找中点与固定指针间距/02 - LC-0019 - Remove Nth Node From End of List>) |

同一个文件夹里还有一整组固定间距 / 找中点的题（0876、0234、0143、1721、2130、0061 等），
整组见 [06-linked-list/fast-slow-pointers 文件夹](<../../../06-linked-list (链表)/02 - 双指针、固定间距与链表中点>)。

## 规则

两个指针**同速**，但先让 `fast` 走出 n 步的间距，然后一起走。
`fast` 到尾部时，`slow` 正好落在倒数第 n+1 个位置上。

```python
dummy = ListNode(0, head)        # ! 哑结点：删头结点时不用特判
slow = fast = dummy
for _ in range(n):               # ! 先拉开 n 步
    fast = fast.next
while fast.next:                 # ! 一起走，fast.next 为空时 slow 停在待删结点的前一个
    slow = slow.next
    fast = fast.next
slow.next = slow.next.next
return dummy.next
```

## 不变量

全程 `fast` 比 `slow` 领先恰好 n 个结点。这是一个**人为制造并始终维持**的不变量 ——
和环检测的「差值每轮减 1」正好相反：那里差值在变，这里差值被固定住。

**所以这两件事不能合成一个模板**：
- 环检测：**不同速**（1 和 2），靠差值变化去撞上
- 固定间距：**同速**，靠恒定的间距把「倒数第 n」翻译成「正数第 k」
- 找中点：**不同速**（1 和 2），但目的是位置而不是环；循环条件决定落在前中点还是后中点
  （`while fast and fast.next` → 后中点；`while fast.next and fast.next.next` → 前中点）

## 易错点

- 间距拉 `n` 步还是 `n+1` 步，取决于你想让 slow 停在待删结点还是它的前驱。
  用 dummy + 拉 n 步 + `while fast.next`，slow 停在前驱，是最省心的组合。
- 不用 dummy 时，删除头结点（`n == 链表长度`）要单独写一个分支，容易漏。
