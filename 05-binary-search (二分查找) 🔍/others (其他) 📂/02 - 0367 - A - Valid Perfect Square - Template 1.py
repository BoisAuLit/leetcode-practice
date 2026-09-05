class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        # ! This is very important
        # ! 1 is special case, if we don't treat it,
        # ! then this won't work.
        if num == 1:
            return True
        left = 0
        right = num // 2
        while left <= right:
            mid = (left + right) // 2
            product = mid * mid
            if product == num:
                return True
            elif product < num:
                left = mid + 1
            else:
                right = mid - 1

        return False
s = Solution()
num = 16
result = s.isPerfectSquare(num)
print(result)
