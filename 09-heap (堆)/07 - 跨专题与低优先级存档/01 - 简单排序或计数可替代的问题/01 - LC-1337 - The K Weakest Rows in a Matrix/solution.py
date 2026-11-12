# https://leetcode.com/problems/the-k-weakest-rows-in-a-matrix/

from typing import List


class Solution:
    def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
        m, n = len(mat), len(mat[0])
        tuples = []
        for i in range(m):
            sod = 0
            j = 0
            for j in range(n):
                if mat[i][j] == 0:
                    break
                sod += 1
            tuples.append((sod, i))
        tuples.sort()
        return [x[1] for x in tuples[:k]]


# Test case 1: Expecting [2, 0, 3]
s = Solution()
mat = [
    [1, 1, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1],
]

k = 3
result = s.kWeakestRows(mat, k)
print(result)
