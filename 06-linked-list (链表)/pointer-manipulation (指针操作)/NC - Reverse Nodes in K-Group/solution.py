from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:

        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            # 找到当前组的第 k 个节点
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if not kth:
                    return dummy.next

            # 当前组之后的第一个节点
            group_next = kth.next

            # 反转当前组
            prev = group_next
            curr = group_prev.next

            while curr != group_next:
                next_node = curr.next
                curr.next = prev
                prev = curr
                curr = next_node

            # 连接前一组和当前组
            old_group_head = group_prev.next
            group_prev.next = kth

            # 原来的组头反转后成为组尾
            group_prev = old_group_head
