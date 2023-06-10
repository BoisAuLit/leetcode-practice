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
        for index, letter in enumerate(s):
            if (
                letter in special
                and index < len(s) - 1
                and s[index + 1] in special[letter]
            ):
                sum_ -= mapping[letter]
            else:
                sum_ += mapping[letter]
        return sum_


s = Solution()
input_ = "MCMXCIV"
result = s.romanToInt(input_)
print(result)
