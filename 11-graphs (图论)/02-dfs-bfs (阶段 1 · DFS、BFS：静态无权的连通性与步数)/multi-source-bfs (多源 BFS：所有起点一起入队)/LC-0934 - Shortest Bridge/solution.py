"""LC-0934 - Shortest Bridge

阶段 1 · 多源 BFS（所有起点一起入队） · 手册未单列（994 的直接变体）
题目在问：n x n 网格里恰好两座岛（四连通的 1），最少把几个 0 翻成 1 能把两座岛接起来
点是什么：一个格子   边是什么：四方向相邻
和签名题比改了哪一行：994 的"所有烂橘子一起入队"换成"第一座岛的所有格子一起入队"；
    多了前置一步：先用 DFS / BFS 把第一座岛找全、标成 2 并全部进队；然后多源 BFS 一层层往外淹水面（0 标成 -1），
    第一次碰到还是 1 的格子就是第二座岛，此时的层数就是答案
"""
from collections import deque  # Solution_3 用
from typing import List

##################################################################################################
##### ! Solution 1: 两段 BFS：先 BFS 把第一座岛找全并全部进队，再多源 BFS 往外扩
##### ! 时间复杂度: O(n²)  每格最多进队一次   空间复杂度: O(n²)  队列
##### ! 适用：默认写法，两段都是同一套"按层扩"的代码，没有递归深度问题；用户的测试代码用的就是它
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


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


##################################################################################################
##### ! Solution 2: 递归 DFS 找第一座岛（顺手全部进队），再多源 BFS 往外扩
##### ! 时间复杂度: O(n²)   空间复杂度: O(n²)  递归栈最坏 = 岛的格子数（蛇形岛可到 10^4，本地默认上限 1000 会炸）
##### ! 适用：最常见的面试写法（DFS 洪水填充 + BFS），n ≤ 100 在 LeetCode 上能过；本地跑大岛要抬递归上限或用 Solution 3
##################################################################################################


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

##################################################################################################
##### ! Solution 3: 显式栈 DFS 找第一座岛 + deque 多源 BFS
##### ! 时间复杂度: O(n²)   空间复杂度: O(n²)  栈 + 队列，没有递归
##### ! 适用：想要 DFS 的写法又不想碰递归上限；入栈时就标 2，一格只进栈一次
##################################################################################################


class Solution_3:
    def shortestBridge(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # 1. 随便找第一座岛的一格
        sr, sc = next((r, c) for r in range(n) for c in range(n) if grid[r][c] == 1)

        # 2. 显式栈 DFS：整座岛标成 2，同时每一格都进 BFS 队列（多源）
        stack = [(sr, sc)]
        grid[sr][sc] = 2
        q = deque()
        while stack:
            x, y = stack.pop()
            q.append((x, y))
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 1:
                    grid[nx][ny] = 2  # ! 入栈时就标，避免同一格重复进栈
                    stack.append((nx, ny))

        # 3. 多源 BFS，层数 = 要填的水格数
        steps = 0
        while q:
            for _ in range(len(q)):
                x, y = q.popleft()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < n and 0 <= ny < n:
                        if grid[nx][ny] == 1:  # ! 碰到还是 1 的格子 = 第二座岛
                            return steps
                        if grid[nx][ny] == 0:
                            grid[nx][ny] = -1  # ! 淹过的水面标 -1 当 visited
                            q.append((nx, ny))
            steps += 1
        return -1  # 题目保证恰好两座岛，走不到这里


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
