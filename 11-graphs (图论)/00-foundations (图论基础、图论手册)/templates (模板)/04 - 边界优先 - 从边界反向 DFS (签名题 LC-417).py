"""
边界优先: 从边界反向 DFS

画面:   水往低处流不好算, 反过来让海水从海岸往高处爬: 爬得到的格子, 它的水就流得到海。
        两片海各爬一次, 两次都爬到的格子就是答案。
动作:   ① 站海岸 (把一整条边界的格子当作起点)
        ② 往高爬 (邻居高度 >= 当前才能爬过去, 这是正向规则反过来)
        ③ 记脚印 (每片海一个 visited 集合)
        ④ 取交集 (两个集合都有的格子)
动作对代码: 见下面 # ! 注释
签名题: LC-417 Pacific Atlantic Water Flow
决策句: 题目问 "哪些格子能到边界 / 被边界包围" 时, 不要从每个格子出发, 而是从边界出发反向遍历一次。
改一行: 和 02 洪水填充比, 起点从 "扫到的第一个陆地" 换成 "整条边界", 流动条件从 "== 1" 换成 "高度 >= 当前"。
        LC-130 Surrounded Regions: 从边界 O 出发标记, 没被标记的 O 改成 X。
        LC-1254 Number of Closed Islands: 先把碰边界的岛淹掉, 再按 02 数岛。
"""
from typing import List, Set, Tuple
import sys

sys.setrecursionlimit(10 ** 6)
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:
    rows, cols = len(heights), len(heights[0])

    def climb(r: int, c: int, seen: Set[Tuple[int, int]]) -> None:
        if (r, c) in seen:
            return
        seen.add((r, c))                                # ! ③ 记脚印
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and heights[nr][nc] >= heights[r][c]:
                climb(nr, nc, seen)                     # ! ② 往高爬: 反向规则

    pac: Set[Tuple[int, int]] = set()
    atl: Set[Tuple[int, int]] = set()
    for r in range(rows):                               # ! ① 站海岸: 左边界归太平洋, 右边界归大西洋
        climb(r, 0, pac)
        climb(r, cols - 1, atl)
    for c in range(cols):                               # ! ① 上边界归太平洋, 下边界归大西洋
        climb(0, c, pac)
        climb(rows - 1, c, atl)
    return [[r, c] for r, c in sorted(pac & atl)]       # ! ④ 取交集


if __name__ == "__main__":
    h = [[1, 2, 2, 3, 5],
         [3, 2, 3, 4, 4],
         [2, 4, 5, 3, 1],
         [6, 7, 1, 4, 5],
         [5, 1, 1, 2, 4]]
    print(pacific_atlantic(h))
    # [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
