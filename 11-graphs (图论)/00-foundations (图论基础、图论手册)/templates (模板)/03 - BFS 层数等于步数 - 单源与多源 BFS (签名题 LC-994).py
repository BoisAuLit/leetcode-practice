"""
BFS 层数等于步数: 单源与多源 BFS

画面:   往水里扔石子, 波纹一圈一圈往外扩; 第几圈到达就是几步。
        多源就是同时扔好几颗石子, 波纹各自扩散, 先到的算数。
动作:   ① 进队 (起点入队并标记; 多源: 所有起点一开始全进队)
        ② 剥一层 (记下当前队列长度, 只处理这么多个)
        ③ 扩散 (邻居没访问过就标记 + 入队)
        ④ 数层 (一层剥完, 步数 +1)
动作对代码: 见下面 # ! 注释
签名题: LC-994 Rotting Oranges (多源); LC-1091 Shortest Path in Binary Matrix (单源)
决策句: 无权图问 "最少几步" 就用 BFS; 边有权就换 08 Dijkstra; 只问 "有几块" 用 02 DFS 更省事。
改一行: 和单源比, 多源 BFS 只改 ①: 把所有起点一起放进初始队列, 其余一行不动。
        标记 visited 要在入队时做, 不是出队时做, 否则同一个点会被重复入队。
        LC-542 01 Matrix: 所有 0 一起进队, 每格的层数就是答案。
"""
from collections import deque
from typing import List, Tuple

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def bfs_steps(grid: List[List[int]], start: Tuple[int, int], target: Tuple[int, int]) -> int:
    """单源: 从 start 走到 target 最少几步, 0 是路 1 是墙, 到不了返回 -1"""
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    seen = {start}                                      # ! ① 进队 + 标记
    steps = 0
    while queue:
        for _ in range(len(queue)):                     # ! ② 剥一层
            r, c = queue.popleft()
            if (r, c) == target:
                return steps
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in seen:
                    seen.add((nr, nc))                  # ! ③ 扩散: 入队时标记
                    queue.append((nr, nc))
        steps += 1                                      # ! ④ 数层
    return -1


def oranges_rotting(grid: List[List[int]]) -> int:
    """多源: 2 是烂橘子, 1 是好橘子, 0 是空; 全烂要几分钟, 烂不完返回 -1"""
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))                    # ! ① 多源: 所有起点一开始全进队
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):                     # ! ② 剥一层
            r, c = queue.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2                    # ! ③ 扩散: 直接改 grid 当 visited
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1                                    # ! ④ 数层
    return minutes if fresh == 0 else -1


if __name__ == "__main__":
    maze = [[0, 0, 1], [1, 0, 1], [1, 0, 0]]
    print(bfs_steps(maze, (0, 0), (2, 2)))                      # 4
    print(oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))   # 4
    print(oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))   # -1
