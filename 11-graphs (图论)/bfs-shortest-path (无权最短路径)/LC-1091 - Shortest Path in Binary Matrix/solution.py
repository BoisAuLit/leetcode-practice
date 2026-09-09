"""LC-1091 - Shortest Path in Binary Matrix

合并自 4 个解法文件:
  1. 1091 - A - Shortest Path in Binary - BFS 最好用 ✅ - 别用 DFS, 无解 ❌.py
  2. 1091 - B - Shortest Path in Binary - BFS 最好用 ✅ - Level by Level.py
  3. 1091 - C - Shortest Path in Binary - DFS Recursive (TODO, empty).py
  4. 1091 - D - Shortest Path in Binary - BFS Queue - 更快 🚀 (TODO, empty).py
"""

from typing import List

from collections import deque


# ============================================================================
# Solution 1: DFS    (原文件: 1091 - A - Shortest Path in Binary - BFS 最好用 ✅ - 别用 DFS, 无解 ❌.py)
# ============================================================================

grid_1 = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]

class Solution_1_DFS:
    def shortestPathBinaryMatrix(self, grid_1: List[List[int]]) -> int:
        if grid_1[0][0] + grid_1[-1][-1] != 0:
            return -1
        n = len(grid_1)
        directions = [
            (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy
        ]
        queue = deque([(0, 0, 1)])
        seen = {(0, 0)}
        while queue:
            x, y, d = queue.popleft()
            if (x, y) == (n - 1, n - 1):
                return d
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < n
                    and 0 <= ny < n
                    and grid_1[nx][ny] == 0
                    and (nx, ny) not in seen
                ):
                    seen.add((nx, ny))
                    queue.append((nx, ny, d + 1))
        return -1

# ============================================================================
# Solution 2: Level_by_Level    (原文件: 1091 - B - Shortest Path in Binary - BFS 最好用 ✅ - Level by Level.py)
# ============================================================================

grid_2 = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]

class Solution_2_Level_by_Level:
    def shortestPathBinaryMatrix(self, grid_2: List[List[int]]) -> int:
        if grid_2[0][0] + grid_2[-1][-1] != 0:
            return -1
        n = len(grid_2)
        directions = [
            (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy
        ]
        queue = deque([(0, 0, 1)])
        seen = {(0, 0)}
        while queue:
            for _ in range(len(queue)):
                x, y, d = queue.popleft()
                if x == y == n-1:
                    return d
                for dx, dy in directions:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < n and 0 <= ny < n and grid_2[nx][ny] == 0 and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        queue.append((nx, ny, d+1))
        return -1

# ============================================================================
# Solution 3: DFS_Recursive_TODO_empty    (原文件: 1091 - C - Shortest Path in Binary - DFS Recursive (TODO, empty).py)
# ============================================================================

# ============================================================================
# Solution 4: TODO_empty    (原文件: 1091 - D - Shortest Path in Binary - BFS Queue - 更快 🚀 (TODO, empty).py)
# ============================================================================


if __name__ == "__main__":

    # --- Solution 1: DFS ---
    s = Solution_1_DFS()
    result = s.shortestPathBinaryMatrix(grid_1)
    print(result)

    # --- Solution 2: Level_by_Level ---
    s = Solution_2_Level_by_Level()
    result = s.shortestPathBinaryMatrix(grid_2)
    print(result)
