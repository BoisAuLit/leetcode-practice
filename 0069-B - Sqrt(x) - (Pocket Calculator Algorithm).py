"""
Time complexity: O(1)
Space complexity: O(1)
"""


from math import e, log


class Solution:
    def mySqrt(self, x):
        if x < 2:
            return x

        left = int(e ** (0.5 * log(x)))
        right = left + 1
        return left if right * right > x else right


s = Solution()
input_ = 0
result = s.mySqrt(input_)
print(result)

"""

"""
