"""LC-0205 - Isomorphic Strings

合并自 4 个解法文件:
  1. 0205-A - Isomorphic Strings - (Brute Force - 1).py
  2. 0205-B - Isomorphic Strings - (Brute Force - 2).py
  3. 0205-C - Isomorphic Strings - (1 pass hashtable 👍).py
  4. 0205-D - Isomorphic Strings - (Convert to strings).py
"""

from collections import defaultdict


# ============================================================================
# Solution 1: V1    (原文件: 0205-A - Isomorphic Strings - (Brute Force - 1).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

input_s_1 = "bbbaaaba"

input_t_1 = "aaabbbba"

# Runtime
# - 75 ms
# - Beats 8.6%
#
# Memory
# - 19.4 MB
# - Beats 5.25%

class Solution_1_V1:
    def isIsomorphic(self, s: str, t: str) -> bool:
        counter1 = defaultdict(list)
        counter2 = defaultdict(list)
        for index, letter in enumerate(s):
            counter1[letter].append(index)
        for index, letter in enumerate(t):
            counter2[letter].append(index)
        set1 = set(str(i) for i in counter1.values())
        set2 = set(str(i) for i in counter2.values())
        return set1 == set2

# ============================================================================
# Solution 2: V2    (原文件: 0205-B - Isomorphic Strings - (Brute Force - 2).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

input_s_2 = "13"

input_t_2 = "42"

# Runtime
# - 67 ms
# - Beats 19.76%
#
# Memory
# - 19.5 MB
# - Beats 5.25%

class Solution_2_V2:
    def isIsomorphic(self, s: str, t: str) -> bool:
        arr1 = [[] for _ in range(128)]
        arr2 = [[] for _ in range(128)]
        for index, letter in enumerate(s):
            arr1[ord(letter)].append(index)
        for index, letter in enumerate(t):
            arr2[ord(letter)].append(index)
        set1 = set(str(l) for l in arr1 if len(l) > 0)
        set2 = set(str(l) for l in arr2 if len(l) > 0)
        return set1 == set2

# ============================================================================
# Solution 3: Isomorphic_Strings    (原文件: 0205-C - Isomorphic Strings - (1 pass hashtable 👍).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(1)

input_s_3 = "badc"

input_t_3 = "baba"

# Runtime
# - 52 ms
# - Beats 81.52%
#
# Memory
# - 16.6 MB
# - Beats 81.44%

class Solution_3_Isomorphic_Strings:
    def isIsomorphic(self, s: str, t: str) -> bool:
        mapping = {}
        mapped_letters = []
        for c1, c2 in zip(s, t):
            if c1 in mapping:
                if mapping[c1] != c2:
                    return False
            else:
                if c2 in mapped_letters:
                    return False
                mapping[c1] = c2
                mapped_letters.append(c2)
        return True

# ============================================================================
# Solution 4: Convert_to_strings    (原文件: 0205-D - Isomorphic Strings - (Convert to strings).py)
# ============================================================================

# Time complexity: O(N)
# Space complexity: O(N)

input_s_4 = "badc"

input_t_4 = "baba"

# Runtime
# - 63 ms
# - Beats 33.6%
#
# Memory
# - 17.2 MB
# - Beats 11.18%

class Solution_4_Convert_to_strings:
    def isIsomorphic(self, s: str, t: str) -> bool:
        mapping1 = {}
        mapping2 = {}
        l1 = []
        l2 = []
        for index, letter in enumerate(s):
            if letter in mapping1:
                l1.append(mapping1[letter])
            else:
                mapping1[letter] = index
                l1.append(index)
        for index, letter in enumerate(t):
            if letter in mapping2:
                l2.append(mapping2[letter])
            else:
                mapping2[letter] = index
                l2.append(index)
        print("l1 =", l1)
        print("l2 =", l2)
        for a, b in zip(l1, l2):
            if a != b:
                return False
        return True


if __name__ == "__main__":

    # --- Solution 1: V1 ---
    s = Solution_1_V1()
    result = s.isIsomorphic(input_s_1, input_t_1)
    print(result)

    # --- Solution 2: V2 ---
    s = Solution_2_V2()
    result = s.isIsomorphic(input_s_2, input_t_2)
    print(result)

    # --- Solution 3: Isomorphic_Strings ---
    s = Solution_3_Isomorphic_Strings()
    result = s.isIsomorphic(input_s_3, input_t_3)
    print(result)

    # --- Solution 4: Convert_to_strings ---
    s = Solution_4_Convert_to_strings()
    result = s.isIsomorphic(input_s_4, input_t_4)
    print(result)
