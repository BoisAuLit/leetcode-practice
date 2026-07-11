class Solution:
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
