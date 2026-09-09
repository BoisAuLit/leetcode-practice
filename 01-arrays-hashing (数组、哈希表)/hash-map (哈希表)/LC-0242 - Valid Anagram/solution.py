"""LC-0242 - Valid Anagram

合并自 2 个解法文件:
  1. 0242-A - Valid Anagram - (Hashtable Counter).py
  2. 0242-B - Valid Anagram - (Array Counter 👍).py
"""


# ============================================================================
# Solution 1: Hashtable_Counter    (原文件: 0242-A - Valid Anagram - (Hashtable Counter).py)
# ============================================================================

# Time complexity: O()
# Space complexity: O()

input_s_1 = "rat"

input_t_1 = "car"

# Runtime
# - 63 ms
# - Beats 73.82%
#
# Memory
# - 16.9 MB
# - Beats 63.85%

class Solution_1_Hashtable_Counter:
    def isAnagram(self, s: str, t: str) -> bool:
        mapping = {}

        for c in s:
            if c in mapping:
                mapping[c] += 1
            else:
                mapping[c] = 1
        for c in t:
            if c in mapping:
                mapping[c] -= 1
            else:
                mapping[c] = -1

        return all(count == 0 for count in mapping.values())

# ============================================================================
# Solution 2: Array_Counter    (原文件: 0242-B - Valid Anagram - (Array Counter 👍).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(1)

input_s_2 = "rat"

input_t_2 = "car"

# Runtime
# - 62 ms
# - Beats 76.59%
#
# Memory
# - 16.7 MB
# - Beats 91.10%

class Solution_2_Array_Counter:
    def isAnagram(self, s: str, t: str) -> bool:
        counter = [0] * 26
        for c in s:
            counter[ord(c) - 97] += 1
        for c in t:
            counter[ord(c) - 97] -= 1
        return all(i == 0 for i in counter)


if __name__ == "__main__":

    # --- Solution 1: Hashtable_Counter ---
    s = Solution_1_Hashtable_Counter()
    result = s.isAnagram(input_s_1, input_t_1)
    print(result)

    # --- Solution 2: Array_Counter ---
    s = Solution_2_Array_Counter()
    result = s.isAnagram(input_s_2, input_t_2)
    print(result)
