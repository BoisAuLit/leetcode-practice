class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def hasCycle(head: ListNode):
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return True

    return False


def detectCycle(head: ListNode):
    slow = fast = head

    # Phase 1: 找到第一次相遇点
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            break
    else:
        return None

    # Phase 2: 找到环入口
    slow = head

    while slow is not fast:
        slow = slow.next
        fast = fast.next

    return slow
