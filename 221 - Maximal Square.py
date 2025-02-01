# from typing import List, Tuple


# class Solution:
#     def maximalSquare(self, matrix: List[List[str]]) -> int:
#         m = len(matrix)
#         n = len(matrix[0])

#         # Initialization
#         level = []
#         step = 1

#         for i in range(m):
#             for j in range(n):
#                 if matrix[i][j] == "1":
#                     level.append([(i, j), (i, j)])

#         def in_range(coord):
#             x, y = coord
#             return x >= 0 and x < m and y >= 0 and y < n

#         def expand(start, end):
#             result = []
#             x1, y1 = start
#             x2, y2 = end
            
#             top= bottom= left= right = True
#             for i in range(step):
#                 if matrix[x1-1][y1+step] == '0':
#                     top = False
#                 if matrix[x1+step][y1-1] == '0':
#                     left = False
#                 if matrix[x2+step][y2+1] == '0':
#                     right = False
#                 if matrix[x2+1][y1+step] == '0':
#                     bottom = False
#             if top and left and matrix[x1-1][y1-1]:
#                 result.append([(x1-1, y1-1), end])
#             if top and right and matrix[x1-1][y2]+1
                    
            


                
                

#         for i in range(min(m, n) - 1):

#         print(level)


# s = Solution()

# # Test case 1: Expecting 4
# matrix = [
#     ["1", "0", "1", "0", "0"],
#     ["1", "0", "1", "1", "1"],
#     ["1", "1", "1", "1", "1"],
#     ["1", "0", "0", "1", "0"],
# ]
# result = s.maximalSquare(matrix)
# print(result)
