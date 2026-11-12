"""LC-0117 - Populating Next Right Pointers in Each Node II（第二轮自主新增）

Level 1 · 06 BFS 层序遍历、视图与多叉树 —— **去掉「完美二叉树」假设之后会怎样**
题目在问：和 LC-0116 一样给每个节点连上同层右边的 next，但树**不再是完美二叉树**
         （任意形状，节点可以只有一个孩子）。

为什么新增它（它补的是哪个缺口 —— 这是本题全部的价值）：
  LC-0116 的 O(1) 空间解法依赖「**完美二叉树**」这个条件：
      - 每个节点要么没孩子，要么**两个都有**；
      - 所以 `node.left.next = node.right` 永远成立，
      - 而且 `node.right.next = node.next.left` 也永远成立（因为 node.next 一定有左孩子）。
  **一旦允许缺孩子，这两条全部失效**：
      `node.next` 可能没有左孩子、甚至没有任何孩子，必须一路往右找到第一个有孩子的。

  有了 LC-0117，才能看清 LC-0116 的解法**依赖了什么前提**，
  而不是把它当成一段背下来的代码。这和 LC-0081 之于 LC-0033 是同一种教学价值。

决定性观察（O(1) 空间解法）：
  1. **利用已经连好的上一层 next 指针，当作遍历上一层的「链表」**，
     在遍历过程中给下一层串 next。这样就不需要队列。
  2. 为下一层维护一个 **dummy 头**和一个 `tail` 指针：
     每遇到一个孩子就 `tail.next = child; tail = child`。
     dummy 让「下一层的第一个节点是谁」这件事不需要特判。
  3. 一层处理完，`cur = dummy.next`（下一层的头），`dummy.next = None` 重置。

```python
cur = root
while cur:
    dummy = Node(0); tail = dummy
    while cur:                       # 沿着当前层的 next 链走
        if cur.left:  tail.next = cur.left;  tail = tail.next
        if cur.right: tail.next = cur.right; tail = tail.next
        cur = cur.next
    cur = dummy.next                 # 下沉到下一层
```

复杂度：
  - **BFS 队列版**：O(n) 时间，**O(w) 空间** —— 不能说成 O(1)。
  - **上面这个「用上一层的 next 当链表」版**：O(n) 时间，**O(1) 额外空间**。
  题目的进阶要求就是后者。

LC-0116 vs LC-0117 对照：

| | LC-0116 | LC-0117 |
|---|---|---|
| 树形 | **完美**二叉树 | 任意二叉树 |
| `node.left.next = node.right` | 永远成立 | **不一定**（可能没有右孩子） |
| 找下一层邻居 | `node.next.left` 直接可用 | 要沿 next **一路往右找**第一个有孩子的 |
| O(1) 解法 | 直接两行连线 | 需要 dummy + tail |

边界：
  - 空树 → None
  - 单节点 → next 为 None
  - 只有左链 / 只有右链（每层只有一个节点）
  - 锯齿形（左右交替缺失）
"""

from collections import deque
from typing import List, Optional


class Node:
    def __init__(self, val: int = 0, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

    @staticmethod
    def from_list(values) -> Optional["Node"]:
        if not values or values[0] is None:
            return None
        root = Node(values[0])
        queue, i = [root], 1
        while queue and i < len(values):
            node = queue.pop(0)
            if i < len(values):
                if values[i] is not None:
                    node.left = Node(values[i]); queue.append(node.left)
                i += 1
            if i < len(values):
                if values[i] is not None:
                    node.right = Node(values[i]); queue.append(node.right)
                i += 1
        return root

    @staticmethod
    def read_next_chains(root) -> List[List[int]]:
        """沿每层的 next 链读出来，用于验证连接是否正确。"""
        out, level = [], root
        while level:
            row, cur, nxt_level = [], level, None
            while cur:
                row.append(cur.val)
                if nxt_level is None:
                    nxt_level = cur.left or cur.right
                cur = cur.next
            out.append(row)
            level = nxt_level
        return out

    @staticmethod
    def bfs_levels(root) -> List[List[int]]:
        """标准 BFS 层序，作为 next 链的正确答案。"""
        if not root:
            return []
        out, q = [], deque([root])
        while q:
            row = []
            for _ in range(len(q)):
                n = q.popleft()
                row.append(n.val)
                if n.left: q.append(n.left)
                if n.right: q.append(n.right)
            out.append(row)
        return out


##################################################################################################
##### ! Solution 1: 用上一层已连好的 next 当链表遍历 + dummy/tail 串下一层（O(1) 额外空间）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：任意形状的二叉树连 next；LC-0116 的通用版本
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def connect(self, root: Optional[Node]) -> Optional[Node]:
        cur = root
        while cur:
            dummy = Node(0)            # ! 下一层的哑头，省掉「下一层第一个是谁」的特判
            tail = dummy
            while cur:                 # ! 沿当前层的 next 链横着走
                if cur.left:
                    tail.next = cur.left
                    tail = tail.next
                if cur.right:
                    tail.next = cur.right
                    tail = tail.next
                cur = cur.next
            cur = dummy.next           # ! 下沉到下一层的第一个节点
        return root


##################################################################################################
##### ! Solution 2: 标准分层 BFS（最直白，但空间是 O(w) 不是 O(1)）
##### ! 时间复杂度: O(n)   空间复杂度: O(w)
##### ! 适用：先给这版再被追问「能不能 O(1) 空间」；**不要把它说成 O(1)**
##################################################################################################


class Solution_2:
    def connect(self, root: Optional[Node]) -> Optional[Node]:
        if not root:
            return None
        q = deque([root])
        while q:
            size = len(q)
            prev = None
            for _ in range(size):
                node = q.popleft()
                if prev:
                    prev.next = node   # ! 同层相邻才连
                prev = node
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            prev.next = None           # ! 每层最后一个指向 None
        return root


if __name__ == "__main__":
    import random

    cases = [[1, 2, 3, 4, 5, None, 7], [], [1], [1, 2, None, 3],
             [1, None, 2, None, 3], [1, 2, 3, None, 5, 6, None]]
    for vals in cases:
        want = Node.bfs_levels(Node.from_list(vals))
        for Sol in (Solution_1, Solution_2):
            t = Node.from_list(vals)
            Sol().connect(t)
            got = Node.read_next_chains(t)
            assert got == want, (vals, Sol.__name__, got, want)
        print(f"{vals} -> next 链 {want}")

    for _ in range(800):                 # ! 随机非完美二叉树：next 链必须等于 BFS 层序
        vals = [random.choice([random.randint(1, 9), None]) for _ in range(random.randint(1, 16))]
        vals[0] = 1
        want = Node.bfs_levels(Node.from_list(vals))
        for Sol in (Solution_1, Solution_2):
            t = Node.from_list(vals)
            Sol().connect(t)
            assert Node.read_next_chains(t) == want, (vals, Sol.__name__)
    print("随机对拍 800 组通过 ✓（O(1) 空间版与 BFS 版的 next 链完全一致）")
