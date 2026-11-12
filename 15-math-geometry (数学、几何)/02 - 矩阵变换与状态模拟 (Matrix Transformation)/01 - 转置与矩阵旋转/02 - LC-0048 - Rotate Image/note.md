# Rotate Image 笔记（2026-09-09）

顺时针旋转 90° = transpose（转置） + reverse each row（每行反转）

```
1 2 3      1 4 7      7 4 1
4 5 6  ->  2 5 8  ->  8 5 2
7 8 9      3 6 9      9 6 3
  原      转置     每行反转
```

- 转置只换上三角：`for c in range(r + 1, n)`，否则换两次等于没换。
- 逆时针 90° = 转置 + 每列反转（或每行反转 + 转置）。

## 2026-09-13 复习

- 转置只需遍历一个三角（上三角 / 下三角任选其一），主对角线（左上→右下）上的元素转置后不动，完全不用碰：内层从 `r + 1` 开始即可。

### 📝 2026-09-22 - retry 1

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        print(matrix)
        # 1. Transpose
        for i in range(1, n):
            for j in range(i):
                # ! 易错点, 这里一定不要写 matrix[i][j] = matrix[j][i], 那样毫无意义
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        print(matrix)
        # 2. Row reverse
        for i in range(n):
            """
            # ! 易错点: matrix[i].revere() 是 in-place 的, 所以可以直接写 matrix[i].reverse()
            
            # ! 但是 list.reverse() 的返回值是 None, 如果写 matrix[i] = matrix[i].reverse() 那就错了,
            # ! 相当于实在些 matrix[i] = None
            """
            matrix[i].reverse()
```

### 📝 2026-10-04 - retry 2

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        m = len(matrix)
        # Step 1: Transpose
        for i in range(1, m):
            for j in range(i):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        # Step 2: Row reverse
        for i in range(m):
            # ! 在 Python 里, list.reverse() 是 in place 发生的
            matrix[i].reverse()
```

### 📝 2026-10-17 - retry 3

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        # Step 1: Transpose
        for i in range(1, n):
            for j in range(i):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        # Step 2: Reverse each row
        for i in range(n):
            matrix[i].reverse()
```
