"""LC-0086 - Partition List

Level 1 · 05 链表分区、重排与分段操作 —— Stable Partition（稳定分区）
题目在问：按 x 把链表分成两部分，`< x` 的全部排在 `>= x` 的前面，
         **且两组内部必须保持原有相对顺序**（这就是「稳定」）。

决定性观察：
  1. 想在**一条**链上原地交换节点会非常痛苦。
     正确做法是**开两条新链**：`small` 和 `large`，各带一个 dummy 和一个 tail。
     扫一遍原链，按 `val < x` 分别尾插，最后把 small 的尾接到 large 的头。
  2. **尾插天然就是稳定的** —— 后来的永远排在后来，相对顺序自动保持。
     这是为什么这题根本不需要「稳定排序」这种复杂手段。
  3. **收尾那一行 `large_tail.next = None` 绝对不能忘**：
     large 的最后一个节点仍然挂着它在原链里的旧 `next`，
     不切断就会形成**环**或者把已经搬到 small 的节点重新接回来。
     这是本题唯一真正的坑。

Loop Invariant：扫描到第 i 个节点时，
      small 链是前 i 个里所有 `< x` 的（按原序），large 链是前 i 个里所有 `>= x` 的（按原序）。

两个 dummy 的作用：省掉「这条链还是空的吗」这个判断，直接 `tail.next = node; tail = node`。

复杂度：O(n) 时间，O(1) 额外空间（只搬指针，不新建节点）。

和 LC-0328 Odd Even Linked List 的关系：
      **完全同一个骨架** —— 拆成两条链、各自维护 tail、最后拼接。
      区别只在分组条件：86 按**值**和 x 比较，328 按**位置**的奇偶。
      不要把它们记成两道题。

边界：
  - [1,4,3,2,5,2], x=3 → [1,2,2,4,3,5]
  - 所有元素都 < x → large 为空
  - 所有元素都 >= x → small 为空
  - [] → []
  - 单节点
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    @staticmethod
    def from_list(values: List[int]) -> Optional["ListNode"]:
        dummy = ListNode()
        cur = dummy
        for v in values:
            cur.next = ListNode(v)
            cur = cur.next
        return dummy.next

    @staticmethod
    def to_list(head: Optional["ListNode"]) -> List[int]:
        out = []
        while head:
            out.append(head.val)
            head = head.next
        return out


##################################################################################################
##### ! Solution 1: 两条链 + 两个 dummy，尾插后拼接（和 LC-0328 同骨架）
##### ! 时间复杂度: O(n)   空间复杂度: O(1) 额外
##### ! 适用：一切「按条件把链表拆成两组、组内保序」的题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        small_dummy, large_dummy = ListNode(), ListNode()
        small, large = small_dummy, large_dummy
        cur = head
        while cur:
            if cur.val < x:
                small.next = cur
                small = cur
            else:
                large.next = cur
                large = cur
            cur = cur.next
        large.next = None                 # ! 必须切断！否则会成环或把 small 的节点接回来
        small.next = large_dummy.next     # ! 拼接：小的在前，大的在后
        return small_dummy.next


##################################################################################################
##### ! Solution 2: 收集两组值后重建新链（不复用原节点）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：想绕开「忘记切断尾巴」这个坑时；但面试更希望看到 Solution_1
##################################################################################################


class Solution_2:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        small, large = [], []
        cur = head
        while cur:
            (small if cur.val < x else large).append(cur.val)
            cur = cur.next
        return ListNode.from_list(small + large)


##################################################################################################
##### ! Solution 3: 用 Python 稳定排序的 key 技巧（基准答案，用来对拍）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：正确性参照 —— sorted 是稳定的，正好验证「组内保序」这个要求
##################################################################################################


class Solution_3:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        vals = ListNode.to_list(head)
        return ListNode.from_list(sorted(vals, key=lambda v: 0 if v < x else 1))


if __name__ == "__main__":
    import random

    cases = [([1, 4, 3, 2, 5, 2], 3), ([2, 1], 2), ([], 1), ([1], 1), ([5, 4, 3], 1), ([1, 2, 3], 99)]
    for vals, x in cases:
        a = ListNode.to_list(Solution_1().partition(ListNode.from_list(vals), x))
        b = ListNode.to_list(Solution_2().partition(ListNode.from_list(vals), x))
        c = ListNode.to_list(Solution_3().partition(ListNode.from_list(vals), x))
        assert a == b == c, (vals, x, a, b, c)
        print(f"{vals}, x={x} -> {a}")

    # ! 专门检查「结果链表没有成环」—— 忘了 large.next = None 就会在这里被抓住
    def has_cycle(h):
        slow = fast = h
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
            if slow is fast:
                return True
        return False

    for _ in range(1000):
        vals = [random.randint(0, 8) for _ in range(random.randint(0, 9))]
        x = random.randint(0, 9)
        r = Solution_1().partition(ListNode.from_list(vals), x)
        assert not has_cycle(r), (vals, x)
        a = ListNode.to_list(r)
        b = ListNode.to_list(Solution_2().partition(ListNode.from_list(vals), x))
        c = ListNode.to_list(Solution_3().partition(ListNode.from_list(vals), x))
        assert a == b == c, (vals, x, a, b, c)
    print("随机对拍 1000 组通过 ✓（含无环检查）")
