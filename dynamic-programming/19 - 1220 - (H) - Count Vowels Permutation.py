from functools import lru_cache


class Solution_Top_Down_Memoization:
    def countVowelPermutation(self, n: int) -> int:
        letters = ("a", "e", "i", "o", "u")

        mod = 10**9 + 7

        @lru_cache(None)
        def dp(prev: str, remain: int) -> int:
            if remain == 0:
                return 1
            result = 0
            if prev == "a":
                result = dp("e", remain - 1)
            elif prev == "e":
                result = dp("a", remain - 1) + dp("i", remain - 1)
            elif prev == "i":
                result = sum(dp(x, remain - 1) for x in letters if x != "i")
            elif prev == "o":
                result = dp("i", remain - 1) + dp("u", remain - 1)
            else:
                result = dp("a", remain - 1)
            
            return result % mod

        return sum(dp(x, n - 1) for x in letters) % mod


class Solution_Bottom_Up_DP:
    def countVowelPermutation(self, n: int) -> int:
        mod = 10**9 + 7
        
        # dp[i][j] = number of strings of length i ending with vowel j
        # j: 0=a, 1=e, 2=i, 3=o, 4=u
        dp = [[0] * 5 for _ in range(n + 1)]
        
        # Base case: strings of length 1
        for j in range(5):
            dp[1][j] = 1
        
        # Fill the DP table
        for i in range(2, n + 1):
            # a can only be followed by e
            dp[i][0] = dp[i-1][1]  # a <- e
            
            # e can be followed by a or i
            dp[i][1] = (dp[i-1][0] + dp[i-1][2]) % mod  # e <- a, i
            
            # i can be followed by a, e, o, u (all except i)
            dp[i][2] = (dp[i-1][0] + dp[i-1][1] + dp[i-1][3] + dp[i-1][4]) % mod  # i <- a, e, o, u
            
            # o can be followed by i or u
            dp[i][3] = (dp[i-1][2] + dp[i-1][4]) % mod  # o <- i, u
            
            # u can only be followed by a
            dp[i][4] = dp[i-1][0]  # u <- a
        
        # Sum all possibilities for strings of length n
        return sum(dp[n]) % mod


class Solution_Space_Optimized_DP:
    def countVowelPermutation(self, n: int) -> int:
        mod = 10**9 + 7
        
        # Only need previous row, so use 1D arrays
        # prev[j] = number of strings ending with vowel j
        prev = [1] * 5  # Base case: length 1
        
        for _ in range(2, n + 1):
            curr = [0] * 5
            
            # Transition rules (same as above)
            curr[0] = prev[1]  # a depends on e
            curr[1] = (prev[0] + prev[2]) % mod  # e depends on a, i
            curr[2] = (prev[0] + prev[1] + prev[3] + prev[4]) % mod  # i depends on a, e, o, u
            curr[3] = (prev[2] + prev[4]) % mod  # o depends on i, u
            curr[4] = prev[0]  # u depends on a
            
            prev = curr
        
        return sum(prev) % mod




# Test all approaches
s1 = Solution_Top_Down_Memoization()
s2 = Solution_Bottom_Up_DP()
s3 = Solution_Space_Optimized_DP()

n = 5

print("=== Top-Down Memoization ===")
result1 = s1.countVowelPermutation(n)
print(f"Result: {result1}")

print("\n=== Bottom-Up DP (2D table) ===")
result2 = s2.countVowelPermutation(n)
print(f"Result: {result2}")

print("\n=== Space-Optimized DP (1D arrays) ===")
result3 = s3.countVowelPermutation(n)
print(f"Result: {result3}")

print(f"\nAll results match: {result1 == result2 == result3}")
