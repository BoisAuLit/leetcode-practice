"""LC-1926 - Nearest Exit from Entrance in Maze

阶段 1 · BFS 层数 = 步数 ○ 核心变体
题目在问：从入口出发，走到最近的"出口"（边界上的空格）要几步；走不到返回 -1
点是什么：一个空格 (r, c)   边是什么：上下左右走一格，落点也得是空格
和签名题比改了哪一行：994 是多源 BFS 数层数，这里是单源，同样按层数步；
    多一条"出口判定"：新发现的格子在边界上就返回当前层数。
    入口本身不算出口：一开始就把它放进 visited，它永远不会作为"新发现的格子"被判定
"""
from collections import deque
from typing import List

##################################################################################################
##### ! Solution 1: BFS 按层数步 (visited 集合)
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：单源、无权、最短步数；不想改输入就用 visited
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        sr, sc = entrance
        queue = deque([(sr, sc)])
        visited = {(sr, sc)}  # ! 入口先标掉：它不算出口，也不许回头
        steps = 0
        while queue:
            steps += 1  # ! 这一轮扩出来的格子离入口都是 steps 步
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if not (0 <= nr < m and 0 <= nc < n) or maze[nr][nc] != ".":
                        continue
                    if (nr, nc) in visited:
                        continue
                    if nr == 0 or nr == m - 1 or nc == 0 or nc == n - 1:
                        return steps  # ! 第一次碰到边界空格就是最近出口(BFS 按距离递增发现)
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return -1  # ! 队列空了还没碰到边界：没有出口


##################################################################################################
##### ! Solution 2: BFS 把走过的格子直接改成墙 (原地标记)
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)   只剩队列
##### ! 适用：允许改输入时省掉 visited；队列里带距离，弹出时判出口
##################################################################################################


class Solution_2:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        sr, sc = entrance
        maze[sr][sc] = "+"  # ! 走过的格子直接封墙，这就是 visited
        queue = deque([(sr, sc, 0)])  # ! (r, c, 走到这里的步数)
        while queue:
            r, c, d = queue.popleft()
            if d > 0 and (r == 0 or r == m - 1 or c == 0 or c == n - 1):
                return d  # ! d > 0 排除入口本身
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < m and 0 <= nc < n and maze[nr][nc] == ".":
                    maze[nr][nc] = "+"
                    queue.append((nr, nc, d + 1))
        return -1


s = Solution_1()
maze = [["+", "+", ".", "+"], [".", ".", ".", "+"], ["+", "+", "+", "."]]
entrance = [1, 2]
result = s.nearestExit(maze, entrance)
print(result)  # 1

maze = [["+", "+", "+"], [".", ".", "."], ["+", "+", "+"]]
entrance = [1, 0]
result = s.nearestExit(maze, entrance)
print(result)  # 2

maze = [[".", "+"]]
entrance = [0, 0]
result = s.nearestExit(maze, entrance)
print(result)  # -1
