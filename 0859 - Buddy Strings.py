"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def buddyStrings(self, s: str, goal: str) -> bool:
        if len(s) != len(goal):
            return False
        diff = []
        counter = [0] * 26
        order_a = ord("a")
        for x, y in zip(s, goal):
            if x != y:
                diff.append([x, y])
            counter[ord(x) - order_a] += 1
        if len(diff) == 0:
            return any(x > 1 for x in counter)
        if len(diff) == 1 or len(diff) > 2:
            return False
        return diff[0] == diff[1][::-1]


s = Solution()

# Expecting True
# str1 = "ab"
# str2 = "ba"
# result = s.buddyStrings(str1, str2)

# Expecting False
# str1 = "aa"
# str2 = "bb"

# Expecting True
# str1 = "aa"
# str2 = "aa"

# Expecting False
str1 = "ab"
str2 = "ab"


result = s.buddyStrings(str1, str2)

print(result)

"""
Runtime
- 47ms
- Beats 71.71%

Memory
16.66mb
- Beats 28.51%
"""
