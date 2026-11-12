"""LC-0061 - Rotate List

合并自 2 个解法文件:
  1. 15 - 0061 - A - Rotate List - Iterate once.py
  2. 15 - 0061 - B - Rotate List - Iterate twice.py

快慢指针的用途：固定距离双指针定位"新的尾巴"
题目在问：把链表整体右移 k 位（k 可能远大于链表长度）

为什么这题躲不开"先数长度"：k 要先对 n 取模，不知道 n 就不知道该移几位。
数完长度之后才是快慢指针出场：让 fast 领先 slow 恰好 k 步，fast 到尾巴时 slow 就是新的尾巴。
右移 k 位 = 把倒数第 k 个节点拎出来当新头 → 新尾巴是倒数第 k+1 个 → 正是"领先 k 步"这个偏移。

坑：
  1. **k %= n 必须先做**，否则 k = 52、n = 5 时指针会跑飞
  2. k % n == 0 要直接返回原链表，不然"断开再接回"会把链表拆坏
  3. 接线顺序：先 new_head = slow.next，再 slow.next = None，最后 old_tail.next = head。
     反过来先接 old_tail.next = head 就成环了，再去断就找不到地方断
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    # ! 下面两个是从 06-linked-list (链表)/utils/ListNode.py 搬来的，
    # ! 原来的 __main__ 直接调它们但本文件没定义，一跑就 AttributeError
    @staticmethod
    def from_list(list_: list) -> Optional["ListNode"]:
        head = ListNode()
        curr = head
        for number in list_:
            curr.next = ListNode(number)
            curr = curr.next
        return head.next

    @staticmethod
    def print_list_node(ln: Optional["ListNode"]) -> None:
        if ln is None:
            print("Empty ListNode")
            return
        list_ = []
        while ln is not None:
            list_.append(ln.val)
            ln = ln.next
        print("ListNode ->", list_)


##################################################################################################
##### ! Solution 1: 节点全存进数组，按下标接线
##### !   (原文件: 15 - 0061 - A - Rotate List - Iterate once.py)
##### ! 时间复杂度: O(n)   空间复杂度: O(n)   一个装 n 个节点的数组
##### ! 适用: 一趟就能拿到长度和所有节点，接线时下标算得最清楚，不容易错
##################################################################################################

class Solution_1:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head:
            return head
        
        length = 0
        curr = head
        nodes = []
        while curr:
            length += 1
            nodes.append(curr)
            curr = curr.next
        k %= length
        if k == 0:
            return head
        nodes[length-k-1].next = None
        nodes[-1].next = nodes[0]
        return nodes[length-k]


##################################################################################################
##### ! Solution 2: 走两趟，第一趟数长度找旧尾巴，第二趟按下标找新尾巴
##### !   (原文件: 15 - 0061 - B - Rotate List - Iterate twice.py)
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   不存节点，只用几个指针
##### ! 适用: 空间已经最优；缺点是要显式算 length - k - 1 这个下标，容易错一格
##################################################################################################


class Solution_2:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head:
            return head
        
        length = 0
        curr = head
        old_tail = None
        while curr:
            length += 1
            if not curr.next:
                old_tail = curr
            curr = curr.next
        k %= length
        if k == 0:
            return head
        
        index = 0
        curr = head
        new_tail = None
        while curr:
            if index == length - k - 1:
                new_tail = curr
                break
            index += 1
            curr = curr.next
        new_head = new_tail.next
        new_tail.next = None
        old_tail.next = head
        return new_head


##################################################################################################
##### ! Solution 3: 数长度 + 固定距离双指针找新尾巴
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   和 Solution 2 同阶
##### ! 适用: 本题最优写法 —— 和 Solution 2 一样省空间，但不用算任何下标：
##### !   "让 fast 领先 k 步，fast 到尾巴时 slow 就是新尾巴"，和 0019 / 1721 是同一个机关
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_3:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        # ① 数长度，顺手拿到旧尾巴（k 要取模，长度躲不开）
        n, old_tail = 1, head
        while old_tail.next:
            n += 1
            old_tail = old_tail.next

        k %= n          # ! 坑 1
        if k == 0:      # ! 坑 2
            return head

        # ② 固定距离双指针：fast 领先 k 步
        fast = head
        for _ in range(k):
            fast = fast.next

        slow = head
        while fast.next:  # ! fast 停在尾巴上时，slow 正好是倒数第 k+1 个 = 新尾巴
            fast = fast.next
            slow = slow.next

        # ③ 接线（坑 3：顺序不能换）
        new_head = slow.next
        slow.next = None
        old_tail.next = head

        return new_head


if __name__ == "__main__":

    # --- Solution 1: Iterate_once ---
    s = Solution_1()
    head = ListNode.from_list([1, 2, 3, 4, 5])
    result = s.rotateRight(head, 52)
    ListNode.print_list_node(result)

    # --- Solution 2: Iterate_twice ---
    s = Solution_2()
    head = ListNode.from_list([1, 2, 3, 4, 5])
    result = s.rotateRight(head, 52)
    ListNode.print_list_node(result)

    # --- Solution 3: 固定距离双指针 ---
    s = Solution_3()
    head = ListNode.from_list([1, 2, 3, 4, 5])
    result = s.rotateRight(head, 52)
    ListNode.print_list_node(result)

    # --- 三个解法一起对拍 ---
    def to_list(node, cap=10000):
        out = []
        while node and len(out) <= cap:
            out.append(node.val)
            node = node.next
        return out

    def expected(vals, k):
        if not vals:
            return []
        k %= len(vals)
        return vals[-k:] + vals[:-k] if k else list(vals)

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        ok = True
        for n in range(0, 25):  # ! 穷举长度 0..24 x k 0..30（覆盖 k > n、k % n == 0）
            vals = list(range(1, n + 1))
            for k in range(0, 31):
                if to_list(sol.rotateRight(ListNode.from_list(vals), k)) != expected(vals, k):
                    ok = False
                    print(f"   Solution_{i} 不一致: n={n} k={k}")
                    break
            if not ok:
                break
        print(f"Solution_{i}: {'✅ 长度 0..24 x k 0..30 穷举全过' if ok else '❌'}")
