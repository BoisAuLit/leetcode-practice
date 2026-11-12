"""LC-0234 - Palindrome Linked List

快慢指针的用途：找中点，反转后半段，然后两头并行比较
题目在问：判断链表是不是回文

这是本文件夹的核心骨架，和 2130（孪生和最大）一字之差：
    0234: while n2: if n1.val != n2.val: return False    ← 比较
    2130: while n2: best = max(best, n1.val + n2.val)    ← 相加

坑：
  1. 这里要的是**第一个**中点（第一半的末尾），所以条件是 `while fast.next and fast.next.next`，
     和 0876 的 `while fast and fast.next`（第二个中点）差一格。
     理由：拿到第一半的末尾才能 `first_half_end.next = 反转后的第二半`，把链表接回去
  2. 奇数长度时正中间那个节点归第二半，比较时会自己和自己比，无害，不用特判
  3. 比较完要把链表**还原**（再反转一次接回去）—— 面试官常追问"你破坏了输入怎么办"，
     下面 Solution_1 已经还原了，这是它比大多数题解强的地方
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


##################################################################################################
##### ! Solution 1: 快慢指针找中点 + 反转后半段 + 比较 + 还原
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   找中点 n/2、反转 n/2、比较 n/2、还原 n/2
##### ! 适用: 本题最优。唯一的 O(1) 空间解法，而且比较完把链表还原了，不破坏输入
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution_1:

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


##################################################################################################
##### ! Solution 2: 值倒进数组，双指针两头夹
##### ! 时间复杂度: O(n)   空间复杂度: O(n)   一个长度 n 的数组
##### ! 适用: 最快写出来的版本；面试里可以先给这个，再问"要不要优化到 O(1) 空间"
##################################################################################################


class Solution_2:
    def isPalindrome(self, head: ListNode) -> bool:
        vals = []
        while head:
            vals.append(head.val)
            head = head.next

        i, j = 0, len(vals) - 1
        while i < j:
            if vals[i] != vals[j]:
                return False
            i += 1
            j -= 1

        return True


##################################################################################################
##### ! Solution 3: 快慢指针边走边压栈，后半段边走边弹
##### ! 时间复杂度: O(n)   空间复杂度: O(n / 2) = O(n)   只存前半段，常数比 Solution 2 小一半
##### ! 适用: "栈天然就是反转"的思路；不破坏链表，但空间仍不如 Solution 1
##################################################################################################


class Solution_3:
    def isPalindrome(self, head: ListNode) -> bool:
        stack = []
        slow = fast = head

        while fast and fast.next:  # ! 这里用第二个中点的条件：slow 停在后半段的头
            stack.append(slow.val)
            slow = slow.next
            fast = fast.next.next

        if fast:       # ! 奇数长度：slow 正站在正中间那个，它没有配对的，跳过
            slow = slow.next

        while slow:
            if slow.val != stack.pop():
                return False
            slow = slow.next

        return True


def build(vals: list[int]) -> ListNode | None:
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: ListNode | None) -> list[int]:
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    import random

    cases = [[1, 2, 2, 1], [1, 2], [1], [], [1, 2, 3, 2, 1], [1, 2, 3, 3, 2, 1], [1, 2, 3]]

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        ok = all(sol.isPalindrome(build(c)) == (c == c[::-1]) for c in cases)

        rng = random.Random(0)
        for _ in range(3000):  # ! 随机对拍：和 c == c[::-1] 比
            c = [rng.randint(0, 2) for _ in range(rng.randint(0, 9))]
            if sol.isPalindrome(build(c)) != (c == c[::-1]):
                ok = False
                print(f"   Solution_{i} 不一致: {c}")
                break

        # ! Solution 1 承诺"比较完还原链表"，单独验一下这个承诺
        if i == 1:
            for c in cases:
                node = build(c)
                sol.isPalindrome(node)
                if to_list(node) != c:
                    ok = False
                    print(f"   Solution_1 没有还原链表: {c} -> {to_list(node)}")

        print(f"Solution_{i}: {'✅ 固定用例 + 3000 组随机对拍全过' + (' + 链表已还原' if i == 1 else '') if ok else '❌'}")
