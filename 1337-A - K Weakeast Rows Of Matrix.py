from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def count_soldiers(self, arr: List[int]) -> int:
        count = 0
        for n in arr:
            if n == 0:
                break
            count += 1
        return count

    def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
        order = [[] for _ in range(len(mat[0]) + 1)]
        for index, row in enumerate(mat):
            soldiers = self.count_soldiers(row)
            order[soldiers].append(index)
        result = []
        count = 0
        for arr in order:
            for index in arr:
                result.append(index)
                count += 1
                if count == k:
                    return result


# class Solution:
#     def count_soldiers(self, arr: List[int]) -> int:
#         count = 0
#         for n in arr:
#             if n == 1:
#                 count += 1
#             else:
#                 break
#         return count

#     def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
#         order = [[] for _ in range(len(mat))]
#         for index, row in enumerate(mat):
#             soldiers = self.count_soldiers(row)
#             order[soldiers - 1].append(index)
#         result = []
#         count = 0
#         for arr in order:
#             for index in arr:
#                 result.append(index)
#                 count += 1
#                 if count == k:
#                     return result


s = Solution()

# Expecting [2, 0 , 3]
# mat = [[1, 1, 0, 0, 0], [1, 1, 1, 1, 0], [1, 0, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 1]]
# k = 3

# Expecting [0, 2]
# mat = [[1,0,0,0],
#  [1,1,1,1],
#  [1,0,0,0],
#  [1,0,0,0]]
# k = 2

# Expecting [0]
# mat = [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
# k = 1

# Expecting [1, 0]
mat = [[1, 0], [0, 0], [1, 0]]
k = 2


result = s.kWeakestRows(mat, k)
print(result)

"""
Runtime
- 119ms
- Beats 77.46%

Memory
- 16.60mb
- Beats 96.87%
"""
