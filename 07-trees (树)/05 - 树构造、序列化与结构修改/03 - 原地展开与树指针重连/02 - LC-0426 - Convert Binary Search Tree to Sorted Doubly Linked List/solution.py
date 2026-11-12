"""LC-0426 - Convert Binary Search Tree to Sorted Doubly Linked List

Level 1 · 05 树构造、序列化与结构修改 → Level 2 · 03 原地展开与树指针重连

题目在问：把 BST **原地**改成有序的**循环双向链表**：`left` 当 prev、`right` 当 next，首尾相连，返回最小节点。

### 决定性观察：中序遍历 + 「记住上一个访问的节点」

BST 的中序就是升序。链表只需要在中序访问每个节点时做一件事：

    prev.right = node        # ! 上一个的 next 指向我
    node.left  = prev        # ! 我的 prev 指向上一个
    prev = node

这是「中序遍历 + prev 指针」这一招的标准用法，和 LC-0114 Flatten（前序 + prev）、LC-0897 Increasing Order Search Tree 同源。
遍历完成后 `head.left = prev; prev.right = head` 闭合成环。

### 为什么递归过程中改 left 不会把树弄坏

中序访问 node 时，它的左子树**已经遍历完了**（左 → 根 → 右），之后再也不需要 `node.left` 指向原左孩子；
而 `node.right` 要等到访问 node 之后才被 prev 规则改写，那时我们正要去遍历右子树 —— 所以**要先取出 `node.right` 再改**，
或者按递归的自然顺序（先递归左、处理自己、再递归右）：处理自己时只改 `node.left` 和 `prev.right`，
`prev.right` 是上一个节点的 right —— 上一个节点的右子树在中序里已经走完（否则它不会是 prev）。安全。

迭代版用显式栈，同一规则；但要注意弹出节点后**先保存 `node.right`** 再改指针。
"""
from typing import Optional


class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


##################################################################################################
##### ! Solution 1: 递归中序 + prev 指针（原地）
##### ! 时间复杂度: O(n)   空间复杂度: O(h) 递归栈
##### ! 适用：面试标准答案。first 记最小节点（第一次访问），prev 记上一个访问的节点；最后闭环
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def treeToDoublyList(self, root: Optional[Node]) -> Optional[Node]:
        if not root:
            return None
        first = prev = None

        def inorder(node):
            nonlocal first, prev
            if not node:
                return
            inorder(node.left)
            if prev:
                prev.right = node                   # ! 上一个的 next → 我
                node.left = prev                    # ! 我的 prev → 上一个
            else:
                first = node                        # ! 第一个访问到的 = 最小
            prev = node
            inorder(node.right)

        inorder(root)
        first.left, prev.right = prev, first        # ! 闭环
        return first


##################################################################################################
##### ! Solution 2: 迭代中序（显式栈）+ prev 指针
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：树很深怕递归爆栈时。弹出节点后要先记下 node.right 再改指针（这里 right 是原孩子，还没被改过，
#####         但保持「先取后改」的习惯最稳）
##################################################################################################


class Solution_2:
    def treeToDoublyList(self, root: Optional[Node]) -> Optional[Node]:
        if not root:
            return None
        stack, node = [], root
        first = prev = None
        while stack or node:
            while node:
                stack.append(node); node = node.left
            node = stack.pop()
            nxt = node.right                        # ! 先保存原右孩子
            if prev:
                prev.right, node.left = node, prev
            else:
                first = node
            prev = node
            node = nxt
        first.left, prev.right = prev, first
        return first


##################################################################################################
##### ! Solution 3: 先中序收集到列表，再串链表（非原地，两遍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：面试「第一版」或作为真值基线；题目要求原地，所以只能当过渡。注意它仍然复用原节点，只是多存一个列表
##################################################################################################


class Solution_3:
    def treeToDoublyList(self, root: Optional[Node]) -> Optional[Node]:
        if not root:
            return None
        nodes = []

        def inorder(n):
            if n:
                inorder(n.left); nodes.append(n); inorder(n.right)

        inorder(root)
        k = len(nodes)
        for i, n in enumerate(nodes):
            n.left, n.right = nodes[i - 1], nodes[(i + 1) % k]   # ! i-1 在 i=0 时是 -1 → 最后一个，天然闭环
        return nodes[0]


def build_bst(vals):
    root = None
    for v in vals:
        if root is None:
            root = Node(v); continue
        cur = root
        while True:
            if v < cur.val:
                if cur.left: cur = cur.left
                else: cur.left = Node(v); break
            else:
                if cur.right: cur = cur.right
                else: cur.right = Node(v); break
    return root


def walk(head, n):
    """沿 right 走 n 步收集值，同时检查 left 是反向指针。"""
    out, cur = [], head
    for _ in range(n):
        out.append(cur.val)
        assert cur.right.left is cur, "prev/next 不互逆"
        cur = cur.right
    assert cur is head, "没有闭环"
    return out


if __name__ == "__main__":
    import random
    random.seed(426)
    for cls in (Solution_1, Solution_2, Solution_3):
        head = cls().treeToDoublyList(build_bst([4, 2, 5, 1, 3]))
        assert walk(head, 5) == [1, 2, 3, 4, 5], cls.__name__
        single = cls().treeToDoublyList(Node(7))
        assert single.left is single and single.right is single    # ! 单节点自环
        assert cls().treeToDoublyList(None) is None
        for _ in range(100):
            vals = random.sample(range(100), random.randint(1, 25))
            head = cls().treeToDoublyList(build_bst(vals))
            assert walk(head, len(vals)) == sorted(vals), (cls.__name__, vals)
    print("所有测试通过 ✓")
