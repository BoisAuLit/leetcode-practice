from typing import List
from collections import defaultdict

class Solution_1_Brute_Force:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        zero_index = -1
        product = 1
        for index, num in enumerate(nums):
            if num == 0:
                if zero_index != -1:
                    return [0] * len(nums)
                zero_index = index
            else:
                product *= num
        result = []

        if zero_index == -1:
            for num in nums:
                result.append(product // num)
        else:
            for num in nums:
                if num == 0:
                    result.append(product)
                else:
                    result.append(0)
        return result

class Solution_One_Single_Pass:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        cols = defaultdict(set)
        rows = defaultdict(set)
        squares = defaultdict(set)

        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    continue
                if ( board[r][c] in rows[r]
                    or board[r][c] in cols[c]
                    or board[r][c] in squares[(r // 3, c // 3)]):
                    return False

                cols[c].add(board[r][c])
                rows[r].add(board[r][c])
                squares[(r // 3, c // 3)].add(board[r][c])

        return True
