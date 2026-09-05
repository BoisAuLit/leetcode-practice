"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
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
- 52 ms
- Beats 81.52%

Memory
- 16.6 MB
- Beats 81.44%
"""
