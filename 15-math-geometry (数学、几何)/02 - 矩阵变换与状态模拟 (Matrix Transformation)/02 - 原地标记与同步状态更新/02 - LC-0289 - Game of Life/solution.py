"""LC-0289 - Game of Life

Level 1 · 02 矩阵变换与状态模拟 —— **Simultaneous Update（同步状态更新）**
题目在问：`board[i][j]` 是 1（活）或 0（死）。所有细胞**同时**按规则演化一代：
  - 活细胞：邻居（周围 8 格）活数 < 2 或 > 3 ⟹ 死；活数 2 或 3 ⟹ 继续活
  - 死细胞：邻居活数 **恰好 3** ⟹ 复活
原地修改 `board`。

### 决定性观察：这是「同时」，不是「依次」

> **每个格子的新状态只依赖所有格子的「原始状态」。**

如果边扫边把新状态写回 `board`，后面的格子算邻居时会读到**已经更新过的**值
⟹ 结果就不是同一代的演化了。

**反例**（横向 blinker，`[[1,1,1],[0,0,0],[0,0,0]]`）：

| 格子 | 正确（读原始状态） | 行优先直接覆盖 |
|---|---|---|
| `(0,0)` | 活邻居 1 ⟹ **死** | 活邻居 1 ⟹ 死，**并立刻写回 0** |
| `(0,1)` | 活邻居 `(0,0)`、`(0,2)` = 2 ⟹ **继续活** | 读到 `(0,0)` 已变成 0 ⟹ 活邻居只剩 1 ⟹ **错判为死** ❌ |

正确答案是 `[[0,1,0],[0,1,0],[0,0,0]]`（blinker 转 90°），
直接覆盖会把 `(0,1)` 也杀掉 ⟹ **整个图案错**。

**本题的通用模式**（和 [LC-0073 Set Matrix Zeroes](<../01 - LC-0073 - Set Matrix Zeroes (学习索引 · 实体在 01-arrays-hashing)>) 完全一样）：

```
Read Original State  →  Record Updates  →  Apply Updates
```
**两阶段**是本质，不是技巧。记住这个三段式，不要去背特殊的数字标记。

### 为什么可以在一个整数里暂存新旧两份信息

一个格子的状态只需要 1 bit，但 Python 的 `int` 有无限位 ⟹ **位是免费的**。
约定：

| bit | 含义 |
|---|---|
| **第 0 位**（`x & 1`） | **旧**状态 |
| **第 1 位**（`x >> 1`） | **新**状态 |

- 第一遍：算邻居时**只读第 0 位**（`board[r][c] & 1`）⟹ 读到的永远是原始状态。
  算出新状态后写进第 1 位（`board[r][c] |= 2`），**完全不碰第 0 位**。
- 第二遍：统一 `board[r][c] >>= 1`，把新状态搬到第 0 位。

**为什么邻居计数仍然用的是旧状态？** 因为第一遍只做 `|= 2`（只动高位），
第 0 位从头到尾没被改过。**写入不污染尚未读取的原始标记** —— 这是整个技巧的要点。

**为什么需要第二遍？** 第一遍结束时每个格子都带着「旧 | 新」两份信息，
`board` 还不是合法的 0/1 矩阵。必须有一遍统一的 `>>= 1` 把新状态「兑现」。

### 三种解法的取舍

| | 做法 | 额外空间 | 说明 |
|---|---|---|---|
| A | 拷一份新矩阵 | **O(m·n)** | 最直白，面试可先写它表明思路正确 |
| B | **位编码原地**（本文件首选） | **O(1)** | 题目的 Follow-up 要的就是这个 |
| C | 临时状态码（如 `-1` = 原活将死、`2` = 原死将活） | O(1) | 等价于 B，但要在计数时写 `== 1 or == -1` 这种条件，更容易写错 |

> **B 比 C 好的唯一理由**：B 的「读旧状态」永远是 `x & 1`，
> 不需要枚举「哪些临时码代表原来是活的」。**少一处能写错的地方。**

### Follow-up：无限大棋盘怎么办？

题目的第二个 Follow-up（面试常问）：棋盘无限大，内存装不下。
**答案**：只存**活细胞的坐标集合** `set[(r, c)]`，
然后统计所有活细胞的邻居出现次数（`Counter`），再按规则筛：
- 活细胞计数 2 或 3 ⟹ 存活
- 计数恰好 3 的格子（无论原来死活）⟹ 下一代活

复杂度变成 **O(k)**（`k` = 活细胞数），与棋盘大小无关。见 `Solution_4`。

复杂度：解法 A/B/C 均 **O(m·n)** 时间；空间 A 是 O(m·n)，**B/C 是 O(1)**。
       解法 D（稀疏集合）**O(k)** 时间与空间。

边界：
  - 全死 `[[0,0],[0,0]]` → 不变
  - 全活 2×2 `[[1,1],[1,1]]` → 不变（每个都有 3 个活邻居）
  - 单格 `[[1]]` → `[[0]]`（0 个邻居 ⟹ 死）
  - 单格 `[[0]]` → `[[0]]`
  - 1×n / n×1（没有上下或左右邻居）
  - 角落和边界格子（邻居不足 8 个）⟹ 必须做坐标合法性检查
"""

from collections import Counter
from typing import List


##################################################################################################
##### ! Solution 1: 位编码原地更新（第 0 位存旧状态，第 1 位存新状态，最后统一右移）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(1) 额外
##### ! 适用：题目 Follow-up 要求的 O(1) 空间解；「读旧写新」互不干扰
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def gameOfLife(self, board: List[List[int]]) -> None:
        m, n = len(board), len(board[0])
        for r in range(m):
            for c in range(n):
                # ! 只读第 0 位 ⟹ 拿到的永远是原始状态
                live = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n:     # ! 坐标合法性检查
                            live += board[nr][nc] & 1
                old = board[r][c] & 1
                # ! 规则：活且邻居 2/3 ⟹ 活；死且邻居恰好 3 ⟹ 活
                if (old == 1 and live in (2, 3)) or (old == 0 and live == 3):
                    board[r][c] |= 2                        # ! 只写第 1 位，不碰第 0 位
        # ! 第二遍：统一把新状态搬到第 0 位
        for r in range(m):
            for c in range(n):
                board[r][c] >>= 1


##################################################################################################
##### ! Solution 2: 拷贝一份原矩阵，读旧写新（最直白，面试先写它证明思路对）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：讲清「两阶段」概念；空间不受限时的默认写法
##################################################################################################


class Solution_2:
    def gameOfLife(self, board: List[List[int]]) -> None:
        m, n = len(board), len(board[0])
        old = [row[:] for row in board]                     # ! 快照：所有读取都走它
        for r in range(m):
            for c in range(n):
                live = sum(
                    old[r + dr][c + dc]
                    for dr in (-1, 0, 1)
                    for dc in (-1, 0, 1)
                    if not (dr == 0 and dc == 0)
                    and 0 <= r + dr < m
                    and 0 <= c + dc < n
                )
                if old[r][c] == 1:
                    board[r][c] = 1 if live in (2, 3) else 0
                else:
                    board[r][c] = 1 if live == 3 else 0


##################################################################################################
##### ! Solution 3: 临时状态码原地更新（-1 = 原活将死，2 = 原死将活）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(1) 额外
##### ! 适用：和解法 1 等价。保留它是为了对比 ——「原来是活的」要写成 in (1, -1)，更易错
##################################################################################################


class Solution_3:
    def gameOfLife(self, board: List[List[int]]) -> None:
        m, n = len(board), len(board[0])
        for r in range(m):
            for c in range(n):
                live = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n:
                            # ! 「原来是活的」= 1（还活着）或 -1（已标记为将死）
                            if board[nr][nc] in (1, -1):
                                live += 1
                if board[r][c] == 1 and live not in (2, 3):
                    board[r][c] = -1                        # ! 原活将死
                elif board[r][c] == 0 and live == 3:
                    board[r][c] = 2                         # ! 原死将活
        for r in range(m):
            for c in range(n):
                board[r][c] = 1 if board[r][c] in (1, 2) else 0


##################################################################################################
##### ! Solution 4: Follow-up —— 无限大棋盘，只存活细胞坐标
##### ! 时间复杂度: O(k)   空间复杂度: O(k)，k = 活细胞数
##### ! 适用：棋盘远大于活细胞数（稀疏）时；面试第二个 Follow-up 的标准答案
##################################################################################################


class Solution_4:
    def nextGenerationSparse(self, live_cells: set) -> set:
        # ! 统计每个格子被多少个活细胞「照顾」到
        neighbor_count = Counter()
        for r, c in live_cells:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr or dc:
                        neighbor_count[(r + dr, c + dc)] += 1
        return {
            cell
            for cell, cnt in neighbor_count.items()
            # ! 活的要 2 或 3；死的要恰好 3 —— 合起来就是这一行
            if cnt == 3 or (cnt == 2 and cell in live_cells)
        }

    def gameOfLife(self, board: List[List[int]]) -> None:
        m, n = len(board), len(board[0])
        live = {(r, c) for r in range(m) for c in range(n) if board[r][c] == 1}
        nxt = self.nextGenerationSparse(live)
        for r in range(m):
            for c in range(n):
                board[r][c] = 1 if (r, c) in nxt else 0


if __name__ == "__main__":
    import random

    def run(cls, b):
        g = [row[:] for row in b]
        cls().gameOfLife(g)
        return g

    for cls in (Solution_1, Solution_2, Solution_3, Solution_4):
        assert run(cls, [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]) == [
            [0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0],
        ]
        assert run(cls, [[1, 1], [1, 0]]) == [[1, 1], [1, 1]]
        assert run(cls, [[1, 1], [1, 1]]) == [[1, 1], [1, 1]]     # ! 2x2 方块是稳定的
        assert run(cls, [[0, 0], [0, 0]]) == [[0, 0], [0, 0]]
        assert run(cls, [[1]]) == [[0]]                            # ! 单格：0 个邻居 ⟹ 死
        assert run(cls, [[0]]) == [[0]]
        assert run(cls, [[1, 1, 1]]) == [[0, 1, 0]]                # ! 1xn
        assert run(cls, [[1], [1], [1]]) == [[0], [1], [0]]        # ! nx1

    print("[[0,1,0],[0,0,1],[1,1,1],[0,0,0]] ->")
    for row in run(Solution_1, [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]):
        print("   ", row)

    for _ in range(400):                          # ! 随机对拍：四种实现必须完全一致
        m, n = random.randint(1, 5), random.randint(1, 5)
        b = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
        outs = [run(cls, b) for cls in (Solution_1, Solution_2, Solution_3, Solution_4)]
        assert outs[0] == outs[1] == outs[2] == outs[3], (b, outs)
        # ! 独立基准：完全不原地，照定义重算一遍
        ref = [
            [
                1
                if (
                    sum(
                        b[r + dr][c + dc]
                        for dr in (-1, 0, 1)
                        for dc in (-1, 0, 1)
                        if (dr or dc) and 0 <= r + dr < m and 0 <= c + dc < n
                    )
                    in ((2, 3) if b[r][c] else (3,))
                )
                else 0
                for c in range(n)
            ]
            for r in range(m)
        ]
        assert ref == outs[0], (b, ref, outs[0])
    print("随机对拍 400 组通过 ✓（位编码 == 拷贝快照 == 临时状态码 == 稀疏集合 == 定义基准）")
