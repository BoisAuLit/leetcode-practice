"""LC-0317 - Shortest Distance from All Buildings

阶段 1 · 多源 BFS（所有起点一起入队） · 会员题，手册未单列（放在 286 / 542 旁边）
题目在问：网格里 0 空地、1 楼、2 障碍；选一块空地盖房，到所有楼的步数之和最小是多少；没有一块空地能到所有楼就 -1
点是什么：一个格子   边是什么：四方向相邻、只能踩空地
和签名题比改了哪一行：994 是"所有起点一起入队、只扩一次"；本题每栋楼的距离要分别算，所以每栋楼单独 BFS 一次，
    把层数累加进 total[x][y]，最后在"每栋楼都走到过"的空地里取 total 最小。
    标记技巧：第 k 栋楼只走 grid 值 == -(k - 1) 的格子，走到就再 -1；没被前面所有楼走到的格子自动被剪掉，不用另开 reach 计数
"""
from collections import deque
from typing import List


##################################################################################################
##### ! Solution 1: 逐楼 BFS，grid 值递减当"已被前 k 栋楼走到"的标记（LeetCode 官方最优写法）
##### ! 时间复杂度: O(B · m · n)  B = 楼的数量，每栋楼一次 BFS   空间复杂度: O(m · n)  total 数组 + 队列
##### ! 适用：多个起点但每个起点的距离都要分别累加，不能合并成一次多源 BFS；越往后的楼能走的格子越少，越走越快
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        # 四个方向
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        rows, cols = len(grid), len(grid[0])
        # 记录每个空地到所有房子的总距离
        total = [[0] * cols for _ in range(rows)]

        empty_land_value = 0
        min_dist = float("inf")

        for row in range(rows):
            for col in range(cols):
                # 从每一栋房子做一次 BFS
                if grid[row][col] == 1:
                    min_dist = float("inf")
                    q = deque([(row, col)])
                    steps = 0

                    while q:
                        steps += 1
                        for _ in range(len(q)):
                            cr, cc = q.popleft()

                            for dr, dc in dirs:
                                nr, nc = cr + dr, cc + dc

                                # 只访问当前“轮次”还没访问过的空地
                                if (
                                    0 <= nr < rows
                                    and 0 <= nc < cols
                                    and grid[nr][nc] == empty_land_value
                                ):
                                    grid[nr][nc] -= 1
                                    total[nr][nc] += steps
                                    q.append((nr, nc))
                                    min_dist = min(min_dist, total[nr][nc])

                    # 下一栋房子只会走到 grid 值为 empty_land_value 的格子
                    empty_land_value -= 1

        return -1 if min_dist == float("inf") else min_dist


##################################################################################################
##### ! Solution 2: 逐楼 BFS 的朴素版，每栋楼各开一份 visited，另开 reach 数一块空地被几栋楼走到过
##### ! 时间复杂度: O(B · m · n)   空间复杂度: O(m · n)  total + reach + 每轮一份 visited
##### ! 适用：不改 grid 的对照写法；看懂它再看 Solution 1 的"值递减"是怎么把 visited 和 reach 合二为一的
##################################################################################################


class Solution_2:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        total = [[0] * cols for _ in range(rows)]  # 到所有楼的距离和
        reach = [[0] * cols for _ in range(rows)]  # 被几栋楼走到过
        buildings = sum(v == 1 for row in grid for v in row)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 1:
                    continue
                visited = [[False] * cols for _ in range(rows)]  # ! 每栋楼一份，不改 grid
                visited[r][c] = True
                q = deque([(r, c)])
                steps = 0
                while q:
                    steps += 1  # ! 层数 = 到这栋楼的步数
                    for _ in range(len(q)):
                        x, y = q.popleft()
                        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                            if (
                                0 <= nx < rows
                                and 0 <= ny < cols
                                and grid[nx][ny] == 0
                                and not visited[nx][ny]
                            ):
                                visited[nx][ny] = True
                                total[nx][ny] += steps
                                reach[nx][ny] += 1
                                q.append((nx, ny))

        # ! 只有被所有楼都走到过的空地才有资格
        candidates = [
            total[r][c]
            for r in range(rows)
            for c in range(cols)
            if grid[r][c] == 0 and reach[r][c] == buildings
        ]
        return min(candidates) if candidates else -1


s = Solution()
grid = [[1, 0, 2, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]]
result = s.shortestDistance(grid)
print(result)  # 7，选 (1, 2) 这块空地：3 + 3 + 1
