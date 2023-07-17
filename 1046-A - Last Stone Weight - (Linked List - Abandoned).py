# from __future__ import annotations
# from typing import List

# """
# Time complexity: O()
# Space complexity: O()
# """

# class ListNode:
#     def __init__(self, val=0, next_=None):
#         self.val = val
#         self.next = next_

#     @staticmethod
#     def from_list(list_: List[int]) -> ListNode:
#         head = ListNode()
#         curr = head
#         for number in list_:
#             new_node = ListNode(number)
#             curr.next = new_node
#             curr = new_node
#         return head.next

# def insert_linked_list(n: int, head: ListNode[int]) -> ListNode[int]:
#     if n < head.val:
#         node = ListNode(n)
#         node.next = head
#         return node
    
#     prev = current = head

# def smash_last_two(head: ListNode) -> ListNode:
#     tmp = head
#     while tmp.next.next.next:
#         tmp = tmp.next
#     last_but_two = tmp
#     last_but_one = tmp.next
#     last = tmp.next.next
#     diff = abs(last.val, last_but_one.val)
#     # if diff == 0:
#     #     last_but_two.next = None
#     # else:
#     #     head = insert_linked_list(diff, head)
#     return head

# def smash_linked_list(head: ListNode[int]) -> int:
#     if head is None:
#         return 0
#     if head.next is None:
#         return head.val
#     if head.next.next is None:
#         return abs(head.val, head.next.val)
        
#     while head is not None and head.next is not None:
#         head = smash_last_two(head) 



# class Solution:
#     def lastStoneWeight(self, stones: List[int]) -> int:
#         # sorted_stones = sorted(stones)
#         # head = ListNode.from_list(sorted_stones)
#         return 10


        

# s = Solution()
# input_ = [2,7,4,1,8,1] # Expecting 1
# # input_ = [1] # Expecting 1
# result = s.lastStoneWeight(input_)
# print(result)

# """

# """
