# Surrounded Regions 笔记

### 📝 2026-10-01 - retry 1

```python
class Solution:
    def solve(self, board: list[list[str]]) -> None:
        m, n = len(board), len(board[0])
        q = deque()
        # 1. 把边界上的 O 全部入队并标记为 #
        for i in range(m):
            for j in range(n):
                if (i in (0, m - 1) or j in (0, n - 1)) and board[i][j] == "O":
                    board[i][j] = "#"
                    q.append((i, j))
        # 2. 从边界 O 出发,把所有连通的 O 都标成 #(这些是"安全"的)
        while q:
            i, j = q.popleft()
            for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] == "O":
                    board[ni][nj] = "#"
                    q.append((ni, nj))
        # 3. 剩下的 O 都是被包围的 → X;# 还原成 O
        for i in range(m):
            for j in range(n):
                board[i][j] = "O" if board[i][j] == "#" else "X"
```

### 📝 2026-10-02 - retry 2

```python
class Solution:
    def solve(self, board: list[list[str]]) -> None:
        m = len(board)
        n = len(board[0])
        q = deque()
        for i in range(m):
            for j in range(n):
                # ! 这里由于优先级的原因, 必须要加括号!!!
                if (i in (0, m - 1) or j in (0, n - 1)) and board[i][j] == "O":
                    board[i][j] = "#"
                    q.append((i, j))
        while q:
            for _ in range(len(q)):
                i, j = q.popleft()
                for di, dj in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and board[ni][nj] == "O":
                        board[ni][nj] = "#"
                        q.append((ni, nj))
        for i in range(m):
            for j in range(n):
                # ! 这里可以简写成这种形式, 更加完美!
                board[i][j] = "O" if board[i][j] == "#" else "X"
```

### 📝 2026-11-02 - retry 3

```python
class Solution:
    def solve(self, board: list[list[str]]) -> None:
        m, n = len(board), len(board[0])
        q = deque()
        for i in range(m):
            for j in range(n):
                # ! 注意，这里 or 和 and 有优先级，所以必须加括号
                if (i in [0, m - 1] or j in [0, n - 1]) and board[i][j] == "O":
                    board[i][j] = "K"
                    q.append((i, j))

        while q:
            i, j = q.popleft()
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] == "O":
                    board[ni][nj] = "K"
                    q.append((ni, nj))
        # ! 这里只用一个循环就可以了，非常得巧妙
        for i in range(m):
            for j in range(n):
                board[i][j] = "O" if board[i][j] == "K" else "X"
```
