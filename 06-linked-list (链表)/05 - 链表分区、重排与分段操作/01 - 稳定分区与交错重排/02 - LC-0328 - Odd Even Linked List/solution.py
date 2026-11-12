class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    # ! 下面两个辅助方法是本次重构补上的：原文件底部的示例代码调用了 ListNode.from_list /
    # ! ListNode.print_list_node，但本文件里的 ListNode 没有定义它们，导致整个文件
    # ! AttributeError 跑不起来。定义取自本专题的 _resources/utils/ListNode.py，没有改动任何解法。
    @staticmethod
    def from_list(list_):
        head = ListNode()
        curr = head
        for number in list_:
            curr.next = ListNode(number)
            curr = curr.next
        return head.next

    @staticmethod
    def print_list_node(ln):
        if ln is None:
            print("Empty ListNode")
            return
        out = []
        while ln is not None:
            out.append(ln.val)
            ln = ln.next
        print("ListNode ->", out)


from typing import Optional


class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        odd = head
        even = head.next
        even_head = head.next
        while odd and even:
            if not even.next:
                odd.next = None
                break
            third, fourth = even.next, even.next.next
            odd.next = third
            even.next = fourth
            odd, even = third, fourth
        odd.next = even_head
        return head
        


s = Solution()
head = ListNode.from_list([1, 2, 3, 4, 5])
result = s.oddEvenList(head)
ListNode.print_list_node(result)
