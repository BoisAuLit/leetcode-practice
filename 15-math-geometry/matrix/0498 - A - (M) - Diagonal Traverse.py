from typing import List


class Solution:
    def findDiagonalOrder(self, mat: List[List[int]]) -> List[int]:
        m = len(mat)
        n = len(mat[0])
        top_right = True
        result = []
        i = j = 0

        def in_range(i: int, j: int) -> bool:
            return 0 <= i < m and 0 <= j < n


        while True:
            result.append(mat[i][j])
            if i == m - 1 and j == n - 1:
                break
            if top_right:
                next_i = i - 1
                next_j = j + 1
                if not in_range(next_i, next_j):
                    top_right = False
                    if next_j >= n:
                        next_i = i + 1
                        next_j = j
                    else:
                        next_i = i
                        next_j = j + 1
            else:
                next_i = i + 1
                next_j = j - 1
                if not in_range(next_i, next_j):
                    top_right = True
                    if next_i >= m:
                        next_i = i
                        next_j = j + 1
                    else:
                        next_i = i + 1
                        next_j = j
            i = next_i
            j = next_j

        return result


# Test case 1: [1,2,4,7,5,3,6,8,9]
s = Solution()
mat = [[1,2,3],[4,5,6],[7,8,9]]
result = s.findDiagonalOrder(mat)
print(result)
