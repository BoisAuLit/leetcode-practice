"""
Time complexity
- Worst case: O(nm)
- Best case: O(n-m+2m)=O(n+m)
- n-m for rolling hash
- 2m
    - 1m for calculating the hash of the frst m-string in the haystack
    - 1m for calculating the hash of the needle
Space complexity: O(1)
"""


class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        m = len(needle)
        n = len(haystack)

        if n < m:
            return -1

        # CONSTANTS
        RADIX_1 = 26
        MOD_1 = 10**9 + 33
        MAX_WEIGHT_1 = 1
        RADIX_2 = 27
        MOD_2 = 2**31 - 1
        MAX_WEIGHT_2 = 1

        for _ in range(m):
            MAX_WEIGHT_1 = (MAX_WEIGHT_1 * RADIX_1) % MOD_1
            MAX_WEIGHT_2 = (MAX_WEIGHT_2 * RADIX_2) % MOD_2

        # Function to compute hash_pair of m-String
        def hash_pair(string):
            hash_1 = hash_2 = 0
            factor_1 = factor_2 = 1
            for i in range(m - 1, -1, -1):
                hash_1 += ((ord(string[i]) - 97) * (factor_1)) % MOD_1
                factor_1 = (factor_1 * RADIX_1) % MOD_1
                hash_2 += ((ord(string[i]) - 97) * (factor_2)) % MOD_2
                factor_2 = (factor_2 * RADIX_2) % MOD_2

            return [hash_1 % MOD_1, hash_2 % MOD_2]

        # Compute hash pairs of needle
        hash_needle = hash_pair(needle)

        # Check for each m-substring of haystack, starting at window_start
        for window_start in range(n - m + 1):
            if window_start == 0:
                # Compute hash pairs of the First Substring
                hash_hay = hash_pair(haystack)
            else:
                # Update Hash pairs using Previous using O(1) Value
                hash_hay[0] = (
                    (hash_hay[0] * RADIX_1) % MOD_1
                    - ((ord(haystack[window_start - 1]) - 97) * (MAX_WEIGHT_1)) % MOD_1
                    + (ord(haystack[window_start + m - 1]) - 97)
                ) % MOD_1
                hash_hay[1] = (
                    (hash_hay[1] * RADIX_2) % MOD_2
                    - ((ord(haystack[window_start - 1]) - 97) * (MAX_WEIGHT_2)) % MOD_2
                    + (ord(haystack[window_start + m - 1]) - 97)
                ) % MOD_2

            # If the hash matches, return immediately.
            # Probability of Spurious Hit tends to zero
            if hash_needle == hash_hay:
                return window_start
        return -1


s = Solution()
haystack = "ababaabbbbababbaabaaabaabbaaaabbabaabbbbbbabbaabbabbbabbbbbaaabaababbbaabbbabbbaabbbbaaabbababbabbbabaaabbaabbabababbbaaaaaaababbabaababaabbbbaaabbbabb"
needle = "abbabbbabaa"  # Expected result --> 92 (✅ passed)
result = s.strStr(haystack, needle)
print(result)

########################################################################
########################################################################

# s = Solution()
# haystack = "baabbaaaaaaabbaaaaabbabbababaabbabbbbbabbabbbbbbabababaabbbbbaaabbbbabaababababbbaabbbbaaabbaababbbaabaabbabbaaaabababaaabbabbababbabbaaabbbbabbbbabbabbaabbbaa"
# needle = "bbaaaababa"  # Expected result --> 107 (✅ passed)
# result = s.strStr(haystack, needle)
# print(result)

########################################################################
########################################################################

# s = Solution()
# haystack = "ccaccaacdba"
# needle = "dba"  # Expected result --> 8 (✅ passed)
# result = s.strStr(haystack, needle)
# print(result)

########################################################################
########################################################################

# s = Solution()
# haystack = "abcabcabc"
# needle = "cab" # Expected result --> 2 (✅ passed)
# result = s.strStr(haystack, needle)
# print(result)
"""
Runtime
- 49 ms
- Beats 31.42%

Memory
- 16.3 MB
- Beats 19.47%
"""
