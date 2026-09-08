"""
Time complexity: O(N)
Space complexity: O(N)
"""


class Solution:
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
# input_s = "13"
# input_t = "42"

# Expecting False
input_s = "badc"
input_t = "baba"

result = s.isIsomorphic(input_s, input_t)
print(result)

"""
Runtime
- 63 ms
- Beats 33.6%

Memory
- 17.2 MB
- Beats 11.18%
"""
