"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        if n <= 0:
            return False
        nb_digits = len(bin(n)[2:])
        mask = (1 << (nb_digits)) - 1
        return ((n ^ mask) + 1) == n


s = Solution()
# input_ = 1 # Expecting True
# input_ = 3  # Expecting False
input_ = 16 #‚ Expecting True
result = s.isPowerOfTwo(input_)
print(result)

"""
Runtime
- 43ms
- Beats 85.24%

Memory
- 16.24mb
- Beats 65.84%
"""
