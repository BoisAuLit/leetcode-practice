"""
DFS 洪水填充: 数连通块

画面:   往一块陆地上倒一桶颜料, 颜料顺着相邻陆地流满整个岛; 倒了几桶就有几个岛。
动作:   ① 扫格子 (遇到没染过的陆地)
        ② 倒颜料 (计数 +1)
        ③ 流开 (把相连的陆地都染掉, 递归或栈)
动作对代码: 见下面 # ! 注释
签名题: LC-200 Number of Islands
决策句: 静态图 + 无权 + 问 "有几块 / 能不能到" 就用它; 边一条条加进来还要中途回答, 改用 05 并查集; 问最少步数改用 03 BFS。
改一行: 和 03 Tutorial 的 DFS 模板比, 只是把 visited 集合换成直接改 grid (染成 '0'), 外面套一层扫格子的双重循环。
        LC-695 Max Area of Island: 让 flood 返回染掉的格子数, 取最大值。
        LC-547 Number of Provinces: 图从网格换成邻接矩阵, 邻居从四方向换成一整行。
"""
from typing import List
import sys

sys.setrecursionlimit(10 ** 6)                          # 网格递归可能很深, 先把栈调大


def num_islands_recursive(grid: List[List[str]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def flood(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return                                      # 越界或不是陆地, 流不过去
        grid[r][c] = "0"                                # ! ③ 染掉 = 标记 visited, 进来就先染
        flood(r + 1, c)
        flood(r - 1, c)
        flood(r, c + 1)
        flood(r, c - 1)

    count = 0
    for r in range(rows):                               # ! ① 扫格子
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1                              # ! ② 倒颜料
                flood(r, c)                             # ! ③ 流开
    return count


def num_islands_iterative(grid: List[List[str]]) -> int:
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):                               # ! ① 扫格子
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            count += 1                                  # ! ② 倒颜料
            grid[r][c] = "0"                            # ! 入栈时就染, 避免同一格重复入栈
            stack = [(r, c)]
            while stack:                                # ! ③ 流开 (用栈代替递归, 不怕深)
                cr, cc = stack.pop()
                for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                        grid[nr][nc] = "0"
                        stack.append((nr, nc))
    return count


if __name__ == "__main__":
    g = [list("11000"), list("11000"), list("00100"), list("00011")]
    print(num_islands_recursive([row[:] for row in g]))     # 3
    print(num_islands_iterative([row[:] for row in g]))     # 3
