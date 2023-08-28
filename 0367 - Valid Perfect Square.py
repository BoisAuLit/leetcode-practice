class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        if num == 1:
            return True
        p1 = 1
        p2 = num
        while p2 - p1 > 1:
            mid = (p1 + p2) // 2
            square = mid * mid
            if square == num:
                return True
            elif square > num:
                p2 = mid
            else:
                p1 = mid
        return False


s = Solution()
# input_ = 2000105819
# input_ = 4
input_ = 16
result = s.isPerfectSquare(input_)
print(result)

"""

"""
