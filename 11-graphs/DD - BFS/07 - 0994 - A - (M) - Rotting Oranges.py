from typing import List
from collections import deque


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        oranges_count = 0
        m = len(grid)
        n = len(grid[0])
        rottons = deque()
        seen = set() # * Just for consistency, we only use the word "seen", never use "visited"
        for x in range(m):
            for y in range(n):
                if grid[x][y] != 0:
                    oranges_count += 1
                if grid[x][y] == 2:
                    rottons.append((x, y))
                    seen.add((x, y))  # ! All rotton oranges are already seen
        # ! If there are no fresh oranges in the beginning, then 0 minutes is needed.
        if len(rottons) == oranges_count:
            return 0
        minutes = 0
        while rottons:
            # ! Traverse level by level, each level takes 1 minute.
            # ! The next level to be traverse will become rotton in 1 minute.
            for _ in range(len(rottons)):
                x, y = rottons.popleft()
                for dx, dy in directions:
                    nx = x + dx
                    ny = y + dy
                    if (
                        0 <= nx < m
                        and 0 <= ny < n
                        and grid[nx][ny] == 1
                        and (nx, ny) not in seen
                    ):
                        seen.add((nx, ny))
                        rottons.append((nx, ny))
            minutes += 1
            # ! Just compare all the "seen" oranges to the total oranges count.
            # ! If they are equal, then just stop.
            if len(seen) == oranges_count:
                return minutes
        return -1

# Test case 1: Expecting 4
# s = Solution()
# grid = [[2,1,1],[1,1,0],[0,1,1]]
# result = s.orangesRotting(grid)
# print(result)

# Test case 2: Expecting -1
# The fresh orange on grid[2][0] will never become rotten
# s = Solution()
# grid = [[2,1,1],[0,1,1],[1,0,1]]
# result = s.orangesRotting(grid)
# print(result)

# Test case 3: Expecting 0
# There are no fresh oranges at all
s = Solution()
grid = [[0,2]]
result = s.orangesRotting(grid)
print(result)
