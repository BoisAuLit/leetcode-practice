"""LC-0980 - Unique Paths III（第二轮自主新增）

Level 1 · 04 网格搜索与约束满足 —— 网格回溯 + **「必须走遍所有空格」的全覆盖约束**
题目在问：从 1 走到 2，**每个 0 都必须恰好经过一次**，-1 是障碍。求不同路径数。

为什么新增它（和 LC-0079 Word Search 的对照）：

| | LC-0079 Word Search | LC-0980 本题 |
|---|---|---|
| 目标 | **存在**一条匹配路径 ⟹ 找到就 return True | **数**所有合法路径 ⟹ 必须走完整棵搜索树 |
| 约束 | 路径上的字符要匹配单词 | **必须覆盖所有空格**（全覆盖） |
| 终止 | 匹配完整个单词 | 到达终点**且** `remaining == 0` |
| 剪枝 | 字符不匹配就退 | 障碍 / 越界 / 已访问 |

「**计数**而不是「存在性」」+「**全覆盖**约束」是本题独有的，
LC-0079 完全覆盖不到。而网格回溯 + visited 标记 + 回溯恢复这套骨架是共用的。

决定性观察：
  1. **先数一遍**有多少个需要走的格子：`need = 空格数 + 1`（含起点）。
     沿路递减，到终点时 `need == 0` 才算一条合法路径。
  2. 标记已访问：直接把格子改成 `-1`（障碍），**递归返回后改回 0** —— 这就是回溯。
     用 `visited` 集合也行，改格子更省内存。
  3. **到达终点时必须立刻 return**，不能继续走 —— 终点只能是路径的最后一格。
  4. 计数题**不能提前 return**（找到一条还要继续找），这是和 LC-0079 最大的代码差异。

```python
def dfs(r, c, remaining):
    if 越界 or grid[r][c] == -1: return 0
    if grid[r][c] == 2:
        return 1 if remaining == 0 else 0      # 必须刚好走完所有空格
    grid[r][c] = -1                            # 标记
    total = sum(dfs(nr, nc, remaining - 1) for 四个方向)
    grid[r][c] = 0                             # 回溯恢复
    return total
```

**`remaining` 的计数要对齐**：进入一个格子就消耗一个名额。
      起点也算一个，所以初始 `remaining = 空格数 + 1`，
      在终点判断时 `remaining` 应该已经减到 0。
      （实现里对「进入终点」那一步不再减，所以判 `remaining == 0`。
       不同写法的偏移量不同，**务必用样例校准**，这是本题最容易差一的地方。）

复杂度：最坏 **O(4^(m·n))**（实际远小于此，因为障碍和已访问会大量剪枝）。
      空间 O(m·n) 递归栈。
      题目限制 `1 <= m*n <= 20`，就是为了让指数级可以接受。

边界：
  - 没有空格（起点和终点相邻）
  - 终点被障碍围死 → 0
  - 整个网格只有起点和终点
  - 存在多条等价路径
"""

from typing import List


##################################################################################################
##### ! Solution 1: 网格回溯 + 剩余格子计数（原地改格子当 visited）
##### ! 时间复杂度: 最坏 O(4^(m·n))   空间复杂度: O(m·n) 递归栈
##### ! 适用：「必须走遍所有可走格子」的路径计数；和 LC-0079 共用网格回溯骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        start = (0, 0)
        empty = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 0:
                    empty += 1
                elif grid[r][c] == 1:
                    start = (r, c)

        def dfs(r: int, c: int, remaining: int) -> int:
            if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] == -1:
                return 0
            if grid[r][c] == 2:
                return 1 if remaining == 0 else 0   # ! 必须刚好把所有空格走完
            saved = grid[r][c]
            grid[r][c] = -1                          # ! 标记已访问（当成障碍）
            total = (dfs(r + 1, c, remaining - 1) + dfs(r - 1, c, remaining - 1)
                     + dfs(r, c + 1, remaining - 1) + dfs(r, c - 1, remaining - 1))
            grid[r][c] = saved                       # ! 回溯恢复
            return total

        # ! 起点自己占一个名额：进入起点时 remaining = empty + 1，走完所有空格后恰好为 0
        return dfs(start[0], start[1], empty + 1)


##################################################################################################
##### ! Solution 2: 用 visited 集合而不是改原网格（不破坏入参）
##### ! 时间复杂度: 同上   空间复杂度: O(m·n)
##### ! 适用：不允许修改输入时；逻辑完全一致，只是标记方式不同
##################################################################################################


class Solution_2:
    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        start = None
        empty = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 0:
                    empty += 1
                elif grid[r][c] == 1:
                    start = (r, c)
        visited = set()

        def dfs(r, c, remaining):
            if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] == -1 or (r, c) in visited:
                return 0
            if grid[r][c] == 2:
                return 1 if remaining == 0 else 0
            visited.add((r, c))
            total = sum(dfs(r + dr, c + dc, remaining - 1)
                        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            visited.remove((r, c))
            return total

        return dfs(start[0], start[1], empty + 1)


if __name__ == "__main__":
    import random

    cases = [([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]], 2),
             ([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]], 4),
             ([[0, 1], [2, 0]], 0),
             ([[1, 2]], 1),
             ([[1, -1, 2]], 0)]
    for grid, want in cases:
        a = Solution_1().uniquePathsIII([row[:] for row in grid])
        b = Solution_2().uniquePathsIII([row[:] for row in grid])
        assert a == b == want, (grid, a, b, want)
        print(f"{grid} -> {a}")

    # ! 验证 Solution_1 用完之后把网格恢复原样了（原地标记必须正确回溯）
    g = [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]]
    snapshot = [row[:] for row in g]
    Solution_1().uniquePathsIII(g)
    assert g == snapshot, "原地标记没有完全回溯！"
    print("原地标记回溯检查通过 ✓ 网格已恢复原样")

    for _ in range(300):                 # ! 随机小网格对拍
        rows, cols = random.randint(1, 3), random.randint(2, 4)   # ! 至少 2 格，才放得下起点和终点
        cells = [0] * (rows * cols)
        idx = random.sample(range(rows * cols), 2)
        cells[idx[0]], cells[idx[1]] = 1, 2
        for i in range(rows * cols):
            if i not in idx and random.random() < 0.3:
                cells[i] = -1
        grid = [cells[r * cols:(r + 1) * cols] for r in range(rows)]
        a = Solution_1().uniquePathsIII([row[:] for row in grid])
        b = Solution_2().uniquePathsIII([row[:] for row in grid])
        assert a == b, (grid, a, b)
    print("随机对拍 300 组通过 ✓")
