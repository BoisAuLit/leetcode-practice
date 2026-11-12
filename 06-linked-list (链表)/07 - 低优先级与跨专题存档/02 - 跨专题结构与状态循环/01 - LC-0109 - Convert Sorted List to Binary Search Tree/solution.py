"""LC-0109 - Convert Sorted List to Binary Search Tree

快慢指针的用途：找中点当根，左右两半递归建子树
题目在问：把一条**升序**链表变成一棵高度平衡的 BST

为什么中点当根就平衡：左右两半节点数最多差 1，递归下去每一层都这样 → 高度 O(log n)。
这和 LC-0108（有序数组转 BST）是同一道题，唯一的区别是数组能 O(1) 取中点，链表要走一半。

坑：
  1. 必须拿到中点的**前驱**才能把左半段断开（prev.next = None），否则左半段还连着根和右半段，
     递归会把同一批节点反复用掉，结果不是树而是一团乱麻
  2. 断开要断两刀：prev.next = None（切左半）和 slow.next = None（切右半）
  3. 递归出口要两个：head 为空 → None；只剩一个节点 → 叶子。少写第二个会多跑一层空递归
  4. 这个解法是 O(n log n)，不是 O(n) —— 每层递归都要重新走一遍链表找中点。
     真正的 O(n) 解法是 Solution 3（中序构建），面试里能说出这点是加分项
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


##################################################################################################
##### ! Solution 1: 快慢指针找中点 + 分治递归
##### ! 时间复杂度: O(n log n)   空间复杂度: O(log n)   每层都要走一遍链表找中点，共 log n 层
##### ! 适用: 面试标准答案；本文件夹要练的就是"找中点 + 断开"这个动作
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution_1:
    def sortedListToBST(self, head: ListNode | None) -> TreeNode | None:
        if not head:  # ! 坑 3: 出口一
            return None
        if not head.next:  # ! 坑 3: 出口二，只剩一个节点就是叶子
            return TreeNode(head.val)

        prev, slow, fast = None, head, head
        while fast and fast.next:  # ! prev 跟在 slow 后面，为的是能把左半段切下来
            prev = slow
            slow = slow.next
            fast = fast.next.next

        prev.next = None            # ! 坑 2 第一刀: 切断左半段和根
        right_head = slow.next
        slow.next = None            # ! 坑 2 第二刀: 切断根和右半段

        root = TreeNode(slow.val)
        root.left = self.sortedListToBST(head)
        root.right = self.sortedListToBST(right_head)

        return root


##################################################################################################
##### ! Solution 2: 先倒进数组，再按下标分治（退化成 LC-0108）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)   数组 n + 递归栈 log n
##### ! 适用: 最好写、最不容易错；用 O(n) 空间换掉了"每层重走链表"的开销
##### ! 和 Solution 1 的取舍: 时间更好(O(n))，空间更差(O(n))。n 很大又卡内存时才需要权衡
##################################################################################################


class Solution_2:
    def sortedListToBST(self, head: ListNode | None) -> TreeNode | None:
        vals, cur = [], head
        while cur:
            vals.append(cur.val)
            cur = cur.next

        def build(lo: int, hi: int) -> TreeNode | None:
            if lo > hi:
                return None
            mid = (lo + hi) // 2  # ! 数组能 O(1) 取中点，这是它比链表省时间的唯一原因
            return TreeNode(vals[mid], build(lo, mid - 1), build(mid + 1, hi))

        return build(0, len(vals) - 1)


##################################################################################################
##### ! Solution 3: 中序构建 —— 边"中序遍历树的形状"边消耗链表
##### ! 时间复杂度: O(n)   空间复杂度: O(log n)   ★ 时间空间都是最优，严格优于前两个
##### ! 适用: 面试官追问"能不能 O(n) 时间 + O(log n) 空间"时的答案
##### ! 原理: BST 的中序遍历 = 升序，而链表本来就是升序。
##### !   所以先只按**下标范围**递归出树的形状，每当递归走到"该放这个节点了"的时刻，
##### !   就从链表头取下一个值 —— 取值顺序天然和中序一致，一个节点只碰一次
##################################################################################################


class Solution_3:
    def sortedListToBST(self, head: ListNode | None) -> TreeNode | None:
        n, cur = 0, head
        while cur:
            n += 1
            cur = cur.next

        self.cur = head  # ! 游标：递归过程中只会往后走，永不回头

        def build(lo: int, hi: int) -> TreeNode | None:
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            left = build(lo, mid - 1)       # ! 先建左子树，左子树建完游标正好停在根该取的值上
            node = TreeNode(self.cur.val)
            self.cur = self.cur.next
            node.left = left
            node.right = build(mid + 1, hi)  # ! 再建右子树
            return node

        return build(0, n - 1)


def build_list(vals: list[int]) -> ListNode | None:
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


if __name__ == "__main__":
    def inorder(t):
        return inorder(t.left) + [t.val] + inorder(t.right) if t else []

    def height(t):
        return 1 + max(height(t.left), height(t.right)) if t else 0

    def balanced(t):
        if not t:
            return True
        return abs(height(t.left) - height(t.right)) <= 1 and balanced(t.left) and balanced(t.right)

    cases = [[-10, -3, 0, 5, 9], [], [1], [1, 3], [1, 2, 3, 4, 5, 6, 7, 8]]

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        ok = True

        for n in range(0, 40):  # ! 穷举长度 0..39：中序必须等于原序列，且每个节点都要平衡
            vals = list(range(n))
            tree = sol.sortedListToBST(build_list(vals))
            if inorder(tree) != vals or not balanced(tree):
                ok = False
                print(f"   Solution_{i} 在长度 {n} 上失败: 中序={inorder(tree)} 平衡={balanced(tree)}")
                break

        for c in cases:
            tree = sol.sortedListToBST(build_list(c))
            if inorder(tree) != c or not balanced(tree):
                ok = False
                print(f"   Solution_{i} 在 {c} 上失败")
                break

        print(f"Solution_{i}: {'✅ 长度 0..39 穷举 + 固定用例：中序正确且处处平衡' if ok else '❌'}")
