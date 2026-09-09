"""LC-0116 - Populating Next Right Pointers in Each Node

合并自 5 个解法文件:
  1. 019 - 0116 - Populating Next Right Pointers.py
  2. 021 - 0116 - Populating Next Right Pointers - (asset).py
  3. 0116 - A - Populating Next - Level Traversal - Level Traversal 🐢.py
  4. 0116 - B - Populating Next - Level Traversal - Linked List 🚀.py
  5. 0116 - C - Populating Next Right Pointers - BFS Queue (older version).py
"""

from typing import Optional

import collections


# ============================================================================
# Solution 1: Populating_Next_Right_Pointers    (原文件: 019 - 0116 - Populating Next Right Pointers.py)
# ============================================================================

# # Definition for a Node_1.

class Node_1:
    def __init__(
        self,
        val: int = 0,
        left: "Node_1" = None,
        right: "Node_1" = None,
        next: "Node_1" = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class Solution_1_Populating_Next_Right_Pointers:
    def connect(self, root: "Optional[Node_1]") -> "Optional[Node_1]":
        if not root:
            return root
        level = [root]
        while True:
            for i in range(0, len(level) - 1):
                level[i].next = level[i + 1]

            next_level = []
            for node in level:
                if not node.left:
                    return root
                next_level.append(node.left)
                next_level.append(node.right)

            level = next_level

# ============================================================================
# Solution 2: asset    (原文件: 021 - 0116 - Populating Next Right Pointers - (asset).py)
# ============================================================================

# # Definition for a Node_2.

class Node_2:
    def __init__(
        self,
        val: int = 0,
        left: "Node_2" = None,
        right: "Node_2" = None,
        next: "Node_2" = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class Solution_2_asset:
    def connect(self, root: "Node_2") -> "Node_2":
        if not root:
            return root
        queue = collections.deque([root])
        while queue:
            size = len(queue)
            for i in range(size):
                node = queue.popleft()
                if i < size - 1:
                    node.next = queue[0]
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return root

# ============================================================================
# Solution 3: Level_Traversal    (原文件: 0116 - A - Populating Next - Level Traversal - Level Traversal 🐢.py)
# ============================================================================

class Node_3:
    def __init__(
        self,
        val: int = 0,
        left: "Node_3" = None,
        right: "Node_3" = None,
        next: "Node_3" = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class Solution_3_Level_Traversal:
    def connect(self, root):
        if not root:
            return root
        level = [root]
        while level[0].left:
            next_level = [y for x in level for y in [x.left, x.right]]
            for idx, node in enumerate(next_level[:-1]):
                node.next = next_level[idx + 1]
            level = next_level
        return root

# ============================================================================
# Solution 4: Linked_List    (原文件: 0116 - B - Populating Next - Level Traversal - Linked List 🚀.py)
# ============================================================================

asset = "../assets/0116.pdf"

# Time complexity: O(N)
# - N is the number of nodes
#
# Space complexity: O(1)

class Node_4:
    def __init__(
        self,
        val: int = 0,
        left: "Node_4" = None,
        right: "Node_4" = None,
        next: "Node_4" = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class Solution_4_Linked_List:
    def connect(self, root: "Node_4") -> "Node_4":
        if not root:
            return root

        # Start with the root node. There are no next pointers
        # that need to be set up on the first level
        leftmost = root

        # Once we reach the final level, we are done
        while leftmost.left:
            # Iterate the "linked list" starting from the head
            # node and using the next pointers, establish the
            # corresponding links for the next level
            head = leftmost
            while head:
                # CONNECTION 1
                head.left.next = head.right

                # CONNECTION 2
                if head.next:
                    head.right.next = head.next.left

                # Progress along the list (nodes on the current level)
                head = head.next

            # Move onto the next level
            leftmost = leftmost.left # ⭐️ This is very important, we reset the leftmost node

        return root

# ============================================================================
# Solution 5: BFS_Queue_older_version    (原文件: 0116 - C - Populating Next Right Pointers - BFS Queue (older version).py)
# ============================================================================

# # Definition for a Node_5.

class Node_5:
    def __init__(
        self,
        val: int = 0,
        left: "Node_5" = None,
        right: "Node_5" = None,
        next: "Node_5" = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class Solution_5_BFS_Queue_older_version:
    def connect(self, root: "Node_5") -> "Node_5":
        if not root:
            return root

        # Start with the root node. There are no next pointers
        # that need to be set up on the first level
        leftmost = root

        # Once we reach the final level, we are done
        while leftmost.left:
            # Iterate the "linked list" starting from the head
            # node and using the next pointers, establish the
            # corresponding links for the next level
            head = leftmost
            while head:
                # CONNECTION 1
                head.left.next = head.right

                # CONNECTION 2
                if head.next:
                    head.right.next = head.next.left

                # Progress along the list (nodes on the current level)
                head = head.next

            # Move onto the next level
            leftmost = leftmost.left

        return root
