from ListNode import ListNode


"""
Time complexity: O(n+m)
Space complexity: O(1)

我们将侧重点放在两个 Linked List 的开头之上，
这样可以简化很多步骤
"""

class Solution:
    def mergeTwoLists(self, l1, l2):
        # maintain an unchanging reference to node ahead of the return node.
        dummy = ListNode(-1)

        prev = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                prev.next = l1
                l1 = l1.next
            else:
                prev.next = l2
                l2 = l2.next
            prev = prev.next

        # At least one of l1 and l2 can still have nodes at this point, so connect
        # the non-null list to the end of the merged list.
        prev.next = l1 if l1 is not None else l2

        return dummy.next
