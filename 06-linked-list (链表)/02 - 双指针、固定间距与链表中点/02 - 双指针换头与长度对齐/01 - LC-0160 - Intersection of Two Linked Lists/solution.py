"""LC-0160 - Intersection of Two Linked Lists

双指针的用途：**路径对齐**（注意：这题不是 Floyd 判圈，没有快慢之分，两个指针同速）
题目在问：两条链表从某个节点开始共用一条尾巴，找出这个汇合点；不相交返回 None

为什么"走到头就跳到对方的头"能对齐：
    设 A 独有部分长 a，B 独有部分长 b，共用尾巴长 c。
    指针 A 走的总路程 = a + c + b，指针 B 走的总路程 = b + c + a —— 完全相等。
    所以两个指针在走完第二条链之前必然同时到达汇合点。
不相交时 c = 0，两个指针会同时变成 None，`pA != pB` 不成立，返回 None —— 边界自动吃掉了。

坑：
  1. 比的是**节点本身**（身份），不是 val。两条链里可能有相同的值但不是同一个节点
  2. 跳转条件写 `pA is None` 而不是 `pA.next is None` —— 要让指针真的走到末尾外面，
     否则 a + c + b 这个等长关系就差一步，不相交的情况会死循环
  3. 不要先算长度再对齐就以为"更直观"：Solution 3 那样写要遍历 4 趟，这个只要 2 趟
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


##################################################################################################
##### ! Solution 1: 双指针路径对齐（走到头就跳到对方的头）
##### ! 时间复杂度: O(m + n)   空间复杂度: O(1)   每个指针最多走 (m + n) 步
##### ! 适用: 本题最优；代码最短，而且"不相交"这个边界不需要任何特判
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution_1:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        pA = headA
        pB = headB

        while pA != pB:
            pA = headB if pA is None else pA.next
            pB = headA if pB is None else pB.next

        return pA
        # Note: In the case lists do not intersect, the pointers for A and B
        # will still line up in the 2nd iteration, just that here won't be
        # a common node down the list and both will reach their respective ends
        # at the same time. So pA will be NULL in that case.


##################################################################################################
##### ! Solution 2: 把 A 的所有节点扔进集合，再走 B 查第一个命中
##### ! 时间复杂度: O(m + n)   空间复杂度: O(m)   集合里装 A 的全部节点
##### ! 适用: 思路零门槛，面试可以先说这个再优化；注意集合里存**节点**不是值（坑 1）
##################################################################################################


class Solution_2:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        seen = set()

        cur = headA
        while cur:
            seen.add(id(cur))  # ! 用 id() 确保比的是身份而不是值
            cur = cur.next

        cur = headB
        while cur:
            if id(cur) in seen:
                return cur
            cur = cur.next

        return None


##################################################################################################
##### ! Solution 3: 先各数一遍长度，长的那条先走差值步，然后同步走
##### ! 时间复杂度: O(m + n)   空间复杂度: O(1)   但要遍历 4 趟（两趟数长度 + 两趟同步走）
##### ! 适用: 最容易向别人解释清楚的版本；代价是比 Solution 1 多走两趟
##################################################################################################


class Solution_3:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        def length(node):
            n = 0
            while node:
                n += 1
                node = node.next
            return n

        la, lb = length(headA), length(headB)

        while la > lb:  # ! 把长的那条先推进差值步，之后两条到末尾的距离就一样了
            headA = headA.next
            la -= 1
        while lb > la:
            headB = headB.next
            lb -= 1

        while headA is not headB:
            headA = headA.next
            headB = headB.next

        return headA


def build(vals: list[int]) -> ListNode | None:
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def attach(head: ListNode | None, tail: ListNode | None) -> ListNode | None:
    """把 tail 接到 head 末尾，返回 head（head 为空就直接返回 tail）。"""
    if not head:
        return tail
    cur = head
    while cur.next:
        cur = cur.next
    cur.next = tail
    return head


if __name__ == "__main__":
    # 每个用例: (A 独有部分, B 独有部分, 共用尾巴)
    cases = [
        ([4, 1], [5, 6, 1], [8, 4, 5]),   # LeetCode 官方例 1，汇合点值为 8
        ([1, 9, 1], [3], [2, 4]),         # 官方例 2
        ([2, 6, 4], [1, 5], []),          # 不相交
        ([], [3], [1, 2]),                # A 的独有部分为空：汇合点就是 headA
        ([3], [], [1, 2]),                # B 的独有部分为空
        ([], [], [7]),                    # 两条完全相同
        ([1], [2], []),                   # 都只有一个节点且不相交
    ]

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        ok = True
        for a_only, b_only, shared in cases:
            tail = build(shared)
            got = sol.getIntersectionNode(attach(build(a_only), tail), attach(build(b_only), tail))
            if got is not tail:  # ! 比身份：shared 为空时 tail 是 None，答案也必须是 None
                ok = False
                print(f"   Solution_{i} 失败: A={a_only} B={b_only} 共用={shared} -> {got and got.val}")
                break
        print(f"Solution_{i}: {'✅ 7 个用例（含不相交、空前缀、完全相同）全过' if ok else '❌'}")
