"""LC-0374 - Guess Number Higher or Lower

合并自 2 个解法文件:
  1. 14 - 0374 - Guess Number Higher or Lower.py
  2. 03 - 0374 - A - Guess Number Lower Higher.py
"""


# ============================================================================
# Solution 1: Guess_Number_Higher_or_Lower    (原文件: 14 - 0374 - Guess Number Higher or Lower.py)
# ============================================================================

class Solution_1_Guess_Number_Higher_or_Lower:
    def guessNumber(self, n: int) -> int:
        left = 1
        right = n
        while left <= right:
            mid = (left + right) // 2
            guess_result = guess(mid)
            if guess_result == 0:
                return mid
            elif guess_result == 1:
                left = mid
            else:
                right = mid
            if right - mid == 1 and guess(right) == 0:
                return right

# ============================================================================
# Solution 2: Guess_Number_Lower_Higher    (原文件: 03 - 0374 - A - Guess Number Lower Higher.py)
# ============================================================================

def guess(num: int) -> int:
    return 0

class Solution_2_Guess_Number_Lower_Higher:
    def guessNumber(self, n: int) -> int:
        left = 1
        right = n
        while left <= right:
            mid = (left+right)//2
            guess_result = guess(mid)
            if guess_result == 1:
                left = mid + 1
            elif guess_result == -1:
                right = mid -1
            else:
                return mid
