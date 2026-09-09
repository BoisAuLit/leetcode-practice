"""LC-0387 - First Unique Character in a String

合并自 2 个解法文件:
  1. 0387-A - First Unique Character In A String.py
  2. 0387-B - First Unique Character In A String - (Super easy 👍).py
"""

import collections


# ============================================================================
# Solution 1: First_Unique_Character_In_A_String    (原文件: 0387-A - First Unique Character In A String.py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

input__1 = "leetcode"  # Expecting 0

# Runtime
# - 141 ms
# - Beats 51.78%
#
# Memory
# - 16.5 MB
# - Beats 64.57%

class Solution_1_First_Unique_Character_In_A_String:
    def firstUniqChar(self, s: str) -> int:
        first_index, count = {}, {}
        for index, character in enumerate(s):
            if character not in first_index:
                first_index[character] = index
            count[character] = count.get(character, 0) + 1
        min_left_index = len(s)
        for character, frequency in count.items():
            if frequency == 1 and first_index[character] < min_left_index:
                min_left_index = first_index[character]
        return min_left_index if min_left_index != len(s) else -1

# ============================================================================
# Solution 2: Super_easy    (原文件: 0387-B - First Unique Character In A String - (Super easy 👍).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

input__2 = "leetcode"  # Expecting 0

# Runtime
# - 110 ms
# - Beats 79.86%
#
# Memory
# - 16.5 MB
# - Beats 64.57%

class Solution_2_Super_easy:
    def firstUniqChar(self, s: str) -> int:
        """
        :type s: str
        :rtype: int
        """
        # build hash map : character and how often it appears
        count = collections.Counter(s)

        # find the index
        for idx, ch in enumerate(s):
            if count[ch] == 1:
                return idx
        return -1


if __name__ == "__main__":

    # --- Solution 1: First_Unique_Character_In_A_String ---
    s = Solution_1_First_Unique_Character_In_A_String()
    result = s.firstUniqChar(input__1)
    print(result)

    # --- Solution 2: Super_easy ---
    s = Solution_2_Super_easy()
    result = s.firstUniqChar(input__2)
    print(result)
