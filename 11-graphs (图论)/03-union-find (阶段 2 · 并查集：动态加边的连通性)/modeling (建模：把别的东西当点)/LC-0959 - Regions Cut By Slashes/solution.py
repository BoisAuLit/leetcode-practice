r"""LC-0959 - Regions Cut By Slashes

阶段 2 · 并查集建模 —— **把每个格子切成 4 个三角形当点**
题目在问：n×n 网格，每格是 `/`、`\` 或空格。这些斜线把方格切成若干**区域**，问有几个。

点是什么：**每个格子的 4 个三角形**（上=0、右=1、下=2、左=3），共 `4·n·n` 个点。
边是什么：同一格内被斜线**不隔开**的三角形之间 union；相邻格子**贴着的**三角形之间 union。
答案：union-find 的**连通块数**。

决定性观察（这题的全部价值在建模）：
  1. 直接把「格子」当点做不出来 —— **一个格子可能属于两个不同区域**（被斜线切开了）。
     所以必须把格子**再细分**。
  2. **切成 4 个三角形**是最小的可行细分（也可以放大 3 倍变成 3×3 的 01 网格再做 flood fill，
     见 Solution_2，但三角形法更直接）。
  3. 同一格内的连接规则：
     ```
     '/'  : 上与左 相连（0-3）、右与下 相连（1-2）
     '\\' : 上与右 相连（0-1）、左与下 相连（2-3）
     ' '  : 四个全连通（0-1-2-3）
     ```
     画一下就记住了：`/` 把格子切成「左上」和「右下」两块。
  4. 跨格子的连接（**只需要连右和下两个方向**，避免重复）：
     - 和**右边**格子：我的 `右(1)` ↔ 它的 `左(3)`
     - 和**下面**格子：我的 `下(2)` ↔ 它的 `上(0)`
     只连两个方向就够了 —— 左和上的连接会由对方负责。

编号公式：`idx(r, c, k) = (r * n + c) * 4 + k`。

复杂度：**O(n² · α(n²))** ≈ O(n²)，α 是反阿克曼函数（并查集近似常数）。
      空间 O(n²)。

和本模板其他题的关系：
      `modeling (建模：把别的东西当点)` 这个模板的核心就是
      **「点不一定是题目字面上给的那个东西」**。
      本题把「格子的四分之一」当点，是这个思想最极端也最漂亮的例子。

边界：
  - 全是空格 → 1 个区域
  - 全是 `/` → n+1 个区域
  - 1×1 网格：`[" "]` → 1；`["/"]` → 2
  - 注意 Python 字符串里的 `\` 要写成 `\\`
"""

from typing import List


class DSU:
    def __init__(self, n: int):
        self.p = list(range(n))
        self.count = n            # ! 连通块数，每次成功合并就减一

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]      # ! 路径压缩
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.p[ra] = rb
        self.count -= 1
        return True


##################################################################################################
##### ! Solution 1: 每格切 4 个三角形 + 并查集，答案 = 连通块数
##### ! 时间复杂度: O(n^2 · α(n^2)) ≈ O(n^2)   空间复杂度: O(n^2)
##### ! 适用：「斜线 / 对角线把区域切开」类题；核心是把格子再细分成可以独立连通的小块
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def regionsBySlashes(self, grid: List[str]) -> int:
        n = len(grid)
        dsu = DSU(4 * n * n)

        def idx(r: int, c: int, k: int) -> int:
            return (r * n + c) * 4 + k            # ! k: 0=上 1=右 2=下 3=左

        for r in range(n):
            for c in range(n):
                ch = grid[r][c]
                if ch == "/":
                    dsu.union(idx(r, c, 0), idx(r, c, 3))   # ! 上-左
                    dsu.union(idx(r, c, 1), idx(r, c, 2))   # ! 右-下
                elif ch == "\\":
                    dsu.union(idx(r, c, 0), idx(r, c, 1))   # ! 上-右
                    dsu.union(idx(r, c, 2), idx(r, c, 3))   # ! 下-左
                else:                                        # ! 空格：四块全连通
                    dsu.union(idx(r, c, 0), idx(r, c, 1))
                    dsu.union(idx(r, c, 1), idx(r, c, 2))
                    dsu.union(idx(r, c, 2), idx(r, c, 3))
                # ! 跨格子只连「右」和「下」两个方向，避免重复
                if c + 1 < n:
                    dsu.union(idx(r, c, 1), idx(r, c + 1, 3))
                if r + 1 < n:
                    dsu.union(idx(r, c, 2), idx(r + 1, c, 0))
        return dsu.count


##################################################################################################
##### ! Solution 2: 把每格放大成 3×3 的 01 网格，再做普通 flood fill 数连通块
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)
##### ! 适用：另一种建模思路，验证三角形法；放大 3 倍是因为斜线要画成对角的 1
##################################################################################################


class Solution_2:
    def regionsBySlashes(self, grid: List[str]) -> int:
        n = len(grid)
        m = 3 * n
        g = [[0] * m for _ in range(m)]
        for r in range(n):
            for c in range(n):
                ch = grid[r][c]
                br, bc = r * 3, c * 3
                if ch == "/":
                    g[br][bc + 2] = g[br + 1][bc + 1] = g[br + 2][bc] = 1
                elif ch == "\\":
                    g[br][bc] = g[br + 1][bc + 1] = g[br + 2][bc + 2] = 1
        seen = [[False] * m for _ in range(m)]
        regions = 0
        for i in range(m):
            for j in range(m):
                if g[i][j] == 0 and not seen[i][j]:
                    regions += 1
                    stack = [(i, j)]
                    seen[i][j] = True
                    while stack:
                        x, y = stack.pop()
                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < m and 0 <= ny < m and g[nx][ny] == 0 and not seen[nx][ny]:
                                seen[nx][ny] = True
                                stack.append((nx, ny))
        return regions


if __name__ == "__main__":
    import random

    cases = [([" /", "/ "], 2), ([" /", "  "], 1), (["/\\", "\\/"], 5),
             ([" "], 1), (["/"], 2), (["\\"], 2),
             (["//", "/ "], 3)]
    for grid, want in cases:
        a = Solution_1().regionsBySlashes(list(grid))
        b = Solution_2().regionsBySlashes(list(grid))
        assert a == want, (grid, a, want)
        assert b == want, (grid, b, want)
        print(f"{grid} -> {a}")

    for _ in range(500):                 # ! 随机网格对拍：三角形并查集 == 放大 3 倍 flood fill
        n = random.randint(1, 4)
        grid = ["".join(random.choice(" /\\") for _ in range(n)) for _ in range(n)]
        a = Solution_1().regionsBySlashes(list(grid))
        b = Solution_2().regionsBySlashes(list(grid))
        assert a == b, (grid, a, b)
    print("随机对拍 500 组通过 ✓（4 三角形并查集 == 3× 放大 flood fill）")
