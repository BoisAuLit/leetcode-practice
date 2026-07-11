from typing import List
from collections import defaultdict, deque


class Solution:
    def minMoves(self, matrix: List[str]) -> int:
        # Updates the node to next level
        def updateQueue(r: int, c: int) -> None:
            if mat[r][c] == ".":  # Regular node
                queue.append((r, c))
                mat[r][c] = "#"  # Mark node as visited

            elif mat[r][c] in teleport:  # Teleportable nodes
                queue.extend(teleport[mat[r][c]])
                teleport.pop(mat[r][c])

        m = len(matrix)
        n = len(matrix[0])
        steps = 0

        mat = list(map(list, matrix))
        queue = deque()

        teleport = defaultdict(list)
        dir = ((0, 1), (0, -1), (1, 0), (-1, 0))

        for r in range(m):
            for c in range(n):
                if mat[r][c].isalpha():
                    teleport[mat[r][c]].append((r, c))

        updateQueue(0, 0)  # Initiate the queue with starting position

        while queue:
            for _ in range(len(queue)):
                r, c = queue.popleft()
                if (r, c) == (m - 1, n - 1):
                    return steps

                for dr, dc in dir:
                    row, col = r + dr, c + dc
                    if 0 <= row < m and 0 <= col < n:
                        updateQueue(row, col)
            steps += 1

        return -1


# Test case 1: Expecting 2
s = Solution()
matrix = ["A..", ".A.", "..."]
result = s.minMoves(matrix)
print(result)

# Test case 2: Expecting 0 (Special case)
s = Solution()
matrix = ["."]
result = s.minMoves(matrix)
print(result)

# Test case 3: Expecting 1 (Special case)
s = Solution()
matrix = [".A", "CA"]
result = s.minMoves(matrix)
print(result)

# Test case 4: Expecting 3 (Special case)
s = Solution()
matrix = ["..G", "C.D", ".EE"]
result = s.minMoves(matrix)
print(result)
