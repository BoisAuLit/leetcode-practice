"""LC-0725 - Split Linked List in Parts（第二轮自主新增）

Level 1 · 05 链表分区、重排与分段操作 —— 定长切分：商与余数决定每段长度
题目在问：把链表切成 k 段，要求
         (1) 任意两段长度相差不超过 1；
         (2) **前面的段不能比后面的段短**；
         (3) 段数不足时补 None。

为什么新增它（补什么缺口）：
  本章其他题（86 / 328 / 25 / 61）都是「按条件分组」或「整体搬运」，
  这道题考的是**精确切断 + 边界算术**：先算清楚每段多长，再准确地在该断的地方 `prev.next = None`。
  「切断链表」这个动作在 LC-0148 Sort List、LC-0025 里都要用，
  但那两题里它被包在递归 / 反转里；这道题把它单独拎出来练，成本低、针对性强。

决定性观察（全在这两行算术里）：
  1. 设链表长度 n，则
        `base, extra = divmod(n, k)`
     前 **extra** 段长度是 `base + 1`，其余段长度是 `base`。
     这正好满足「相差不超过 1」且「前面的不短于后面的」。
  2. `n < k` 时 `base == 0`，后面 `k - n` 段长度为 0 ⟹ 自然就是 None，**不需要特判**。
  3. 切断的写法：走 `size` 步到这一段的最后一个节点，
     **先记下 `nxt = cur.next`，再 `cur.next = None`**，然后从 nxt 继续。
     顺序反了就把后面整条链丢了。

Loop Invariant：处理完第 i 段后，`cur` 指向第 i+1 段的第一个节点，
      前 i 段都已经各自以 None 结尾、互不相连。

复杂度：O(n + k) 时间（一趟数长度 + 一趟切分），O(k) 空间（输出数组）。

边界：
  - [1,2,3], k=5 → [[1],[2],[3],[],[]]（后两段是 None）
  - [1,2,3,4,5,6,7,8,9,10], k=3 → [[1,2,3,4],[5,6,7],[8,9,10]]（extra=1，第一段多一个）
  - head = None → k 个 None
  - k == 1 → 整条链
  - n 恰好被 k 整除 → extra == 0，所有段等长
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
##### ! Solution 1: 先数长度 → divmod 算每段长度 → 走到段尾精确切断
##### ! 时间复杂度: O(n + k)   空间复杂度: O(k)
##### ! 适用：所有「把链表均匀切成若干段」的题；核心是 divmod 和「先存 next 再断开」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:
        n = 0
        cur = head
        while cur:
            n += 1
            cur = cur.next
        base, extra = divmod(n, k)         # ! 前 extra 段每段 base+1 个，其余每段 base 个
        res: List[Optional[ListNode]] = []
        cur = head
        for i in range(k):
            size = base + (1 if i < extra else 0)
            res.append(cur if size else None)
            prev = None
            for _ in range(size):          # ! 走 size 步，prev 停在这一段的最后一个节点
                prev = cur
                cur = cur.next
            if prev:
                prev.next = None           # ! cur 已经前进过了，这里切断不会丢后面的链
        return res


##################################################################################################
##### ! Solution 2: 先把值收集到数组，再按同样的 divmod 规则重建每一段
##### ! 时间复杂度: O(n + k)   空间复杂度: O(n)
##### ! 适用：想绕开「切断顺序」这个坑；也最容易一眼看出分段长度算对没有
##################################################################################################


class Solution_2:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:
        vals = ListNode.to_list(head)
        base, extra = divmod(len(vals), k)
        res, idx = [], 0
        for i in range(k):
            size = base + (1 if i < extra else 0)
            res.append(ListNode.from_list(vals[idx:idx + size]) if size else None)
            idx += size
        return res


if __name__ == "__main__":
    import random

    cases = [([1, 2, 3], 5), ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3), ([], 3),
             ([1], 1), ([1, 2, 3, 4], 2), ([1, 2, 3, 4, 5], 5)]
    for vals, k in cases:
        a = [ListNode.to_list(p) for p in Solution_1().splitListToParts(ListNode.from_list(vals), k)]
        b = [ListNode.to_list(p) for p in Solution_2().splitListToParts(ListNode.from_list(vals), k)]
        assert a == b, (vals, k, a, b)
        # ! 三条题目规则逐条验证
        sizes = [len(p) for p in a]
        assert sum(sizes) == len(vals), (vals, k)
        assert max(sizes) - min(sizes) <= 1, (vals, k, sizes)      # 相差不超过 1
        assert sizes == sorted(sizes, reverse=True), (vals, k, sizes)  # 前面的不短于后面的
        assert len(a) == k
        print(f"{vals}, k={k} -> {a}")

    for _ in range(1000):
        vals = list(range(random.randint(0, 12)))
        k = random.randint(1, 8)
        a = [ListNode.to_list(p) for p in Solution_1().splitListToParts(ListNode.from_list(vals), k)]
        b = [ListNode.to_list(p) for p in Solution_2().splitListToParts(ListNode.from_list(vals), k)]
        assert a == b, (vals, k, a, b)
        sizes = [len(p) for p in a]
        assert len(a) == k and sum(sizes) == len(vals)
        assert (max(sizes) - min(sizes) <= 1) and sizes == sorted(sizes, reverse=True), (vals, k, sizes)
        assert [v for p in a for v in p] == vals          # ! 顺序和内容都不能变
    print("随机对拍 1000 组通过 ✓（段长、顺序、总数全部校验）")
