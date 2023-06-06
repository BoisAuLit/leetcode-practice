from collections import OrderedDict

"""
Time complexity: O(1)
Space complexity: O(1)
"""


class Solution:
    def romanToInt(self, s: str) -> int:
        mapping = dict(
            [
                ("I", 1),
                ("V", 5),
                ("X", 10),
                ("L", 50),
                ("C", 100),
                ("D", 500),
                ("M", 1000),
            ]
        )
        special = {"I": {"V", "X"}, "X": {"L", "C"}, "C": {"D", "M"}, "M": set()}
        sum_ = 0
        for i in range(len(s)):
            if s[i] in special and i < len(s) - 1 and s[i + 1] in special[s[i]]:
                sum_ -= mapping[s[i]]
            else:
                sum_ += mapping[s[i]]
        return sum_


s = Solution()
input_ = "MCMXCIV"
result = s.romanToInt(input_)
print(result)
