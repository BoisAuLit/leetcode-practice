from typing import List

class Solution_BFS:
    """
    Solution: BFS
    1. First use BFS to find all cells of island A
    2. Then use BFS to stetch from island A to island B (Take note of the distance
    in along the way)

    Time complexity: O(N²)
    Space complexity: O(N²)
    """
    def shortestBridge(self, grid: List[List[int]]) -> int:
        n = len(grid)
        first_x, first_y = -1, -1
        
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    first_x, first_y = i, j
                    break
            if first_x != -1:
                break
        
        # bfsQueue for BFS on land cells of island A; secondBfsQueue for BFS on water cells.
        bfs_queue = [(first_x, first_y)]
        second_bfs_queue = [(first_x, first_y)]
        grid[first_x][first_y] = 2
        
        # BFS for all land cells of island A and add them to second_bfs_queue.
        while bfs_queue:
            new_bfs = []
            for x, y in bfs_queue:
                for cur_x, cur_y in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if 0 <= cur_x < n and 0 <= cur_y < n and grid[cur_x][cur_y] == 1:
                        new_bfs.append((cur_x, cur_y))
                        second_bfs_queue.append((cur_x, cur_y))
                        grid[cur_x][cur_y] = 2
            bfs_queue = new_bfs

        distance = 0
        while second_bfs_queue:
            new_bfs = []
            for x, y in second_bfs_queue:
                for cur_x, cur_y in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if 0 <= cur_x < n and 0 <= cur_y < n:
                        if grid[cur_x][cur_y] == 1:
                            return distance
                        elif grid[cur_x][cur_y] == 0:
                            new_bfs.append((cur_x, cur_y))
                            grid[cur_x][cur_y] = -1

            # Once we finish one round without finding land cells of island B, we will
            # start the next round on all water cells that are 1 cell further away from
            # island A and increment the distance by 1.
            second_bfs_queue = new_bfs
            distance += 1


class Solution_DFS_BFS:
    """
    Solution: Depth First Search (DFS) then Breadth First Search (BFS)
    1. First use DFS to find all cells of island A
    2. Then use BFS to stetch from island A to island B (Take note of the distance
    in along the way)

    Time complexity: O(N²)
    Space complexity: O(N²)
    """

    def shortestBridge(self, grid: List[List[int]]) -> int:
        n = len(grid)
        first_x, first_y = -1, -1
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    first_x, first_y = i, j
                    break
            if first_x != -1:
                break

        def dfs(x, y):
            grid[x][y] = 2
            bfs_queue.append((x, y))
            for cur_x, cur_y in [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]:
                if (
                    0 <= cur_x < n
                    and 0 <= cur_y < n
                    and grid[cur_x][cur_y] == 1
                ):
                    dfs(cur_x, cur_y)

        bfs_queue = []
        dfs(first_x, first_y)

        distance = 0
        while bfs_queue:
            new_bfs = []
            for x, y in bfs_queue:
                for cur_x, cur_y in [
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1),
                ]:
                    if 0 <= cur_x < n and 0 <= cur_y < n:
                        if grid[cur_x][cur_y] == 1:
                            return distance
                        elif grid[cur_x][cur_y] == 0:
                            new_bfs.append((cur_x, cur_y))
                            grid[cur_x][cur_y] = -1
            bfs_queue = new_bfs
            distance += 1


s = Solution_BFS()
input_ = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
]
result = s.shortestBridge(input_)
print(result)

"""

"""
