"""LC-0505 - The Maze II

阶段 4 · Dijkstra 堆版 (relax 写 d + w) △ 扩展题
题目在问：球在迷宫里一滚就滚到撞墙(或边界)才停，从 start 滚到 destination 总共最少滚过几格，到不了返回 -1
点是什么：球能停下来的格子   边是什么：朝一个方向一直滚到底，边权 = 这一滚经过的格数
和签名题比改了哪一行：743 原样；只是"邻居"不是上下左右那四格，而是朝四个方向各滚到底的落点，w 是滚过的步数
"""
from collections import deque
from heapq import heappop, heappush
from math import inf
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

##################################################################################################
##### ! Solution 1: Dijkstra，邻居 = 滚到底的落点，边权 = 滚过的格数
##### ! 时间复杂度: O(mn · (max(m, n) + log(mn)))，每个格子定案一次，4 次滚动各 O(max(m, n))   空间复杂度: O(mn)
##### ! 适用：边权不是 1 (一滚好几格) 所以普通 BFS 不行，带权最短路就上 Dijkstra
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        sr, sc = start
        tr, tc = destination
        dist = [[inf] * n for _ in range(m)]
        dist[sr][sc] = 0
        heap = [(0, sr, sc)]  # (滚过的总格数, r, c)

        while heap:
            d, r, c = heappop(heap)
            if (r, c) == (tr, tc):  # 第一次弹出终点就是最短
                return d
            if d > dist[r][c]:  # 作废票
                continue
            for dr, dc in DIRS:
                nr, nc, steps = r, c, 0
                while 0 <= nr + dr < m and 0 <= nc + dc < n and maze[nr + dr][nc + dc] == 0:  # ! 一直滚到撞墙
                    nr += dr
                    nc += dc
                    steps += 1
                nd = d + steps  # ! relax 还是 d + w，w 就是滚过的格数 (steps 为 0 说明贴着墙，等于没动)
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heappush(heap, (nd, nr, nc))

        return -1


##################################################################################################
##### ! Solution 2: SPFA (BFS 队列 + dist 松弛，变短就重新入队)
##### ! 时间复杂度: 平均接近 O(mn · max(m, n))，最坏 O(V · E) 级别   空间复杂度: O(mn)
##### ! 适用：不想写堆；注意不能像普通 BFS 那样第一次碰到终点就返回，要跑到队列空再读 dist
##################################################################################################


class Solution_2:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        sr, sc = start
        tr, tc = destination
        dist = [[inf] * n for _ in range(m)]
        dist[sr][sc] = 0
        q = deque([(sr, sc)])

        while q:
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc, steps = r, c, 0
                while 0 <= nr + dr < m and 0 <= nc + dc < n and maze[nr + dr][nc + dc] == 0:
                    nr += dr
                    nc += dc
                    steps += 1
                nd = dist[r][c] + steps
                if nd < dist[nr][nc]:  # ! 落点变短了才入队，同一个格子可能进队好几次
                    dist[nr][nc] = nd
                    q.append((nr, nc))

        return dist[tr][tc] if dist[tr][tc] != inf else -1  # ! 队列空了 dist 才是最终值


s = Solution_1()
maze = [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 0, 0]]
result = s.shortestDistance(maze, [0, 4], [4, 4])
print(result)  # 12

result = s.shortestDistance(maze, [0, 4], [3, 2])
print(result)  # -1

maze = [[0, 0, 0, 0, 0], [1, 1, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 1, 0, 0, 0]]
result = s.shortestDistance(maze, [4, 3], [0, 1])
print(result)  # -1
