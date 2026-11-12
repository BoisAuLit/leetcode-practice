class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


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

##################################################################################################
##### ! Solution NC: NC 版：dummy + 尾插，收尾用 `node.next = list1 or list2`
##### ! 时间复杂度: O(m + n)   空间复杂度: O(1)
##### ! 和本文件已有解法同一个思路；收尾一行 `node.next = list1 or list2` 比 while 循环更简洁。
##### ! 来源：原 `NC - ...` 目录。按仓库规则「LC / NC 重复时只保留 LeetCode 版」，
#####   原 NC 文件夹已删除，但它的实现一字未改地并入这里，没有丢失任何代码。
##################################################################################################


class Solution_NC:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        dummy = node = ListNode()

        while list1 and list2:
            if list1.val < list2.val:
                node.next = list1
                list1 = list1.next
            else:
                node.next = list2
                list2 = list2.next
            node = node.next

        node.next = list1 or list2

        return dummy.next
