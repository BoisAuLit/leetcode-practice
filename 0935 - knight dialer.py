"""
Time complexity: O()
Space complexity: O()
"""


# class Solution_Top_Down_Dynamic_Programming:
#     def knightDialer(self, n: int) -> int:
#         @cache
#         def dp(remain, square):
#             if remain == 0:
#                 return 1
            
#             ans = 0
#             for next_square in jumps[square]:
#                 ans = (ans + dp(remain - 1, next_square)) % MOD
            
#             return ans
        
#         jumps = [
#             [4, 6],
#             [6, 8],
#             [7, 9],
#             [4, 8],
#             [3, 9, 0],
#             [],
#             [1, 7, 0],
#             [2, 6],
#             [1, 3],
#             [2, 4]
#         ]

#         ans = 0
#         MOD = 10 ** 9 + 7
#         for square in range(10):
#             ans = (ans + dp(n - 1, square)) % MOD
        
#         return ans


class Solution_Bottom_Up_Dynamic_Programming:
    def knightDialer(self, n: int) -> int:
        jumps = [
            [4, 6],
            [6, 8],
            [7, 9],
            [4, 8],
            [3, 9, 0],
            [],
            [1, 7, 0],
            [2, 6],
            [1, 3],
            [2, 4]
        ]
        
        MOD = 10 ** 9 + 7
        dp = [[0] * 10 for _ in range(n)]
        for square in range(10):
            dp[0][square] = 1

        for remain in range(1, n):
            for square in range(10):
                ans = 0
                for next_square in jumps[square]:
                    ans = (ans + dp[remain - 1][next_square]) % MOD
                
                dp[remain][square] = ans

        ans = 0
        for square in range(10):
            ans = (ans + dp[n - 1][square]) % MOD
        
        return ans


class Solution_Bottom_Up_Dynamic_Programming_Space_Optimized:
    def knightDialer(self, n: int) -> int:
        jumps = [
            [4, 6],
            [6, 8],
            [7, 9],
            [4, 8],
            [3, 9, 0],
            [],
            [1, 7, 0],
            [2, 6],
            [1, 3],
            [2, 4]
        ]
        
        MOD = 10 ** 9 + 7
        dp = [0] * 10
        prev_dp = [1] * 10
        
        for remain in range(1, n):
            dp = [0] * 10
            for square in range(10):
                ans = 0
                for next_square in jumps[square]:
                    ans = (ans + prev_dp[next_square]) % MOD
                
                dp[square] = ans
                
            prev_dp = dp

        ans = 0
        for square in range(10):
            ans = (ans + prev_dp[square]) % MOD
        
        return ans

class Solution_Final_Solution_Symytry_Bottom_Up_Dynamic_Programming:
    def knightDialer(self, n: int) -> int:
        if n == 1:
            return 10
        
        A = 4
        B = 2
        C = 2
        D = 1
        MOD = 10 ** 9 + 7
        
        for _ in range(n - 1):
            A, B, C, D = (2 * (B + C)) % MOD, A, (A + 2 * D) % MOD, C 
        
        return (A + B + C + D) % MOD
