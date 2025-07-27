from functools import lru_cache

class Solution_Top_Down_Memoization:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        
        @lru_cache(maxsize=None)
        def memo_solve(p1, p2):
            
            # Base case: If either string is now empty, we can't match
            # up anymore characters.
            if p1 == len(text1) or p2 == len(text2):
                return 0
            
            """
            If the starting letter of both string are the same,
            then we move both pointers 1 position ahead
            """
            if text1[p1] == text2[p2]:
                return 1 + memo_solve(p1 + 1, p2 + 1)
            else:
                """
                If the beginning letter of both strings are not the same,
                then we choose the max between another two recursive solutions
                """
                return max(memo_solve(p1, p2 + 1), memo_solve(p1 + 1, p2))
            
        return memo_solve(0, 0)



class Solution_Bottom_Up_Iterative:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # Make a grid of 0's with len(text2) + 1 columns
        # and len(text1) + 1 rows.
        dp = [[0] * (len(text2) + 1) for _ in range(len(text1) + 1)]

        # Iterate up each column, starting from the last one.
        for col in reversed(range(len(text2))):
            for row in reversed(range(len(text1))):
                # If the corresponding characters for this cell are the same...
                if text2[col] == text1[row]:
                    dp[row][col] = 1 + dp[row + 1][col + 1]
                # Otherwise they must be different...
                else:
                    dp[row][col] = max(dp[row + 1][col], dp[row][col + 1])

        # The original problem's answer is in dp_grid[0][0]. Return it.
        return dp[0][0]


# s = Solution()
# text1 = "actgattag"
# text2 = "gtgtgatcg"
# result = s.longestCommonSubsequence(text1, text2)
# print(result)
