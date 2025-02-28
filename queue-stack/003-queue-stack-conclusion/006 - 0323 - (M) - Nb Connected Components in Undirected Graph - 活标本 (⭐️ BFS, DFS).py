from typing import List
from collections import defaultdict, deque


class Solution_BFS_Using_Queue:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        adjacency = defaultdict(set)
        for a, b in edges:
            adjacency[a].add(b)
            adjacency[b].add(a)

        unvisited = set(range(n))

        def bfs(root: int, unvisited):
            visited = set([root])
            queue = deque([root])
            while queue:
                node = queue.popleft()
                for neighbor in adjacency[node]:
                    adjacency[neighbor].remove(node)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            unvisited -= visited

        count = 0
        while unvisited:
            root = next(iter(unvisited))
            bfs(root, unvisited)
            count += 1
        return count


class Solution_DFS_Using_Stack:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        adjacency = defaultdict(set)
        for a, b in edges:
            adjacency[a].add(b)
            adjacency[b].add(a)

        unvisited = set(range(n))

        def dfs(root: int, unvisited):
            print(root, unvisited)
            stack = deque([root])
            visited = set([root])
            while stack:
                node = stack.pop()
                for neighbor in adjacency[node]:
                    adjacency[neighbor].remove(node)
                    # We do this to avoid circle
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            unvisited -= visited

        count = 0
        while unvisited:
            root = next(iter(unvisited))
            dfs(root, unvisited)
            count += 1
        return count


s = Solution_BFS_Using_Queue()

# Test case 1: Expecting 2
n = 5
edges = [[0, 1], [1, 2], [3, 4]]

# Test case 2: Expecting 1
# n = 5
# edges = [[0, 1], [1, 2], [2, 3], [3, 4]]

result = s.countComponents(n, edges)
print(result)
