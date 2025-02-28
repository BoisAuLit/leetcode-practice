from typing import List
from collections import defaultdict, deque

# ! Using DFS With Stack
# ! This is significantly faster
class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # ! The following two conditions take care of edge cases
        if n - len(edges) != 1:
            return False
        if len(edges) == 0:
            return True
        adjacency = defaultdict(set)
        for a, b in edges:
            adjacency[a].add(b)
            adjacency[b].add(a)
        stack = deque([edges[0][0]])
        visited = set([edges[0][0]])
        count = 0
        while stack:
            node = stack.pop()
            count += 1
            for neighbor in adjacency[node]:
                if neighbor in visited:
                    return False
                visited.add(neighbor)
                adjacency[neighbor].remove(node)
                stack.append(neighbor)
        return count == n


# ! Using BFS With Queue
class Solution_BFS_Using_Queue:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if n - len(edges) != 1:
            return False
        if len(edges) == 0:
            return True
        adjacency = defaultdict(set)
        for a, b in edges:
            adjacency[a].add(b)
            adjacency[b].add(a)
        queue = deque([edges[0][0]])
        visited = set([edges[0][0]])
        count = 0
        while queue:
            node = queue.popleft()
            count += 1
            for neighbor in adjacency[node]:
                if neighbor in visited:
                    return False
                visited.add(neighbor)
                adjacency[neighbor].remove(node)
                queue.append(neighbor)
        return count == n


s = Solution()

# Test case 1: Expecting True
# n = 5
# edges = [[0, 1], [0, 2], [0, 3], [1, 4]]

# Test case 2: Expecting False
# n = 5
# edges = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 4]]

# Test case 3: Expecting True
# n = 2
# edges = [[1, 0]]

# Test case 4: Expecting True
# n = 3
# edges = [[1, 0], [2, 0]]

# Test case 5: Expecting True
# n = 3
# edges = [[2, 0], [2, 1]]

# Test case 6: Expecting False
# n = 4
# edges = [[2, 3], [1, 2], [1, 3]]

# Test case 7: Expecting True (Edge case)
n = 1
edges = []

result = s.validTree(n, edges)
print(result)
