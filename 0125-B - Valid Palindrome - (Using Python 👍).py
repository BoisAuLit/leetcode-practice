"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def isPalindrome(self, s: str) -> bool:
        filtered_chars = (ch for ch in s if ch.isalnum())
        lowercase_filtered_chars = (ch.lower() for ch in filtered_chars)

        filtered_chars_list = list(lowercase_filtered_chars)
        reversed_chars_list = filtered_chars_list[::-1]

        return list(lowercase_filtered_chars) == reversed_chars_list


s = Solution()
# input_ = "A man, a plan, a canal: Panama" # Expecting True
# input_ = "race a car" # Expecting False
# input_ = " "  # Expecting True
input_ = ".,"  # Expecting True
result = s.isPalindrome(input_)
print(result)

"""
Runtime
- 61 ms
- Beats 68.69%

Memory
- 22.7 MB
- Beats 5.59%
"""
