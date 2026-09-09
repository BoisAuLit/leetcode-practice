"""LC-0125 - Valid Palindrome

合并自 2 个解法文件:
  1. 0125-A - Valid Palindrome - (First Attempt).py
  2. 0125-B - Valid Palindrome - (Using Python 👍).py
"""


# ============================================================================
# Solution 1: First_Attempt    (原文件: 0125-A - Valid Palindrome - (First Attempt).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

input__1 = ".,"  # Expecting True

# Runtime
# - 78 ms
# - Beats 17.88%
#
# Memory
# - 17.2 MB
# - Beats 51.59%

class Solution_1_First_Attempt:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1
        while left < right:
            while left < len(s) and not s[left].isalnum():
                left += 1
            while right > -1 and not s[right].isalnum():
                right -= 1
            if left == len(s) or right == -1:
                return True
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True

# ============================================================================
# Solution 2: Using_Python    (原文件: 0125-B - Valid Palindrome - (Using Python 👍).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

input__2 = ".,"  # Expecting True

# Runtime
# - 61 ms
# - Beats 68.69%
#
# Memory
# - 22.7 MB
# - Beats 5.59%

class Solution_2_Using_Python:
    def isPalindrome(self, s: str) -> bool:
        filtered_chars = (ch for ch in s if ch.isalnum())
        lowercase_filtered_chars = (ch.lower() for ch in filtered_chars)

        filtered_chars_list = list(lowercase_filtered_chars)
        reversed_chars_list = filtered_chars_list[::-1]

        return list(lowercase_filtered_chars) == reversed_chars_list


if __name__ == "__main__":

    # --- Solution 1: First_Attempt ---
    s = Solution_1_First_Attempt()
    result = s.isPalindrome(input__1)
    print(result)

    # --- Solution 2: Using_Python ---
    s = Solution_2_Using_Python()
    result = s.isPalindrome(input__2)
    print(result)
