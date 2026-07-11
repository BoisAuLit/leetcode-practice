import math

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def isStrobogrammatic(self, num: str) -> bool:
        not_allowd_digits = "23457"
        if any(digit in not_allowd_digits for digit in num):
            return False
        mapping = {"0": "0", "9": "6", "6": "9", "8": "8", "1": "1"}
        length = len(num)
        for i in range(math.ceil(length / 2)):
            if mapping[num[i]] != num[length - 1 - i]:
                return False
        return True


s = Solution()

# Expecting True
input_ = "69"
result = s.isStrobogrammatic(input_)

print(result)

"""

"""
