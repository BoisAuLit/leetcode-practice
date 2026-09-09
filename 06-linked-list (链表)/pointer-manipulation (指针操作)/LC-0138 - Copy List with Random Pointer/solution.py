"""LC-0138 - Copy List with Random Pointer

合并自 2 个解法文件:
  1. 14 - 0138 - A - Copy List Random Pointer - O(N) - O(N).py
  2. 14 - 0138 - B - Copy List Random Pointer - O(N) - O(1).py
"""

from typing import Optional


# ============================================================================
# Solution 1: A    (原文件: 14 - 0138 - A - Copy List Random Pointer - O(N) - O(N).py)
# ============================================================================

class Node_1:
    def __init__(self, x: int, next: "Node_1" = None, random: "Node_1" = None):
        self.val = int(x)
        self.next = next
        self.random = random

    @staticmethod
    def from_list(list_):
        head = Node_1()
        curr = head
        for number in list_:
            new_node = Node_1(number)
            curr.next = new_node
            curr = new_node
        return head.next

    @staticmethod
    def print_list_node(ln: "Node_1"):
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

class Solution_1_A:
    def copyRandomList(self, head: "Optional[Node_1]") -> "Optional[Node_1]":
        if not head:
            return None
        curr = head
        mapping = dict()
        prev = dummy = Node_1(0)

        while curr:
            new_node = Node_1(curr.val)
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

# ============================================================================
# Solution 2: B    (原文件: 14 - 0138 - B - Copy List Random Pointer - O(N) - O(1).py)
# ============================================================================

class Node_2:
    def __init__(self, x: int, next: "Node_2" = None, random: "Node_2" = None):
        self.val = int(x)
        self.next = next
        self.random = random

class Solution_2_B:
    def copyRandomList(self, head: "Optional[Node_2]") -> "Optional[Node_2]":
        if not head:
            return head

        # Creating a new weaved list of original and copied nodes.
        p1 = head
        while p1:
            # Cloned node
            new_node = Node_2(p1.val, None, None)

            # Inserting the cloned node just next to the original node.
            # If A->B->C is the original linked list,
            # Linked list after weaving cloned nodes would be A->A'->B->B'->C->C'
            new_node.next = p1.next
            p1.next = new_node
            p1 = new_node.next

        p1 = head

        # Now link the random pointers of the new nodes created.
        # Iterate the newly created list and use the original nodes random pointers,
        # to assign references to random pointers for cloned nodes.
        while p1:
            p1.next.random = p1.random.next if p1.random else None
            p1 = p1.next.next

        # Unweave the linked list to get back the original linked list and the cloned list.
        # i.e. A->A'->B->B'->C->C' would be broken to A->B->C and A'->B'->C'
        p1 = head  # A->B->C
        p2 = head.next  # A'->B'->C'
        result = head.next
        while p1:
            p1.next = p1.next.next
            p2.next = p2.next.next if p2.next else None
            p1 = p1.next
            p2 = p2.next
        return result


if __name__ == "__main__":

    # --- Solution 1: A ---
    n1 = Node_1(7)
    n2 = Node_1(13)
    n3 = Node_1(11)
    n4 = Node_1(10)
    n5 = Node_1(1)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n2.random = n1
    n3.random = n5
    n4.random = n3
    n5.random = n1
    s = Solution_1_A()
    result = s.copyRandomList(n1)
    Node_1.print_list_node(result)
