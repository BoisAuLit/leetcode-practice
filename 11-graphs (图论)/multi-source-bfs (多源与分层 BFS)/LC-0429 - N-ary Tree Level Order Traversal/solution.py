"""LC-0429 - N-ary Tree Level Order Traversal

合并自 3 个解法文件:
  1. 0429 - A - N-ary Tree Level Order Traversal - BFS Without Queue 🐢.py
  2. 0429 - B - N-ary Tree Level Order Traversal - BFS With Queue 🚀 神仙级别速度.py
  3. 0429 - C - N-ary Tree Level Order Traversal - BFS (older version).py
"""

from typing import List, Optional

from collections import deque


# ============================================================================
# Solution 1: BFS_Without_Queue    (原文件: 0429 - A - N-ary Tree Level Order Traversal - BFS Without Queue 🐢.py)
# ============================================================================

class Node_1:
    def __init__(
        self, val: Optional[int] = None, children: Optional[List["Node_1"]] = None
    ):
        self.val = val
        self.children = children

class Solution_1_BFS_Without_Queue:
    def levelOrder(self, root: "Node_1") -> List[List[int]]:
        if not root:
            return []
        result = []
        level = [root]
        while level:
            next_level = []
            values = []
            for node in level:
                values.append(node.val)
                next_level.extend(node.children)
            result.append(values)
            level = next_level
        return result

# ============================================================================
# Solution 2: BFS_With_Queue    (原文件: 0429 - B - N-ary Tree Level Order Traversal - BFS With Queue 🚀 神仙级别速度.py)
# ============================================================================

class Node_2:
    def __init__(
        self, val: Optional[int] = None, children: Optional[List["Node_2"]] = None
    ):
        self.val = val
        self.children = children

class Solution_2_BFS_With_Queue:
    def levelOrder(self, root: "Node_2") -> List[List[int]]:
        if not root:
            return []
        queue = deque([(root)])
        result = []
        while queue:
            values = []
            for _ in range(len(queue)):
                node = queue.popleft()
                values.append(node.val)
                queue.extend(node.children)
            result.append(values)

        return result

# ============================================================================
# Solution 3: BFS_older_version    (原文件: 0429 - C - N-ary Tree Level Order Traversal - BFS (older version).py)
# ============================================================================

class Node_3:
    def __init__(
        self, val: Optional[int] = None, children: Optional[List["Node_3"]] = None
    ):
        self.val = val
        self.children = children

class Solution_3_BFS_older_version:
    def levelOrder(self, root: "Node_3") -> List[List[int]]:
        if not root:
            return []
        level = [root]
        result = []
        while level:
            new_level = []
            values = []
            for node in level:
                values.append(node.val)
                if node.children:
                    new_level.extend(node.children)
            result.append(values)
            level = new_level
        return result
