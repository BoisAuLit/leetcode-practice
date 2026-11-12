"""LC-0542 - 01 Matrix

阶段 1 · DFS、BFS（静态无权的连通性与步数）· 多源 BFS（所有起点一起入队）○ 核心
题目在问：每个格子到最近的 0 的距离
点是什么：一个格子   边是什么：上下左右相邻，距离 1
和签名题比改了哪一行：和 994 比，起点从烂橘子换成所有 0，答案不是总层数而是每个格子自己的层数（dist = 父格 + 1）
"""
from typing import List
from collections import deque


##################################################################################################
##### ! Solution 1: 多源 BFS，所有 0 一起入队，按层写距离
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：每格到最近起点的距离就是它所在的层数；visited 集合保证每格只入队一次
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m = len(mat)
        n = len(mat[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        visited = {(x, y) for x in range(m) for y in range(n) if mat[x][y] == 0}
        queue = deque(visited)
        distance = 0
        while queue:
            new_queue = deque()
            while queue:
                x, y = queue.popleft()
                mat[x][y] = distance
                for dx, dy in directions:
                    x1, y1 = x + dx, y + dy
                    if 0 <= x1 < m and 0 <= y1 < n and (x1, y1) not in visited:
                        visited.add((x1, y1))
                        new_queue.append((x1, y1))
            queue = new_queue
            distance += 1

        return mat


##################################################################################################
##### ! Solution 2: 多源 BFS，原地写距离（dist = 父格 + 1）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)（队列）
##### ! 适用：最标准的多源 BFS 模板，用 -1 代替 visited 集合，不数层
##################################################################################################


class Solution_2:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        q = deque()
        for x in range(m):
            for y in range(n):
                if mat[x][y] == 0:
                    q.append((x, y))  # ! 所有 0 一起入队，它们的距离就是 0
                else:
                    mat[x][y] = -1  # ! -1 表示还没算过，省掉 visited 集合
        while q:
            x, y = q.popleft()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < m and 0 <= ny < n and mat[nx][ny] == -1:
                    mat[nx][ny] = mat[x][y] + 1  # ! 距离从父格 +1 得来，写进去的同时也完成了标记
                    q.append((nx, ny))
        return mat


##################################################################################################
##### ! Solution 3: 两遍 DP（左上到右下，再右下到左上）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)（原地改 mat 可到 O(1)）
##### ! 适用：不想用队列时；最近的 0 要么在左上方向要么在右下方向，两遍各管一半，取 min
##################################################################################################


class Solution_3:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        INF = m + n  # ! 任何格子到最近 0 的距离都不会超过 m + n（题目保证至少一个 0）
        dist = [[0 if mat[x][y] == 0 else INF for y in range(n)] for x in range(m)]
        for x in range(m):  # ! 第一遍：左上到右下，只看上、左两个来源
            for y in range(n):
                if x > 0:
                    dist[x][y] = min(dist[x][y], dist[x - 1][y] + 1)
                if y > 0:
                    dist[x][y] = min(dist[x][y], dist[x][y - 1] + 1)
        for x in range(m - 1, -1, -1):  # ! 第二遍：右下到左上，只看下、右两个来源
            for y in range(n - 1, -1, -1):
                if x < m - 1:
                    dist[x][y] = min(dist[x][y], dist[x + 1][y] + 1)
                if y < n - 1:
                    dist[x][y] = min(dist[x][y], dist[x][y + 1] + 1)
        return dist


s = Solution()


# Test case 1: Expecting [[0,0,0],[0,1,0],[1,2,1]]
input_ = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]


result = s.updateMatrix(input_)
print(result)
