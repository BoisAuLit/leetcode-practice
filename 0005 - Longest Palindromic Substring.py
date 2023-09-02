class Solution_Manacher:
    def longestPalindrome(self, s: str) -> str:
        s_prime = '#' + '#'.join(s) + '#'
        n = len(s_prime)
        P = [0] * n
        center = radius = 0
        
        for i in range(n):
            mirror = 2 * center - i

            if i < radius:
                P[i] = min(radius - i, P[mirror])

            while (i + 1 + P[i] < n and 
                   i - 1 - P[i] >= 0 and
                   s_prime[i + 1 + P[i]] == s_prime[i - 1 - P[i]]):
                P[i] += 1

            if i + P[i] > radius:
                center = i
                radius = i + P[i]

        max_length = max(P)
        center_index = P.index(max_length)
        start_index = (center_index - max_length) // 2
        longest_palindrome = s[start_index: start_index + max_length]

        return longest_palindrome


class Solution_Dynamic_Programming:
    """
    Time complexity: O(N²)
    Space complexity: O(N)
    """
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        ans = [0, 0]

        for i in range(n):
            dp[i][i] = True

        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                ans = [i, i + 1]

        for diff in range(2, n):
            for i in range(n - diff):
                j = i + diff
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    ans = [i, j]

        i, j = ans
        return s[i : j + 1]



class Solution_Expand_From_Center:
    """
    Time complexity: O(N²)
    Space complexity: O(1)
    """
    def longestPalindrome(self, s: str) -> str:
        def expand(i, j):
            left = i
            right = j
            
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
                
            return right - left - 1
        
        ans = [0, 0]

        for i in range(len(s)):
            odd_length = expand(i, i)
            if odd_length > ans[1] - ans[0] + 1:
                dist = odd_length // 2
                ans = [i - dist, i + dist]

            even_length = expand(i, i + 1)
            if even_length > ans[1] - ans[0] + 1:
                dist = (even_length // 2) - 1
                ans = [i - dist, i + 1 + dist]
                
        i, j = ans
        return s[i:j + 1]
