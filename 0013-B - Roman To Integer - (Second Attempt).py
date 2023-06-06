from collections import OrderedDict

"""
Time complexity: O(1)
Space complexity: O(1)
"""


class Solution:
    def romanToInt(self, s: str) -> int:
        mapping = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }
        sum_ = mapping[s[-1]]
        for i in range(len(s) - 1):
            x = mapping[s[i]]
            y = mapping[s[i + 1]]
            sum_ += x * (-1 if x < y else 1)
        return sum_


s = Solution()
input_ = "MCMXCIV"
result = s.romanToInt(input_)
print(result)
