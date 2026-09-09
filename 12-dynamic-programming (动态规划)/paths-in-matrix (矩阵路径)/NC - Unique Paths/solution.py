class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[0] * n for _ in range(m)]
        dp[0][0] = 1
        for x in range(m):
            for y in range(n):
                points = [(x - 1, y), (x, y - 1)]
                for a, b in points:
                    if 0 <= a < m and 0 <= b < n:
                        dp[x][y] += dp[a][b]
        return dp[-1][-1]


class Solution_2:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n
        for _ in range(1, m):
            new_dp = [0] * n
            new_dp[0] = dp[0]
            for y in range(1, n):
                new_dp[y] += dp[y] + new_dp[y-1]
            dp = new_dp
        return dp[-1]


s = Solution_2()
m = 3
n = 6
result = s.uniquePaths(m, n)
print(result)
