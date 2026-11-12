"""LC-0019 - Remove Nth Node From End of List

快慢指针的用途：**固定距离**双指针 —— 一趟定位倒数第 n 个
题目在问：删掉倒数第 n 个节点，返回新的头

机关：让 first 比 second 领先 n+1 步，然后两个一起走。
first 走到 None 时，second 正好停在"倒数第 n 个的前驱"上 —— 删节点要的就是前驱。
为什么是 n+1 而不是 n：两个指针都从 dummy 出发，多出的那 1 步就是"前驱"这个偏移。

和 1721（交换正数第 k 和倒数第 k）是同一个机关，区别只在先走几步、停下来拿谁。

坑：
  1. **一定要用 dummy**：删的可能就是 head（n == 链表长度），没有 dummy 就得特判
  2. 先走 n+1 步而不是 n 步 —— 差一格就变成删倒数第 n+1 个。写的时候拿 [1,2] n=1 数一遍
  3. `while first is not None` 而不是 `while first.next`：first 要真的走出链表末尾
"""
# from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# class Solution:
#     def removeNthFromEnd(
#         self, head: Optional[ListNode], n: int
#     ) -> Optional[ListNode]:
#         positions = dict()
#         curr = head
#         length = 0
#         at = 1 # Current index position
#         while curr:
#             positions[at] = curr
#             curr = curr.next
#             at += 1
#             length += 1
#         if n == length:
#             return head.next
#         positions[length - n].next = positions[length - n].next.next
#         return head

##################################################################################################
##### ! Solution 1: 固定距离双指针 + dummy（一趟）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   只遍历一次，不需要知道长度
##### ! 适用: 本题最优，面试标准答案；dummy 把"删 head"这个边界吃掉了，代码没有任何特判
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution_1:
    def removeNthFromEnd(self, head, n):
        """
        :type head: ListNode
        :type n: int
        :rtype: ListNode
        """
        dummy = ListNode(0)
        dummy.next = head
        first = dummy
        second = dummy
        # Advances first pointer so that the gap between first and second is n nodes apart
        for _ in range(n + 1):
            first = first.next
        # Move first to the end, maintaining the gap
        while first is not None:
            first = first.next
            second = second.next
        second.next = second.next.next
        return dummy.next


##################################################################################################
##### ! Solution 2: 先数长度，再走到前驱（两趟）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   走两趟，总步数约 2n
##### ! 适用: 想不清"先走几步"时的保底 —— 下标全部显式算出来，不会错一格
##################################################################################################


class Solution_2:
    def removeNthFromEnd(self, head, n):
        length, cur = 0, head
        while cur:
            length += 1
            cur = cur.next

        if n == length:  # ! 没有 dummy，就得自己特判"删的是 head"
            return head.next

        cur = head
        for _ in range(length - n - 1):  # ! 倒数第 n 个的下标是 length-n，它的前驱是 length-n-1
            cur = cur.next

        cur.next = cur.next.next

        return head


##################################################################################################
##### ! Solution 3: 节点全存进数组，按下标删（上面注释掉那段的可运行版）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)   一个装 n 个节点的数组
##### ! 适用: 需要反复按下标访问节点时才值得；本题纯属多花空间
##################################################################################################


class Solution_3:
    def removeNthFromEnd(self, head, n):
        nodes, cur = [], head
        while cur:
            nodes.append(cur)
            cur = cur.next

        if n == len(nodes):
            return head.next

        nodes[len(nodes) - n - 1].next = nodes[len(nodes) - n].next

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
    def expected(vals, n):
        out = list(vals)
        del out[len(out) - n]
        return out

    cases = [([1, 2, 3, 4, 5], 2), ([1], 1), ([1, 2], 1), ([1, 2], 2), ([1, 2, 3], 3)]

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        ok = all(to_list(sol.removeNthFromEnd(build(c), n)) == expected(c, n) for c, n in cases)

        for length in range(1, 30):  # ! 穷举长度 1..29 x 所有合法 n，覆盖"删 head"和"删尾巴"
            vals = list(range(1, length + 1))
            for n in range(1, length + 1):
                if to_list(sol.removeNthFromEnd(build(vals), n)) != expected(vals, n):
                    ok = False
                    print(f"   Solution_{i} 不一致: length={length} n={n}")
                    break
            if not ok:
                break

        print(f"Solution_{i}: {'✅ 固定用例 + 长度 1..29 x 全部 n 穷举全过' if ok else '❌'}")
