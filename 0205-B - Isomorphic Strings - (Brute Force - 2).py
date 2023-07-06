"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
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


s = Solution()

# Expecting True
# input_s = "egg"
# input_t = "add"

# Expecting False
# input_s = "foo"
# input_t = "bar"

# Expecting True
# input_s = "paper"
# input_t = "title"

# Expecting False
# input_s = "bbbaaaba"
# input_t = "aaabbbba"

# Expecting False
input_s = "13"
input_t = "42"

result = s.isIsomorphic(input_s, input_t)
print(result)

"""
Runtime
- 67 ms
- Beats 19.76%

Memory
- 19.5 MB
- Beats 5.25%
"""
