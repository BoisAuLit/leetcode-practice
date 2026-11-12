# Sudoku Solver 笔记

### 📝 2026-09-19 - retry 1

```python
class Solution:
    """
    宫的编号用 (i//3)*3 + j//3,一个整数把 9 个宫映射到 0~8,不用再每次现扫 9 个格子。
    -------------------------------
    rows/cols/boxes 三个集合数组是增量维护的,填一个数就 add,撤销就 remove,不像你原来每个格子都要重新算一遍 get_row | get_col | get_3x3(每次 27 次访问)。
    -------------------------------
    backtrack 返回 bool 是关键:一旦某条路填到底成功了,要立刻 return True 一路传回去,不能再撤销,否则会把已经填好的答案擦掉。你原来的 while 循环没有"试错"这个概念,所以卡住就是永远卡住。
    """
    def solveSudoku(self, board: List[List[str]]) -> None:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        empties = []

        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    empties.append((i, j))
                else:
                    d = board[i][j]
                    rows[i].add(d)
                    cols[j].add(d)
                    boxes[(i // 3) * 3 + j // 3].add(d)

        def backtrack(k: int) -> bool:
            if k == len(empties):
                return True  # 所有空格填完了
            i, j = empties[k]
            b = (i // 3) * 3 + j // 3
            for d in "123456789":
                if d in rows[i] or d in cols[j] or d in boxes[b]:
                    continue
                board[i][j] = d  # 做选择
                rows[i].add(d)
                cols[j].add(d)
                boxes[b].add(d)
                if backtrack(k + 1):
                    return True  # 后面全填通了,一路 return True 回去
                board[i][j] = "."  # 撤销
                rows[i].remove(d)
                cols[j].remove(d)
                boxes[b].remove(d)
            return False  # 9 个数字都试过,这条路走死了

        backtrack(0)
```

### 📝 2026-09-22 - retry 2

```python
class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        # ! rows, cols, boxes, 每一个都要创建 9 get set
        # ! 每一个 set() 代表一行, 一列, 或者 9 宫格
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        unsolved = []

        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    unsolved.append((i, j)) # ! 将 unsolved 的都记录下来, 方便之后使用
                else:
                    d = board[i][j]
                    rows[i].add(d)
                    cols[j].add(d)
                    # ! 这个方法很巧妙, 正好将所有的 i,j 都赢烧到 0-8 这 9 个数字
                    boxes[(i // 3) * 3 + j // 3].add(d)

        def backtrack(k: int) -> bool:
            if k == len(unsolved):
                return True  # 所有空格填完了
            # ! 每次都取一个新的 k 来尝试进行解答
            i, j = unsolved[k]
            # ! 将 i, j 和 0-8 这 9 个数字映射
            b = (i // 3) * 3 + j // 3
            for d in "123456789":
                if d in rows[i] or d in cols[j] or d in boxes[b]:
                    continue
                board[i][j] = d  # 做选择
                rows[i].add(d)
                cols[j].add(d)
                boxes[b].add(d)
                if backtrack(k + 1):
                    return True  # 后面全填通了,一路 return True 回去
                board[i][j] = "."  # 撤销
                rows[i].remove(d)
                cols[j].remove(d)
                boxes[b].remove(d)
            return False  # 9 个数字都试过,这条路走死了

        backtrack(0)
```

### 📝 2026-09-26 - retry 3

```python
class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        nine = [set() for _ in range(9)]

        dots = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    dots.append((i, j))
                else:
                    # ! 注意, 这里不能忘记 else 语句
                    d = board[i][j]
                    b = (i // 3) * 3 + j // 3
                    rows[i].add(d)
                    cols[j].add(d)
                    nine[b].add(d)

        def backtrack(k: int) -> bool:
            if k == len(dots):
                return True

            i, j = dots[k]
            b = (i // 3) * 3 + j // 3
            for d in "123456789":
                # ! 注意, 这里不是以下 
                # ! d in rows or d in cols or d in nine
                if d in rows[i] or d in cols[j] or d in nine[b]:
                    continue

                board[i][j] = d
                rows[i].add(d)
                cols[j].add(d)
                nine[b].add(d)
                if backtrack(k + 1):
                    return True
                board[i][j] = "."
                rows[i].remove(d)
                cols[j].remove(d)
                nine[b].remove(d)

            return False

        backtrack(0)
```
