"""
Time complexity: O(logn)
Space complexity: O(1)
"""


class Solution:
    def mySqrt(self, x):
        if x < 2:
            return x
        left = 1
        right = x
        while True:
            if right - left <= 1:
                return left
            pivot = (left + right) // 2
            pivot_square = pivot * pivot
            if pivot_square == x:
                return pivot
            if pivot_square < x:
                left = pivot
            else:
                right = pivot


s = Solution()
input_ = 4
result = s.mySqrt(input_)
print(result)

"""
Runtime
- 54 ms
- Beats 53.32%

Memory
- 16.4 MB
- Beats 15.80%
"""
