# Spiral Matrix 笔记（2026-09-09）

- 恰好走 m*n 步，走满即止；
- 撞墙：右转一次（一次必然够）；
- 不追求空间优化，因为这个方法我这辈子都记不住，所以索性不去记，现有的版本已经足够优秀了。面试中被问到如何优化空间，就说可以维护四个 pointer 边界（即 四边界收缩 解法）。

## 走法

- 起点放在第一格的门口 `(0, -1)`，方向向右，这样第一步自然走进 `(0, 0)`。
- 每步先试当前方向；越界或已访问就 `d = (d + 1) % 4` 右转，再走一步。
- `visited` 记已走过的格子，O(m*n) 额外空间。

### 📝 2026-09-27 - retry 1

```python
class Solution_1:
    """
    Preferred solution
    """

    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        top, right, bottom, left = 0, n - 1, m - 1, 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        # ! 这里不要用 dir 作为变量名, 因为 dir 是 python 里的一个函数
        direction = 0
        x, y = 0, -1

        def in_range(x: int, y: int) -> bool:
            return top <= x <= bottom and left <= y <= right

        res = []
        while len(res) < m * n:
            dx, dy = directions[direction]
            nx, ny = x + dx, y + dy
            if not in_range(nx, ny):
                # 

                """
                ! 注意,这里转向的时候只需要更新一个边界就行了
                因为四条边界的含义是
                    "还没走过的格子构成的矩形",
                而你每转一次向,恰好只走完了这个矩形的一条边,所以只有一条边界需要变。
                """
                if direction == 0:
                    top = x + 1
                elif direction == 1:
                    right = y - 1
                elif direction == 2:
                    bottom = x - 1
                else:
                    left = y + 1
                direction = (direction + 1) % len(directions)
                dx, dy = directions[direction]
                nx, ny = x + dx, y + dy
            res.append(matrix[nx][ny])
            x, y = nx, ny

        return res
```
