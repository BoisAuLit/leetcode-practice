from ListNode import ListNode


"""
Time complexity: O(n)
Space complexity: O(1)

原理：
在遍历 Linked List 中的每个 Node 的过程中，
逐渐将下一个 Node 的 next 指针指向当前 Node
"""
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev = None # 一开始的 Prev 确实是 None，因为它是左边的空气
        curr = head # Initialize current node to the head
        while curr:
            next_temp = curr.next # 先保存下一个 Node，以后有用
            curr.next = prev # 将下一个 Node 的 next 指针指向上一个 node (prev)
            prev = curr # 重新定义 prev
            curr = next_temp # 重新定义 curr
            
        return prev

