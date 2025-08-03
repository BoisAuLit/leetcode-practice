from functools import lru_cache

class Solution:
    @lru_cache(maxsize=None)
    def uniquePaths(self, m: int, n: int) -> int:
        if m == 1 or n == 1:
            return 1
        return self.uniquePaths(m-1, n) + self.uniquePaths(m, n-1)




# Test case 1: Expecting 28
s = Solution()
m = 3
n = 7
result = s.uniquePaths(m, n)
print(result)
