"""LC-0024 - Swap Nodes in Pairs

Level 1 · 01 基础指针、Dummy Node 与反转 —— 两两交换**节点本身**（不是交换值）
题目在问：每两个相邻节点交换一次，1->2->3->4 变成 2->1->4->3。

决定性观察：
  1. **必须真正重连指针，不能偷懒交换 val。** 面试官问这道题就是在考指针操作；
     而且如果节点里带了别的字段（或题目禁止改值），交换 val 就是错的。
  2. 每一轮只涉及 4 个位置，画出来就不用背：
        prev   —— 上一对的尾（第一轮是 dummy）
        first  —— 这一对的第 1 个
        second —— 这一对的第 2 个
        next_pair = second.next
     三条接线：`prev.next = second`、`second.next = first`、`first.next = next_pair`。
     然后 `prev = first`（first 现在是这一对的尾）。
  3. **Dummy Node 必需**：头节点会被换掉，有 dummy 就不用为「第一对」单独写分支。

循环条件 `while prev.next and prev.next.next`：
      必须同时检查两个，保证确实还有**完整的一对**。
      奇数长度时最后剩一个节点，它自然留在原位（prev.next 已经指着它）。

和 LC-0025（K 个一组反转）的关系：
      **LC-0024 就是 k = 2 的特例。** 先把 24 画清楚，25 就只是把「3 条接线」
      换成「反转 k 个的循环 + 2 条接线」。不要当成两道互不相干的题。

复杂度：O(n) 时间，O(1) 额外空间（递归版是 O(n) 栈空间）。

边界：
  - [] → []
  - [1] → [1]（单个节点不动）
  - [1,2] → [2,1]
  - [1,2,3] → [2,1,3]（奇数长度，最后一个不动）
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    @staticmethod
    def from_list(values: List[int]) -> Optional["ListNode"]:
        dummy = ListNode()
        cur = dummy
        for v in values:
            cur.next = ListNode(v)
            cur = cur.next
        return dummy.next

    @staticmethod
    def to_list(head: Optional["ListNode"]) -> List[int]:
        out = []
        while head:
            out.append(head.val)
            head = head.next
        return out


##################################################################################################
##### ! Solution 1: 迭代 + Dummy Node，每轮三条接线
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：所有「固定小分组内重排节点」的题；LC-0025 是它的 k 推广
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:      # ! 必须还剩完整的一对
            first = prev.next
            second = first.next
            next_pair = second.next
            prev.next = second                   # ! 三条接线，顺序照着画的图写
            second.next = first
            first.next = next_pair
            prev = first                         # ! first 现在是这一对的尾巴
        return dummy.next


##################################################################################################
##### ! Solution 2: 递归 —— 换好头两个，剩下的交给递归
##### ! 时间复杂度: O(n)   空间复杂度: O(n) 调用栈
##### ! 适用：代码最短、最好口述；但不满足 O(1) 空间，面试被追问时要说清楚
##################################################################################################


class Solution_2:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:            # ! 不足一对就原样返回
            return head
        second = head.next
        head.next = self.swapPairs(second.next)  # ! head 接上「剩余部分交换后的结果」
        second.next = head
        return second                            # ! second 成为新的头


##################################################################################################
##### ! Solution 3: 取出所有值、两两交换后重建（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：正确性参照。注意这**不是**本题想要的解法（它交换的是值，不是节点）
##################################################################################################


class Solution_3:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        vals = ListNode.to_list(head)
        for i in range(0, len(vals) - 1, 2):
            vals[i], vals[i + 1] = vals[i + 1], vals[i]
        return ListNode.from_list(vals)


if __name__ == "__main__":
    import random

    for vals in [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]:
        a = ListNode.to_list(Solution_1().swapPairs(ListNode.from_list(vals)))
        b = ListNode.to_list(Solution_2().swapPairs(ListNode.from_list(vals)))
        c = ListNode.to_list(Solution_3().swapPairs(ListNode.from_list(vals)))
        assert a == b == c, (vals, a, b, c)
        print(f"{vals} -> {a}")

    # ! 额外验证「交换的是节点而不是值」：给节点打标记，看标记有没有跟着一起走
    nodes = [ListNode(i) for i in range(4)]
    for i in range(3):
        nodes[i].next = nodes[i + 1]
    for i, nd in enumerate(nodes):
        nd.tag = f"node{i}"
    res = Solution_1().swapPairs(nodes[0])
    tags = []
    cur = res
    while cur:
        tags.append(cur.tag)
        cur = cur.next
    assert tags == ["node1", "node0", "node3", "node2"], tags
    print("节点身份检查通过 ✓ 交换的是节点本身，不是 val:", tags)

    for _ in range(500):
        vals = [random.randint(0, 9) for _ in range(random.randint(0, 9))]
        a = ListNode.to_list(Solution_1().swapPairs(ListNode.from_list(vals)))
        b = ListNode.to_list(Solution_2().swapPairs(ListNode.from_list(vals)))
        c = ListNode.to_list(Solution_3().swapPairs(ListNode.from_list(vals)))
        assert a == b == c, (vals, a, b, c)
    print("随机对拍 500 组通过 ✓")
