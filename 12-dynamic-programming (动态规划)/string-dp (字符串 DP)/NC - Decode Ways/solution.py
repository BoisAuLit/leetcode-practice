class Solution:
    def numDecodings(self, s: str) -> int:
        n = len(s)

        # dp[i] = number of ways to decode s[:i]
        dp = [0] * (n + 1)

        # Empty string has one way:
        # decode nothing
        dp[0] = 1

        # First character
        dp[1] = 0 if s[0] == "0" else 1

        for i in range(2, n + 1):
            # 1. Decode the last digit alone
            if s[i - 1] != "0":
                dp[i] += dp[i - 1]

            # 2. Decode the last two digits together
            if "10" <= s[i - 2 : i] <= "26":
                dp[i] += dp[i - 2]

        return dp[n]


s = Solution()
# input_ = "10"
# input_ = "26"
# input_ = "10011"
input_ = "1212121212121212121212121212121212121212121277777777777777777777777777777777777777777777777777777777"
input_ = "1110"
result = s.numDecodings(input_)
print(result)
