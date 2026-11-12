"""LC-0143 - Reorder List

快慢指针的用途：找中点，反转后半段，然后交替穿插
题目在问：把 L0→L1→…→Ln 重排成 L0→Ln→L1→Ln-1→…（原地改，不返回）

三步走，和 0234 / 2130 是同一个骨架，只是最后一步换成"穿插"：
    ① 快慢指针找第一个中点  ② 反转后半段  ③ 两条链交替接起来

坑：
  1. 要的是**第一个**中点（`while fast.next and fast.next.next`）。
     用第二个中点的话，奇数长度时正中间那个节点会被分到后半段，穿插完顺序就错了
  2. 劈开后一定要 `slow.next = None`，否则前半段还连着后半段，穿插时会绕回去形成环
  3. 穿插时必须**先把两个 next 存下来**再改指针，顺序写错就断链：
         nxt1, nxt2 = first.next, second.next   ← 先存
         first.next = second; second.next = nxt1 ← 再改
  4. 循环条件用 `while second`：前半段长度 >= 后半段，所以后半段先走完
"""
from collections import deque
from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


##################################################################################################
##### ! Solution 1: 全部节点进 deque，两头交替弹
##### ! 时间复杂度: O(n)   空间复杂度: O(n)   一个装 n 个节点的 deque
##### ! 适用: 思路最直白 —— "要的就是首尾交替"，deque 两头弹正好对应。面试可以先给这个
##################################################################################################

class Solution_1:
    def reorderList(self, head: Optional[ListNode]) -> None:
        dq = deque()
        while head:
            dq.append(head)
            head = head.next
        prev = ListNode()
        isLeft = True
        while dq:
            node = dq.popleft() if isLeft else dq.pop()
            node.next = None
            prev.next = node
            prev = prev.next
            isLeft = not isLeft


##################################################################################################
##### ! Solution 2: 快慢指针找中点 + 反转后半段 + 交替穿插
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   ★ 空间优于 Solution 1，不存任何节点
##### ! 适用: 本题最优，也是面试官真正想看的答案；本文件夹要练的就是这个三步骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next:
            return

        # ① 找第一个中点（坑 1）：slow 停在前半段的末尾
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # ② 劈开并反转后半段（坑 2）
        second, slow.next = slow.next, None
        prev = None
        while second:
            second.next, prev, second = prev, second, second.next

        # ③ 交替穿插（坑 3、坑 4）：前半段 head…，后半段反转后 prev…
        first, second = head, prev
        while second:
            nxt1, nxt2 = first.next, second.next  # ! 先存，再改指针
            first.next = second
            second.next = nxt1
            first, second = nxt1, nxt2


##################################################################################################
##### ! Solution 3: 快慢指针找中点 + 后半段压栈 + 穿插
##### ! 时间复杂度: O(n)   空间复杂度: O(n / 2) = O(n)   只存后半段，常数是 Solution 1 的一半
##### ! 适用: 不想手写反转链表时的折中 —— 栈天然就是反转，省掉 ② 那段指针操作
##################################################################################################


class Solution_3:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next:
            return

        slow, fast = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        stack, cur = [], slow.next
        slow.next = None
        while cur:  # ! 压栈 = 反转，弹出顺序就是从尾往前
            stack.append(cur)
            cur = cur.next

        first = head
        while stack:
            nxt = first.next
            first.next = stack.pop()
            first.next.next = nxt
            first = nxt


def build(vals: list[int]) -> Optional[ListNode]:
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode], cap: int = 10000) -> list[int]:
    """cap 防死循环：穿插写错很容易产生环，没有上限测试会挂住。"""
    out = []
    while head and len(out) <= cap:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    def expected(vals):
        out, i, j = [], 0, len(vals) - 1
        while i <= j:
            out.append(vals[i])
            if i != j:
                out.append(vals[j])
            i += 1
            j -= 1
        return out

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        ok = True
        for n in range(0, 40):  # ! 穷举长度 0..39（奇偶都覆盖）
            vals = list(range(1, n + 1))
            node = build(vals)
            sol.reorderList(node)
            got = to_list(node)
            if got != expected(vals):
                ok = False
                print(f"   Solution_{i} 在长度 {n} 上失败: {got} != {expected(vals)}")
                break
        print(f"Solution_{i}: {'✅ 长度 0..39 穷举全过' if ok else '❌'}")
