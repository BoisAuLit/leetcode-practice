"""
Time complexity: O(1)
Space complexity: O(1)
"""


class Solution(object):
    def isPowerOfTwo(self, n):
        if n == 0:
            return False
        return n & (n - 1) == 0


s = Solution()
# input_ = 1 # Expecting True
# input_ = 3  # Expecting False
input_ = 16 #‚ Expecting True
result = s.isPowerOfTwo(input_)
print(result)

"""
"""
