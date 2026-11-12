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


from typing import Optional, Tuple


class Solution:
    # Reverse a segment of LinkedList
    # Return [finished, new_head, new_tail]
    def reverseSingleGroup(
        self, head: ListNode, k: int
    ) -> Tuple[bool, ListNode, ListNode]:
        tail = head
        curr = head
        prev = None
        for _ in range(k):
            if not curr:
                return True, prev, None
            tmp_next = curr.next
            curr.next = prev
            prev = curr
            curr = tmp_next
        tail.next = curr
        return False, prev, tail

    def reverseKGroup(
        self, head: Optional[ListNode], k: int
    ) -> Optional[ListNode]:
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy
        curr = head
        while True:
            finished, new_head, new_tail = self.reverseSingleGroup(curr, k)
            if finished:
                self.reverseSingleGroup(new_head, k)
                break
            prev.next = new_head
            curr = new_tail.next
            prev = new_tail
        return dummy.next


s = Solution()

node = ListNode.from_list([1, 2, 3, 4, 5])
k = 2
result = s.reverseKGroup(node, k)
ListNode.print_list_node(result)
