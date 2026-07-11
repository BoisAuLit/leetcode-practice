"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def bitwiseComplement(self, n: int) -> int:
        if n == 0:
            return 1
        mask = (1 << (n).bit_length()) - 1
        return n ^ mask


s = Solution()
# input_ = 5  # Expecting 2
# input_ = 7 # Expecting 0
input_ = 10  # Expecting 5
input_ = 0  # Expecting 1
result = s.bitwiseComplement(input_)
print(result)

"""
Runtime
- 47 ms
- Beats 52.55%

Memory
- 16.3 MB
- Beats 63.88%
"""
