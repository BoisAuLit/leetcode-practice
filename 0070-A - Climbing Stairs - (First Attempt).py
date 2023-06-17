"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 3:
            return n
        return self.climbStairs(n - 1) + self.climbStairs(n - 2)


s = Solution()
input_ = 5
result = s.climbStairs(input_)
print(result)

"""
Stack easily overflow
"""
