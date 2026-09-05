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
