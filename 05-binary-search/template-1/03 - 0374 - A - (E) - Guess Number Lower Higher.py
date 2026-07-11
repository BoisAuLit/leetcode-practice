def guess(num: int) -> int:
    return 0

class Solution:
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
