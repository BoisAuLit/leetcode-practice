"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
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
- 63 ms
- Beats 73.82%

Memory
- 16.9 MB
- Beats 63.85%
"""
