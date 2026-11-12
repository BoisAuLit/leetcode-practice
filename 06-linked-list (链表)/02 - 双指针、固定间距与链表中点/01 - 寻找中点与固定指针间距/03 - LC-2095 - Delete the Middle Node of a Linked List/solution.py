"""LC-2095 - Delete the Middle Node of a Linked List

快慢指针的用途：找中点的**前驱**（删节点必须拿到前驱，单链表没法回头）
题目在问：删掉下标 ⌊n/2⌋ 的节点（0-indexed），返回新的头

和 0876 的差别：0876 只要中点本身，这题要中点的前一个。两种拿法：
    拿法 A：额外维护一个 prev 跟在 slow 后面（最通用，任何"删 slow"的题都能用）
    拿法 B：让 fast 从 head.next.next 起步，slow 自然就停在前驱（最短，但只适用于这一类）

坑：
  1. n == 1 时中点就是 head，删完链表为空 → 必须特判 return None，否则 prev 是 None 会崩
  2. 删的是 ⌊n/2⌋ 不是 ⌈n/2⌉：n = 4 删下标 2（第三个），自己数一遍 [1,2,3,4] → [1,2,4]
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


##################################################################################################
##### ! Solution 1: 快慢指针 + prev 跟在 slow 后面
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   一趟
##### ! 适用: 最通用的写法 —— 任何"遍历到某个节点然后删掉它"的题都是这个骨架，优先记这个
##################################################################################################

class Solution_1:
    def deleteMiddle(self, head: ListNode | None) -> ListNode | None:
        if not head or not head.next:  # ! 坑 1: 只有一个节点，删完就空了
            return None

        prev, slow, fast = None, head, head

        while fast and fast.next:  # ! 和 0876 一样的条件 → slow 停在第二个中点 = 要删的那个
            prev = slow
            slow = slow.next
            fast = fast.next.next

        prev.next = slow.next  # ! 跳过 slow，它就被摘下来了

        return head


##################################################################################################
##### ! Solution 2: fast 预走两步，slow 直接停在前驱
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   一趟，比 Solution 1 少一个指针
##### ! 适用: 本题最简洁；原理是让 fast 领先 2 格，fast 到头时 slow 刚好差一格没到中点
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def deleteMiddle(self, head: ListNode | None) -> ListNode | None:
        if not head or not head.next:
            return None

        slow, fast = head, head.next.next  # ! 预走两步 = 把"前驱"这件事编码进起始偏移里

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        slow.next = slow.next.next

        return head


##################################################################################################
##### ! Solution 3: 先数长度，再走 n // 2 - 1 步到前驱
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   走两趟，总步数 1.5n
##### ! 适用: 想不起偏移怎么设时的保底写法；下标算得清楚，不容易错一格
##################################################################################################


class Solution_3:
    def deleteMiddle(self, head: ListNode | None) -> ListNode | None:
        n, cur = 0, head
        while cur:
            n += 1
            cur = cur.next

        if n == 1:
            return None

        cur = head
        for _ in range(n // 2 - 1):  # ! 走到下标 n//2 - 1，也就是要删那个的前驱
            cur = cur.next

        cur.next = cur.next.next

        return head


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
    def expected(vals):
        if len(vals) <= 1:
            return []
        return vals[: len(vals) // 2] + vals[len(vals) // 2 + 1 :]

    cases = [[1, 3, 4, 7, 1, 2, 6], [1, 2, 3, 4], [2, 1], [1], [1, 2, 3]]

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        ok = all(to_list(sol.deleteMiddle(build(c))) == expected(c) for c in cases)

        for n in range(1, 60):  # ! 穷举长度 1..59，和直接切片的答案比
            c = list(range(n))
            if to_list(sol.deleteMiddle(build(c))) != expected(c):
                ok = False
                print(f"   Solution_{i} 在长度 {n} 上不一致")
                break

        print(f"Solution_{i}: {'✅ 固定用例 + 长度 1..59 穷举全过' if ok else '❌'}")
