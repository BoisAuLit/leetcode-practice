"""LC-0430 - Flatten a Multilevel Doubly Linked List

Level 1 · 06 复杂指针与链表数据结构设计 —— Doubly Linked List + 嵌套结构展开
题目在问：双向链表的节点除了 prev/next 还有一个 child 指针指向另一条链表。
         把整个多级结构展开成一条单层双向链表，child 全部置空，顺序按**深度优先**。

（Solution_1 的 `flatten` 方法体来自用户原有的
 `_original_sources/02 - Flatten ML Doubly Linked List.py`，**一字未改**；
 原文件也完整保留在 `_original_sources/` 里。）

决定性观察：
  1. 展开顺序就是 **DFS 前序**：遇到 child 就先把 child 整条链插进来，再接回原来的 next。
     所以这题本质是「用链表表示的树做前序遍历」。
  2. **用栈模拟 DFS 时，入栈顺序必须是「先 next 后 child」**，
     因为栈是后进先出，这样弹出时才会**先处理 child**。写反了顺序就错了。
  3. 双向链表意味着每次接线要写**两条**：`prev.next = curr` **和** `curr.prev = prev`。
     漏掉任何一条，结果在正向遍历时看起来是对的，反向遍历就崩了 —— 这是本题最隐蔽的坑。
  4. `curr.child = None` **必须做**，题目明确要求展开后不能还留着 child 指针。
  5. 最后 `dummy.next.prev = None`：头节点的 prev 不能指向 dummy。

Dummy Node 的作用：统一「第一个节点」的接线，不用为 head 单独写分支。

两种实现的取舍：
  - **Solution_1（显式栈）**：O(1) 概念上的递归深度控制，不会爆栈，面试首选。
  - **Solution_2（原地拼接）**：不用栈，O(1) 额外空间 —— 遇到 child 就把 child 链
    整条「缝」进当前位置，再把原来的 next 接到 child 链的尾部。思路更巧，但指针更多。

复杂度：
  - Solution_1：O(n) 时间，O(n) 栈空间（最坏是一条全是 child 的深链）。
  - Solution_2：O(n) 时间（每个节点最多被访问常数次），**O(1) 额外空间**。

边界：
  - head = None → None
  - 没有任何 child → 原链不变
  - child 链本身还有 child（多层嵌套）
  - child 挂在最后一个节点上（child 链接完后面没有东西了）
  - 单节点带 child
"""

from collections import deque
from typing import List, Optional


class Node:
    def __init__(self, val, prev=None, next=None, child=None):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child

    @staticmethod
    def print_doubly(node) -> None:
        while node:
            print(node.val)
            node = node.next

    # ---- 下面是测试用的辅助函数，不属于题解 ----
    @staticmethod
    def build(spec) -> Optional["Node"]:
        """spec 形如 [1, 2, (3, [7, 8, (9, [...])]), 4]；元组表示该节点带一条 child 链。"""
        head = prev = None
        for item in spec:
            val, child_spec = item if isinstance(item, tuple) else (item, None)
            nd = Node(val)
            nd.child = Node.build(child_spec) if child_spec else None
            if prev:
                prev.next = nd
                nd.prev = prev
            else:
                head = nd
            prev = nd
        return head

    @staticmethod
    def to_list(head: Optional["Node"]) -> List[int]:
        out = []
        while head:
            out.append(head.val)
            head = head.next
        return out

    @staticmethod
    def check_flat(head: Optional["Node"]) -> List[int]:
        """正向走一遍，同时校验 prev 指针和 child 已清空；返回反向走回来的序列。"""
        if not head:
            return []
        assert head.prev is None, "头节点的 prev 必须是 None"
        forward, tail = [], head
        while True:
            assert tail.child is None, f"节点 {tail.val} 的 child 没有清空"
            forward.append(tail.val)
            if not tail.next:
                break
            assert tail.next.prev is tail, f"节点 {tail.next.val} 的 prev 没有正确回指"
            tail = tail.next
        backward = []
        while tail:
            backward.append(tail.val)
            tail = tail.prev
        assert backward[::-1] == forward, "反向遍历和正向遍历不一致"
        return forward


##################################################################################################
##### ! Solution 1: 显式栈模拟 DFS（用户原有实现，方法体未改动）
##### ! 时间复杂度: O(n)   空间复杂度: O(n) 栈
##### ! 适用：一切「链表表示的树做前序展开」；入栈顺序必须先 next 后 child
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def flatten(self, head: "Optional[Node]") -> "Optional[Node]":
        # ! This is very important
        if not head:
            return head
        stack = deque([head])

        dummy = Node(0, None, None, None)
        prev = dummy
        while stack:
            curr = stack.pop()
            prev.next = curr
            curr.prev = prev

            if curr.next:
                stack.append(curr.next)
            if curr.child:
                stack.append(curr.child)
                curr.child = None
            prev = curr
        dummy.next.prev = None
        return dummy.next


##################################################################################################
##### ! Solution 2: 原地拼接 —— 遇到 child 就把整条 child 链「缝」进当前位置
##### ! 时间复杂度: O(n)   空间复杂度: O(1) 额外
##### ! 适用：被追问 O(1) 空间时；不用栈，但指针接线更多，要小心 prev 的两条线
##################################################################################################


class Solution_2:
    def flatten(self, head: "Optional[Node]") -> "Optional[Node]":
        cur = head
        while cur:
            if cur.child:
                nxt = cur.next                 # ! 先把原来的后继存起来
                child = cur.child
                cur.child = None               # ! 题目要求清空
                cur.next = child               # ! 把 child 链接到当前位置后面
                child.prev = cur
                tail = child
                while tail.next:               # ! 走到 child 链的尾部
                    tail = tail.next
                tail.next = nxt                # ! 再把原后继接到 child 链尾
                if nxt:
                    nxt.prev = tail
            cur = cur.next
        return head


##################################################################################################
##### ! Solution 3: 递归 DFS 收集所有值后重建（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 直接表达「展开顺序 == DFS 前序」这个定义
##################################################################################################


class Solution_3:
    def flatten(self, head: "Optional[Node]") -> "Optional[Node]":
        order: List[int] = []

        def dfs(node):
            while node:
                order.append(node.val)
                if node.child:
                    dfs(node.child)
                node = node.next

        dfs(head)
        if not order:
            return None
        nodes = [Node(v) for v in order]
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
            nodes[i + 1].prev = nodes[i]
        return nodes[0]


if __name__ == "__main__":
    import random

    specs = [
        [1, 2, (3, [7, 8, (11, [12]), 9, 10]), 4, 5, 6],      # 官方样例
        [1, (2, [3])],
        [],
        [1],
        [(1, [2, (3, [4])])],                                   # 层层嵌套
        [1, 2, (3, [4])],                                       # child 挂在中间
        [1, (2, [3, 4])],
    ]
    for spec in specs:
        a = Node.check_flat(Solution_1().flatten(Node.build(spec)))
        b = Node.check_flat(Solution_2().flatten(Node.build(spec)))
        c = Node.to_list(Solution_3().flatten(Node.build(spec)))
        assert a == b == c, (spec, a, b, c)
        print(f"{spec} -> {a}")

    def rand_spec(depth, counter):
        out = []
        for _ in range(random.randint(0, 4)):
            v = next(counter)
            if depth < 3 and random.random() < 0.35:
                out.append((v, rand_spec(depth + 1, counter)))
            else:
                out.append(v)
        return out

    for _ in range(500):                 # ! 随机多级结构对拍（同时校验 prev 指针与 child 清空）
        it = iter(range(1, 1000))
        spec = rand_spec(0, it)
        a = Node.check_flat(Solution_1().flatten(Node.build(spec)))
        b = Node.check_flat(Solution_2().flatten(Node.build(spec)))
        c = Node.to_list(Solution_3().flatten(Node.build(spec)))
        assert a == b == c, (spec, a, b, c)
    print("随机对拍 500 组通过 ✓（prev 回指、child 清空、DFS 顺序全部校验）")
