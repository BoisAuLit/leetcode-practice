"""
Time complexity: O(√n)
Space complexity: O(1)
"""


class Solution:
    def mySqrt(self, x: int) -> int:
        i = 0
        for i in range(x+10):
            if i * i > x:
                break
        return i - 1


s = Solution()
input_ = 0
result = s.mySqrt(input_)
print(result)

"""

"""
