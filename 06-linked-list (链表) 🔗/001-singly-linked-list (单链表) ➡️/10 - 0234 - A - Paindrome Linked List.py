from ListNode import ListNode

class Solution:

    def isPalindrome(self, head: ListNode) -> bool:
        if head is None:
            return True
        
        # ! Step 1: Find end of first half using two pointers (slow & fast)
        first_half_end = self.end_of_first_half(head)
        # ! Step 2: Reverse the second half
        # ! (The tail of the original LinkedList will become the start)
        second_half_start = self.reverse_list(first_half_end.next)

        # Check whether or not there's a palindrome.
        result = True
        n1 = head
        n2 = second_half_start
        while result and n2:
            if n1.val != n2.val:
                result = False
            n1 = n1.next
            n2 = n2.next

        # Restore the list and return the result.
        first_half_end.next = self.reverse_list(second_half_start)
        return result    

    def end_of_first_half(self, head: ListNode) -> ListNode:
        fast = head # Hare
        slow = head # Tortoise
        while fast.next and fast.next.next:
            fast = fast.next.next
            slow = slow.next
        return slow

    # ! This is the solution to 0206 - Reverse Linked List
    def reverse_list(self, head: ListNode) -> ListNode:
        previous = None
        current = head
        while current:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        return previous
