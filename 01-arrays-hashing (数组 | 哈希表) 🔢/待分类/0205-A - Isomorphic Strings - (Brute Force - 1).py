from collections import defaultdict

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        counter1 = defaultdict(list)
        counter2 = defaultdict(list)
        for index, letter in enumerate(s):
            counter1[letter].append(index)
        for index, letter in enumerate(t):
            counter2[letter].append(index)
        set1 = set(str(i) for i in counter1.values())
        set2 = set(str(i) for i in counter2.values())
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
input_s = "bbbaaaba"
input_t = "aaabbbba"

result = s.isIsomorphic(input_s, input_t)
print(result)

"""
Runtime
- 75 ms
- Beats 8.6%

Memory
- 19.4 MB
- Beats 5.25%
"""
