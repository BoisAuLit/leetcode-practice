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


from typing import List, Optional
import heapq

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


"""
Time complexity: O(N log k)
Space complexity: O(n)
"""


class Solution:
    def mergeKLists(
        self, lists: List[Optional[ListNode]]
    ) -> Optional[ListNode]:
        # The min heap
        heap = [(node.val, index) for index, node in enumerate(lists) if node]
        heapq.heapify(heap)
        dummy = ListNode(0)
        prev = dummy
        while heap:
            value, index = heapq.heappop(heap)
            new_node = ListNode(value)
            prev.next = new_node
            prev = new_node
            node = lists[index]
            if node.next:
                lists[index] = node.next
                heapq.heappush(heap, (node.next.val, index))
        return dummy.next


s = Solution()
lists = [
    ListNode.from_list([1, 4, 5]),
    ListNode.from_list([1, 3, 4]),
    ListNode.from_list([2, 6]),
]
result = s.mergeKLists(lists)
ListNode.print_list_node(result)

##################################################################################################
##### ! Solution NC: NC 版：堆里直接放原节点 (val, id(node), node) 并**重连原节点**
##### ! 时间复杂度: O(N log k)   空间复杂度: O(k)
##### ! 和本文件已有解法的区别：已有版本把值取出来**新建节点**，用 index 当 tie-breaker；
#####   NC 版直接搬运原节点，用 id(node) 当 tie-breaker 避免比较 ListNode 对象。两种都对。
##### ! 来源：原 `NC - ...` 目录。按仓库规则「LC / NC 重复时只保留 LeetCode 版」，
#####   原 NC 文件夹已删除，但它的实现一字未改地并入这里，没有丢失任何代码。
##################################################################################################


class Solution_NC:
    def mergeKLists(
        self, lists: List[Optional[ListNode]]
    ) -> Optional[ListNode]:

        min_heap = []

        for node in lists:
            if node:
                heapq.heappush(min_heap, (node.val, id(node), node))

        dummy = prev = ListNode()

        while min_heap:
            node = heapq.heappop(min_heap)[2]
            if node.next:
                heapq.heappush(
                    min_heap, (node.next.val, id(node.next), node.next)
                )

            prev.next = node
            prev = node

        return dummy.next
