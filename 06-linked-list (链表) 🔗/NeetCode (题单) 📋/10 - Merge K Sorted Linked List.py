"""
📌 信号→模式: 合并 k 个有序链表 → 小根堆放 (val, idx, node)；或分治两两合并
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List, Optional
import heapq


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeKLists(
        self, lists: List[Optional[ListNode]]
    ) -> Optional[ListNode]:

        min_heap = []

        for node in lists:
            if node:
                heapq.heappush(min_heap, (node.val, id(node), node))

        dummy = prev = ListNode()

        while min_heap:
            node = heapq.heappop(min_heap)[2]
            if node.next:
                heapq.heappush(
                    min_heap, (node.next.val, id(node.next), node.next)
                )

            prev.next = node
            prev = node

        return dummy.next
