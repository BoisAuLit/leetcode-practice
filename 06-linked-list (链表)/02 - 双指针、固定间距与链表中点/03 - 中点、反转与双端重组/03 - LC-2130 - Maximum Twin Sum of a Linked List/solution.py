"""LC-2130 - Maximum Twin Sum of a Linked List

快慢指针的用途：找中点，把链表劈成两半，反转后半段，然后双指针并行
题目在问：n 是偶数，下标 i 和 n-1-i 是一对"孪生"，求最大的孪生和

这题是 0234（回文链表）的同一个骨架，只是最后一步从"逐个比较"换成"逐个相加取最大"：
    0234: while prev: if head.val != prev.val: return False
    2130: while prev: best = max(best, head.val + prev.val)
把这两题放在一起记，等于一次背会两道。

坑：
  1. n 保证是偶数，所以 `while fast and fast.next` 之后 slow 正好是后半段的头，不用额外处理奇数
  2. 反转后半段会把第一半最后那个节点的 next 指成反转段的尾巴 —— 不用管，
     因为循环条件是 `while prev`（走 n/2 步就停），不会越界读到脏指针
  3. 面试里被问"能不能不破坏原链表"：那就上 Solution 2（O(n) 空间），或者反转完再反转回去
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


##################################################################################################
##### ! Solution 1: 快慢指针找中点 + 反转后半段 + 并行相加
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   找中点 n/2 步、反转 n/2 步、相加 n/2 步
##### ! 适用: 本题最优；和 0234 共用骨架，是这个文件夹的核心套路
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution_1:
    def pairSum(self, head: ListNode | None) -> int:
        # ① 找中点：n 是偶数，所以 slow 停在后半段的头（下标 n/2）
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # ② 原地反转后半段，prev 最后指向反转段的头（也就是原来的尾节点）
        prev = None
        while slow:
            slow.next, prev, slow = prev, slow, slow.next

        # ③ 两条链并行走 n/2 步，每一步就是一对孪生
        best = 0
        while prev:
            best = max(best, head.val + prev.val)
            head, prev = head.next, prev.next

        return best


##################################################################################################
##### ! Solution 2: 全部值存进数组，下标 i 配 n-1-i
##### ! 时间复杂度: O(n)   空间复杂度: O(n)   一个长度 n 的数组
##### ! 适用: 不许破坏原链表、或者只想快速过题时；思路零门槛
##################################################################################################


class Solution_2:
    def pairSum(self, head: ListNode | None) -> int:
        vals, cur = [], head
        while cur:
            vals.append(cur.val)
            cur = cur.next

        n = len(vals)

        return max(vals[i] + vals[n - 1 - i] for i in range(n // 2))


##################################################################################################
##### ! Solution 3: 前半段压栈，后半段边走边弹
##### ! 时间复杂度: O(n)   空间复杂度: O(n / 2) = O(n)   只存一半，常数比 Solution 2 小一倍
##### ! 适用: "栈天然就是反转"的思路演示；仍然不如 Solution 1 的 O(1)
##################################################################################################


class Solution_3:
    def pairSum(self, head: ListNode | None) -> int:
        slow = fast = head
        stack = []

        while fast and fast.next:  # ! 边找中点边把前半段压栈，一趟干两件事
            stack.append(slow.val)
            slow = slow.next
            fast = fast.next.next

        best = 0
        while slow:  # ! slow 是后半段的头；栈顶正好是它的孪生
            best = max(best, slow.val + stack.pop())
            slow = slow.next

        return best


def build(vals: list[int]) -> ListNode | None:
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


if __name__ == "__main__":
    import random

    def expected(vals):
        n = len(vals)
        return max(vals[i] + vals[n - 1 - i] for i in range(n // 2))

    cases = [[5, 4, 2, 1], [4, 2, 2, 3], [1, 100000], [1, 2, 3, 4, 5, 6]]

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        ok = all(sol.pairSum(build(c)) == expected(c) for c in cases)

        rng = random.Random(0)  # ! 随机对拍：长度取偶数（题目保证）
        for _ in range(2000):
            c = [rng.randint(1, 50) for _ in range(2 * rng.randint(1, 8))]
            if sol.pairSum(build(c)) != expected(c):
                ok = False
                print(f"   Solution_{i} 不一致: {c}")
                break

        print(f"Solution_{i}: {'✅ 固定用例 + 2000 组随机对拍全过' if ok else '❌'}")
