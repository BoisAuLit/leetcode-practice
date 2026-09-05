from typing import List, Optional
from ListNode import ListNode
import heapq

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


"""
Time complexity: O(N log k)
Space complexity: O(n)
"""


class Solution:
    def mergeKLists(
        self, lists: List[Optional[ListNode]]
    ) -> Optional[ListNode]:
        # The min heap
        heap = [(node.val, index) for index, node in enumerate(lists) if node]
        heapq.heapify(heap)
        dummy = ListNode(0)
        prev = dummy
        while heap:
            value, index = heapq.heappop(heap)
            new_node = ListNode(value)
            prev.next = new_node
            prev = new_node
            node = lists[index]
            if node.next:
                lists[index] = node.next
                heapq.heappush(heap, (node.next.val, index))
        return dummy.next


s = Solution()
lists = [
    ListNode.from_list([1, 4, 5]),
    ListNode.from_list([1, 3, 4]),
    ListNode.from_list([2, 6]),
]
result = s.mergeKLists(lists)
ListNode.print_list_node(result)
