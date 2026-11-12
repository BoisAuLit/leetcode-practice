"""LC-0876 - Middle of the Linked List

快慢指针的"Hello World" —— 本文件夹所有题的地基
题目在问：返回链表的中间节点；长度是偶数时返回**第二个**中点

快慢指针为什么能找中点：fast 的速度是 slow 的两倍，fast 走到尽头时 slow 正好走了一半。
一趟搞定，不需要先数长度。

唯一的坑：循环条件决定你拿到哪个中点（偶数长度时）
    while fast and fast.next:        → slow 停在第二个中点  ← 本题要这个
    while fast.next and fast.next.next: → slow 停在第一个中点（反转后半段的题要这个，见 0234 / 2130）
记法：条件里检查谁，slow 就偏向谁的反方向。写错了不会崩，只会答案偏一格，所以要当场数一遍 [1,2,3,4]。
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


##################################################################################################
##### ! Solution 1: 快慢指针（一趟）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   fast 走 n 步，slow 走 n/2 步
##### ! 适用: 本题最优；也是 0234 / 0143 / 0148 / 2095 / 2130 / 0109 的第一步
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution_1:
    def middleNode(self, head: ListNode | None) -> ListNode | None:
        slow = fast = head

        # ! fast 每次走 2 步，所以要同时保证 fast 和 fast.next 都存在
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow


##################################################################################################
##### ! Solution 2: 先数长度，再走 n // 2 步（两趟）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   走两趟，总步数 1.5n，比快慢指针多
##### ! 适用: 想不起快慢指针时的保底；思路直白但要遍历两次
##################################################################################################


class Solution_2:
    def middleNode(self, head: ListNode | None) -> ListNode | None:
        n, cur = 0, head
        while cur:
            n += 1
            cur = cur.next

        cur = head
        for _ in range(n // 2):  # ! n // 2 对偶数长度正好落在第二个中点
            cur = cur.next

        return cur


##################################################################################################
##### ! Solution 3: 节点全存进数组，直接取下标
##### ! 时间复杂度: O(n)   空间复杂度: O(n)   多了一个长度 n 的数组
##### ! 适用: 需要反复随机访问链表节点时才值得；本题纯属浪费空间
##################################################################################################


class Solution_3:
    def middleNode(self, head: ListNode | None) -> ListNode | None:
        nodes = []
        while head:
            nodes.append(head)
            head = head.next

        return nodes[len(nodes) // 2]


def build(vals: list[int]) -> ListNode | None:
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: ListNode | None) -> list[int]:
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4, 5], [3, 4, 5]),        # 奇数：正中间
        ([1, 2, 3, 4, 5, 6], [4, 5, 6]),     # 偶数：第二个中点（坑）
        ([1], [1]),
        ([1, 2], [2]),
    ]

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        got = [to_list(sol.middleNode(build(vals))) for vals, _ in cases]
        want = [w for _, w in cases]
        print(f"Solution_{i}: {'✅' if got == want else f'❌ {got} != {want}'}")
