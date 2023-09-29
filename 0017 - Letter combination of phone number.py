from typing import List
from itertools import product

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if len(digits) == 0:
            return []
        mapping = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }
        digits = [mapping[digit]  for digit in digits]
        return list(set("".join(x) for x in list(product(*digits))))
        

s = Solution()
input_ = "2326"
result = s.letterCombinations(input_)
print(result)

"""

"""
        
