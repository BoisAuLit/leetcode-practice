from typing import Optional


# Definition for a Node.
class Node:
    def __init__(self, x: int, next: "Node" = None, random: "Node" = None):
        self.val = int(x)
        self.next = next
        self.random = random

    @staticmethod
    def from_list(list_):
        head = Node()
        curr = head
        for number in list_:
            new_node = Node(number)
            curr.next = new_node
            curr = new_node
        return head.next

    @staticmethod
    def print_list_node(ln: "Node"):
        if ln is None:
            print("Empty ListNode")
            return
        list_ = []
        while ln is not None:
            if ln.random is not None:
                list_.append((ln.val, ln.random.val))
            else:
                list_.append(ln.val)
            ln = ln.next
        print("ListNode ->", list_)


class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if not head:
            return None
        curr = head
        mapping = dict()
        prev = dummy = Node(0)

        while curr:
            new_node = Node(curr.val)
            id1 = id(curr)
            mapping[id1] = {
                "rand_id": id(curr.random),
                "corr_id": new_node,
            }

            prev.next = new_node
            prev = new_node
            curr = curr.next

        n1 = head
        n2 = dummy.next

        while n1:
            entry = mapping[id(n1)]
            if entry["rand_id"] != id(None):
                n2.random = mapping[entry["rand_id"]]["corr_id"]
            n1 = n1.next
            n2 = n2.next
        return dummy.next


n1 = Node(7)
n2 = Node(13)
n3 = Node(11)
n4 = Node(10)
n5 = Node(1)

n1.next = n2
n2.next = n3
n3.next = n4
n4.next = n5

n2.random = n1
n3.random = n5
n4.random = n3
n5.random = n1

# Node.print_list_node(n1)

s = Solution()
result = s.copyRandomList(n1)
Node.print_list_node(result)
