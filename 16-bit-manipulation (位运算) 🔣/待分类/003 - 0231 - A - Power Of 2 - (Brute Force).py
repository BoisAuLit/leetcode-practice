"""
Time complexity: O(logn)
Space complexity: O(logn)
"""


class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        if n <= 0:
            return False
        return all(x == '0' for x in list(bin(n)[3:]))


s = Solution()
# input_ = 1 # Expecting True
# input_ = 3 # Expecting False
input_ = 16 #‚ Expecting True
result = s.isPowerOfTwo(input_)
print(result)

"""
Runtime
- 59ms
- Beats 7.89%

Memory
- 16.24mb
- Beats 65.84%
"""
