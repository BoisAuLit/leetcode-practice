# Level 1 · 01 基础指针、Dummy Node 与反转

## 核心定义
链表的全部基本功：**遍历、哑节点、原地反转、局部重连**。
后面六章都建立在这四件事上。

## 决定性观察
1. **改 `next` 之前必须先把它存下来** —— 这是链表题唯一的物理定律。
   `nxt = curr.next` 写在 `curr.next = prev` 之前，顺序反了链就断了。
2. **头节点可能变** ⟹ 用 Dummy Node。判据很简单：
   「这道题会删掉或替换头节点吗？」会，就加 dummy。
3. **交换节点 ≠ 交换值**。LC-0024 考的就是真正的指针重连。

## Loop Invariant
- 反转：`prev` 指向已反转部分的头，`curr` 指向待处理部分的首节点。
- 删除：`prev` 指向最后一个**确定保留**的节点。

## 模板
```python
# 整条反转（LC-0206）
prev, curr = None, head
while curr:
    nxt = curr.next
    curr.next = prev
    prev, curr = curr, nxt
return prev

# Dummy + 删除（LC-0203 / 0082）
dummy = ListNode(0, head); prev = dummy; cur = head
while cur:
    if 要删: prev.next = cur.next
    else:    prev = cur
    cur = cur.next
return dummy.next
```

## 题目

| # | 题 | 优先级 | 独有的东西 |
|---|---|---|---|
| 01/01 | LC-0206 Reverse Linked List | P0 | 反转模板本身；**整个专题最该写熟的 5 行** |
| 01/02 | LC-0092 Reverse Linked List II | P1 | 局部反转 + 4 个边界位置接线；`left==1` 靠 dummy |
| 01/03 | LC-0024 Swap Nodes in Pairs | P1 | 真·交换节点；是 LC-0025 的 k=2 特例 |
| 02/01 | LC-0203 Remove Linked List Elements | P1 | 最基础的 dummy + 删除 |
| 02/02 | LC-0083 Remove Duplicates from Sorted List | P2 | 每个值留一个；**不需要** dummy |
| 02/03 | LC-0082 Remove Duplicates from Sorted List II | P1 | 重复的全删；**必须** dummy + prev 不动 |
| 03/01 | LC-0002 Add Two Numbers | P0 | 低位在前，边走边加 + 尾插；carry 要进循环条件 |
| 03/02 | LC-0445 Add Two Numbers II | P1 | 高位在前 ⟹ **栈** + **头插**；不许修改输入 |

## 三组必须分清的对照

### LC-0083 vs LC-0082
| | 0083 | 0082 |
|---|---|---|
| 规则 | 每个值留一个 | 重复过的一个不留 |
| `1->1->2` | `1->2` | `2` |
| 头会被删吗 | 不会 | **会** |
| Dummy | 不需要 | **需要** |
| 指针 | 1 个 | prev + cur，且**删完 prev 不动** |

### LC-0002 vs LC-0445
| | 0002 | 0445 |
|---|---|---|
| 数字顺序 | 低位在前 | **高位在前** |
| 遍历 vs 进位方向 | 一致 | **相反** |
| 技巧 | 边走边加 | **栈**（题目不许反转输入） |
| 结果构造 | 尾插 | **头插** |

### LC-0024 vs LC-0025
0024 就是 0025 的 **k = 2**。先把 0024 的三条接线画清楚，
0025 只是把「三条接线」换成「反转 k 个的循环 + 两条接线」。

## 常见错误
- 改 `curr.next` 之前忘了存 `nxt`。
- LC-0083 删除后立刻 `cur = cur.next` ⟹ `1->1->1` 只删掉一个。
- LC-0082 删完整组后把 `prev` 也往前挪了 ⟹ 连续两组重复会漏删。
- LC-0082 用 `if` 而不是 `while` 跳过重复。
- LC-0002 / 0445 忘了把 `carry` 写进循环条件 ⟹ `[9,9] + [1]` 丢最高位。
- LC-0024 偷懒交换 `val` —— 题目考的就是指针。

## 复习时的 Pattern Recognition
> 「反转整条 / 某一段 / 每 k 个」「删除满足条件的节点」「两数相加」
> → 先问自己：**头节点会变吗？**（决定要不要 dummy）
