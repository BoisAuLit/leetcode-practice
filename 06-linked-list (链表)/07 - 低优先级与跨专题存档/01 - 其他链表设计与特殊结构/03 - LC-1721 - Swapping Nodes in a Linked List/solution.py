"""LC-1721 - Swapping Nodes in a Linked List

快慢指针的用途：**固定距离**双指针 —— 一趟同时定位"正数第 k 个"和"倒数第 k 个"
题目在问：交换正数第 k 个节点和倒数第 k 个节点，返回新的头

和 0019（删倒数第 n 个）是同一个机关：
    让一个指针先走 k 步，另一个从 head 起步，两者始终相差 k；
    先走的那个到尾巴时，后走的那个就正好在倒数第 k 个上。
这里"先走的指针"停下来的位置本身就是正数第 k 个，所以一趟能同时拿到两个目标，白捡一个。

坑：
  1. 题目只要求交换**值**，所以一句 `a.val, b.val = b.val, a.val` 就完事了，
     千万别一上来就做指针手术（相邻、同一个节点这些情况极容易写错，见 Solution 3）
  2. k 和 n-k+1 可能指同一个节点（k 正好在正中间），交换值时无害，交换节点时必须特判
  3. 先走 k-1 步还是 k 步：想清楚 fast 停在哪。这里要 fast 落在第 k 个节点上，所以走 k-1 步
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


##################################################################################################
##### ! Solution 1: 固定距离双指针，一趟
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   只遍历一次，不需要知道长度
##### ! 适用: 本题最优，也是 0019 的同一套骨架，优先记这个
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution_1:
    def swapNodes(self, head: ListNode | None, k: int) -> ListNode | None:
        fast = head
        for _ in range(k - 1):  # ! 坑 3: 走 k-1 步，fast 落在第 k 个节点上
            fast = fast.next

        first = fast  # ! 正数第 k 个，顺手就拿到了

        slow = head
        while fast.next:  # ! fast 和 slow 始终相差 k；fast 到尾巴时 slow 在倒数第 k 个
            fast = fast.next
            slow = slow.next

        first.val, slow.val = slow.val, first.val  # ! 坑 1: 只换值；坑 2 的同节点情况自动无害

        return head


##################################################################################################
##### ! Solution 2: 先数长度，再分别走到两个位置（两趟）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   走两趟，总步数约 2n
##### ! 适用: 想不清"先走几步"时的保底 —— 下标算得明明白白，不会错一格
##################################################################################################


class Solution_2:
    def swapNodes(self, head: ListNode | None, k: int) -> ListNode | None:
        n, cur = 0, head
        while cur:
            n += 1
            cur = cur.next

        a = head
        for _ in range(k - 1):
            a = a.next

        b = head
        for _ in range(n - k):  # ! 倒数第 k 个 = 正数第 n-k+1 个 = 从 head 走 n-k 步
            b = b.next

        a.val, b.val = b.val, a.val

        return head


##################################################################################################
##### ! Solution 3: 真正交换节点（指针手术），不碰 val
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   和 Solution 1 同阶，但代码长三倍
##### ! 适用: 面试官追问"如果节点里装的是不可改的大对象，只能换节点怎么办"
##### ! 三个必须特判的情况: 两者是同一个节点、两者相邻(a 在前)、两者相邻(b 在前)
##### !   —— 相邻时一个节点的前驱就是另一个节点，按常规写法会把 next 指向自己造成死循环
##################################################################################################


class Solution_3:
    def swapNodes(self, head: ListNode | None, k: int) -> ListNode | None:
        dummy = ListNode(0, head)

        a_prev = dummy
        for _ in range(k - 1):
            a_prev = a_prev.next
        a = a_prev.next

        fast, b_prev = a, dummy
        while fast.next:
            fast = fast.next
            b_prev = b_prev.next
        b = b_prev.next

        if a is b:  # ! 情况 1: 同一个节点，什么都不用做
            return dummy.next

        if a_prev is b:  # ! 情况 3: b 在 a 前面且相邻 → 交换角色，统一成"a 在前"
            a_prev, a, b_prev, b = b_prev, b, a_prev, a

        if b_prev is a:  # ! 情况 2: a, b 相邻且 a 在前
            a.next = b.next  # ! 顺序要紧: 先把 a 的新 next 定下来，再让 b 指向 a
            b.next = a
            a_prev.next = b
        else:  # ! 不相邻: 两个前驱对调，两个 next 对调
            a_prev.next, b_prev.next = b, a
            a.next, b.next = b.next, a.next

        return dummy.next


def build(vals: list[int]) -> ListNode | None:
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: ListNode | None, cap: int = 10000) -> list[int]:
    """cap 是防死循环的保险：指针手术写错会产生环，没有上限的话测试会挂住。"""
    out = []
    while head and len(out) <= cap:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    def expected(vals, k):
        out = list(vals)
        out[k - 1], out[len(out) - k] = out[len(out) - k], out[k - 1]
        return out

    cases = [([1, 2, 3, 4, 5], 2), ([7, 9, 6, 6, 7, 8, 3, 0, 9, 5], 5), ([1], 1), ([1, 2], 1), ([1, 2, 3], 2)]

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        ok = all(to_list(sol.swapNodes(build(c), k)) == expected(c, k) for c, k in cases)

        for n in range(1, 25):  # ! 穷举长度 1..24 x 所有合法 k，覆盖相邻 / 同节点 / 首尾
            c = list(range(1, n + 1))
            for k in range(1, n + 1):
                if to_list(sol.swapNodes(build(c), k)) != expected(c, k):
                    ok = False
                    print(f"   Solution_{i} 不一致: n={n} k={k}")
                    break
            if not ok:
                break

        print(f"Solution_{i}: {'✅ 固定用例 + 长度 1..24 x 全部 k 穷举全过' if ok else '❌'}")
