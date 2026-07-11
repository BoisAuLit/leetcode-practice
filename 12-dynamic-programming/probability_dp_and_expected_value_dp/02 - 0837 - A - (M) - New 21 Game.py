class Solution:
    def new21Game(self, n: int, k: int, maxPts: int) -> float:
        # If k == 0, Alice stops immediately at 0 points, which is always <= n
        if k == 0:
            return 1.0
        
        # If the max possible score (k-1 + maxPts) is <= n,
        # we can never go above n, so win probability is 1
        if n >= k - 1 + maxPts:
            return 1.0
        
        # Probability array: dp[x] = probability to win from score x
        dp = [0] * (n + maxPts + 1)
        
        # Base case: if k <= x <= n, we already stopped and x <= n => win
        for x in range(k, n + 1):
            dp[x] = 1.0
        
        # Sliding window sum of next maxPts dp values
        window_sum = sum(dp[k : k + maxPts])
        
        # Fill dp backwards from k-1 down to 0
        for x in range(k - 1, -1, -1):
            dp[x] = window_sum / maxPts
            window_sum += dp[x] - dp[x + maxPts]
        
        # dp[0] is the answer: probability to win starting from 0 points
        return dp[0]


# Test case 1: Expecting 0.73278
s = Solution()
n = 21
k = 17
maxPts = 10
result = s.new21Game(n, k, maxPts)
print(result)
