"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        counter = [0] * 26
        for c in s:
            counter[ord(c) - 97] += 1
        for c in t:
            counter[ord(c) - 97] -= 1
        return all(i == 0 for i in counter)


s = Solution()


# Expecting True
# input_s = "anagram"
# input_t = "nagaram"


# Expecting False
input_s = "rat"
input_t = "car"

result = s.isAnagram(input_s, input_t)
print(result)

"""
Runtime
- 62 ms
- Beats 76.59%

Memory
- 16.7 MB
- Beats 91.10%
"""
