"""LC-0028 - Find the Index of the First Occurrence in a String

合并自 4 个解法文件:
  1. 0028 - (1) - A - Find The Index Of The First Occur In A String - (Sliding Window) copy.py
  2. 0028 - (1) - B - Find The Index Of The First Occur In A String - (Rabin-Karp Algo - Single Hash).py
  3. 0028 - (1) - C - Find The Index Of The First Occur In A String - (Rabin-Karp Algo - Single Hash - DIY).py
  4. 0028 - (1) - D - Find The Index Of The First Occur In A String - (Rabin-Karp Algo - Double Hash).py
"""


# ============================================================================
# Solution 1: Sliding_Window_copy    (原文件: 0028 - (1) - A - Find The Index Of The First Occur In A String - (Sliding Window) copy.py)
# ============================================================================

# Time complexity: O(nm)
# Space complexity: O(1)

haystack_1 = "leetcode"

needle_1 = "de"

# Runtime
# - 42 ms
# - Beats 64.21%
#
# Memory
# - 16.2 MB
# - Beats 75.20%

class Solution_1_Sliding_Window_copy:
    def strStr(self, haystack_1: str, needle_1: str) -> int:
        if len(haystack_1) < len(needle_1):
            return -1
        for i in range(len(haystack_1) - len(needle_1) + 1):
            if haystack_1[i : i + len(needle_1)] == needle_1:
                return i
        return -1

# ============================================================================
# Solution 2: Single_Hash    (原文件: 0028 - (1) - B - Find The Index Of The First Occur In A String - (Rabin-Karp Algo - Single Hash).py)
# ============================================================================

haystack_2 = "ccaccaacdba"

needle_2 = "dba"


class Solution_2_Single_Hash:
    def strStr(self, haystack_2: str, needle_2: str) -> int:
        m = len(needle_2)
        n = len(haystack_2)
        if n < m:
            return -1

        # CONSTANTS
        RADIX = 26
        MOD = 1_000_000_033
        MAX_WEIGHT = 1

        for _ in range(m):
            MAX_WEIGHT = (MAX_WEIGHT * RADIX) % MOD

        # Function to compute the hash of m-String
        def hash_value(string):
            ans = 0
            factor = 1

            for i in range(m - 1, -1, -1):
                ans += ((ord(string[i]) - 97) * (factor)) % MOD
                factor = (factor * RADIX) % MOD

            return ans % MOD

        # Compute the hash of needle_2
        hash_needle = hash_value(needle_2)

        # Check for each m-substring of haystack_2, starting at window_start
        for window_start in range(n - m + 1):
            if window_start == 0:
                # Compute hash of the First Substring
                hash_hay = hash_value(haystack_2)
            else:
                # Update Hash using Previous Hash Value in O(1)
                hash_hay = (
                    (hash_hay * RADIX) % MOD
                    - ((ord(haystack_2[window_start - 1]) - 97) * MAX_WEIGHT) % MOD
                    + (ord(haystack_2[window_start + m - 1]) - 97)
                    + MOD
                ) % MOD

            # If hash matches, Check Character by Character.
            # Because of Mod, spurious hits can be there.
            if hash_needle == hash_hay:
                for i in range(m):
                    if needle_2[i] != haystack_2[i + window_start]:
                        break
                if i == m - 1:
                    return window_start

        return -1

# ============================================================================
# Solution 3: DIY    (原文件: 0028 - (1) - C - Find The Index Of The First Occur In A String - (Rabin-Karp Algo - Single Hash - DIY).py)
# ============================================================================

# Time complexity
# - Worst case: O(nm)
# - Best case: O(n-m+2m)=O(n+m)
# - n-m for rolling hash
# - 2m
#     - 1m for calculating the hash of the frst m-string in the haystack_3
#     - 1m for calculating the hash of the needle_3
# Space complexity: O(1)

haystack_3 = "ababaabbbbababbaabaaabaabbaaaabbabaabbbbbbabbaabbabbbabbbbbaaabaababbbaabbbabbbaabbbbaaabbababbabbbabaaabbaabbabababbbaaaaaaababbabaababaabbbbaaabbbabb"

needle_3 = "abbabbbabaa"  # Expected result --> 92 (✅ passed)

# Runtime
# - 49 ms
# - Beats 31.42%
#
# Memory
# - 16.3 MB
# - Beats 19.47%

class Solution_3_DIY:
    radix = 26
    mod = 1_000_000_033

    def hash_letter(self, letter: str) -> int:
        return ord(letter) - 97

    def hash_string(self, string: str, m: int) -> int:
        weight = 1
        hash_value = 0
        for index in reversed(range(0, m)):
            hash_value += self.hash_letter(string[index]) * weight % self.mod
            weight *= self.radix
        return hash_value % self.mod

    def strStr(self, haystack_3: str, needle_3: str) -> int:
        n = len(haystack_3)
        m = len(needle_3)
        if n < m:
            return -1
        hash_needle = self.hash_string(needle_3, m)
        max_weight = 1
        for _ in range(m):
            max_weight = max_weight * self.radix % self.mod
        for i in range(0, n - m + 1):
            if i == 0:
                hash_prev = self.hash_string(haystack_3, m)
            else:
                hash_prev = (
                    hash_prev * self.radix % self.mod
                    - self.hash_letter(haystack_3[i - 1]) * max_weight % self.mod
                    + self.hash_letter(haystack_3[i + m - 1]) % self.mod
                ) % self.mod
            if hash_prev == hash_needle:
                for j in range(m):
                    if haystack_3[i + j] != needle_3[j]:
                        break
                if j == m - 1:
                    return i
        return -1

# ============================================================================
# Solution 4: Double_Hash    (原文件: 0028 - (1) - D - Find The Index Of The First Occur In A String - (Rabin-Karp Algo - Double Hash).py)
# ============================================================================

# Time complexity
# - Worst case: O(nm)
# - Best case: O(n-m+2m)=O(n+m)
# - n-m for rolling hash
# - 2m
#     - 1m for calculating the hash of the frst m-string in the haystack_4
#     - 1m for calculating the hash of the needle_4
# Space complexity: O(1)

haystack_4 = "ababaabbbbababbaabaaabaabbaaaabbabaabbbbbbabbaabbabbbabbbbbaaabaababbbaabbbabbbaabbbbaaabbababbabbbabaaabbaabbabababbbaaaaaaababbabaababaabbbbaaabbbabb"

needle_4 = "abbabbbabaa"  # Expected result --> 92 (✅ passed)

# Runtime
# - 49 ms
# - Beats 31.42%
#
# Memory
# - 16.3 MB
# - Beats 19.47%

class Solution_4_Double_Hash:
    def strStr(self, haystack_4: str, needle_4: str) -> int:
        m = len(needle_4)
        n = len(haystack_4)

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

        # Compute hash pairs of needle_4
        hash_needle = hash_pair(needle_4)

        # Check for each m-substring of haystack_4, starting at window_start
        for window_start in range(n - m + 1):
            if window_start == 0:
                # Compute hash pairs of the First Substring
                hash_hay = hash_pair(haystack_4)
            else:
                # Update Hash pairs using Previous using O(1) Value
                hash_hay[0] = (
                    (hash_hay[0] * RADIX_1) % MOD_1
                    - ((ord(haystack_4[window_start - 1]) - 97) * (MAX_WEIGHT_1)) % MOD_1
                    + (ord(haystack_4[window_start + m - 1]) - 97)
                ) % MOD_1
                hash_hay[1] = (
                    (hash_hay[1] * RADIX_2) % MOD_2
                    - ((ord(haystack_4[window_start - 1]) - 97) * (MAX_WEIGHT_2)) % MOD_2
                    + (ord(haystack_4[window_start + m - 1]) - 97)
                ) % MOD_2

            # If the hash matches, return immediately.
            # Probability of Spurious Hit tends to zero
            if hash_needle == hash_hay:
                return window_start
        return -1


if __name__ == "__main__":

    # --- Solution 1: Sliding_Window_copy ---
    s = Solution_1_Sliding_Window_copy()
    result = s.strStr(haystack_1, needle_1)
    print(result)

    # --- Solution 2: Single_Hash ---
    s = Solution_2_Single_Hash()
    result = s.strStr(haystack_2, needle_2)
    print(result)

    # --- Solution 3: DIY ---
    s = Solution_3_DIY()
    result = s.strStr(haystack_3, needle_3)
    print(result)

    # --- Solution 4: Double_Hash ---
    s = Solution_4_Double_Hash()
    result = s.strStr(haystack_4, needle_4)
    print(result)
