from functools import cache

"""
f(n): Number of ways to fully cover tiles of 2*n
    f(n) = f(n-1) + f(n-2) + 2*p(n-1)

p(n): Number of ways to partially cover tiles of 2*n (with top-right cornoer uncovered)
    - Partially cover means leaving the top-right cornoer tile uncovered
    - Due to symmetry, 2*p(n) = number of ways to partially cover tiles of 2*n
        (wether it be top-right corner uncovered or bottom-right corner uncovered)
    p(n) = p(n-1) + f(n-2)
"""


class Solution_Top_Down_Memoization:
    def numTilings(self, n: int) -> int:
        MOD = 1_000_000_007

        @cache  
        def p(n):  
            if n == 2:
                return 1
            return (p(n - 1) + f(n - 2)) % MOD

        @cache  
        def f(n):  
            if n <= 2:
                return n
            return (f(n - 1) + f(n - 2) + 2 * p(n - 1)) % MOD

        return f(n)


class Solution_Bottom_Up_Iteration:
    def numTilings(self, n: int) -> int:
        MOD = 1_000_000_007
        
        # handle base case scenarios
        if n <= 2:
            return n

        # f[k]: number of ways to "fully cover a board" of width k
        f = [0] * (n + 1)  
        
        # p[k]: number of ways to "partially cover a board" of width k
        p = [0] * (n + 1)  
        
        # initialize f and p with results for the base case scenarios
        f[1] = 1
        f[2] = 2
        p[2] = 1
        
        for k in range(3, n + 1):
            f[k] = (f[k - 1] + f[k - 2] + 2 * p[k - 1]) % MOD
            p[k] = (p[k - 1] + f[k - 2]) % MOD
        return f[n]

class Solutionl_Bottom_Up_Iteration_Space_Optimized:
    def numTilings(self, n: int) -> int:
        MOD = 1_000_000_007
        if n <= 2:
            return n
        fPrevious = 1
        fCurrent = 2
        pCurrent = 1
        for k in range(3, n + 1):
            tmp = fCurrent
            fCurrent = (fCurrent + fPrevious + 2 * pCurrent) % MOD
            pCurrent = (pCurrent + fPrevious) % MOD
            fPrevious = tmp
        return fCurrent
