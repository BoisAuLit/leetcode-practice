class Solution(object):
    def findLength(self, A, B):
        dp = [[0] * (len(B) + 1) for _ in range(len(A) + 1)]
        max_ = 0
        # dp[i][j]: The longest common prefix of A[i:] and B[j:]
        for i in range(len(A) - 1, -1, -1):
            for j in range(len(B) - 1, -1, -1):
                if A[i] == B[j]:
                    dp[i][j] = dp[i + 1][j + 1] + 1
                    max_ = max(max_, dp[i][j])
        return max_
