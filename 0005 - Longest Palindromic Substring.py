class Solution:
    """
    Time complexity: O(N²)
    Space complexity: O(N)
    """
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        dp = [[False] * n for i in range(n)]
        max_ = s[0]
        for i in range(n): # i is the difference
            for j in range(n-i): # j is the starting row position
                if i == 0:
                    dp[j][j+i] = True
                elif i == 1:
                    dp[j][j+i] = s[j] == s[j+i]
                else:
                    dp[j][j+i] = dp[j+1][j+i-1] and s[j] == s[j+i]
                
                if dp[j][j+i] and len(s[j:j+i+1]) > len(max_):
                    max_ = s[j:j+i+1]
        return max_

s = Solution()
input_ = "babad"
result = s.longestPalindrome(input_)
print(result)
