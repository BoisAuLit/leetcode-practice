from typing import List
from itertools import product

"""
Time complexity: O()
Space complexity: O()
"""


class Solution_Iterative:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        mapping = {
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz'
        }
        combinations = [""]

        for digit in digits:
            new_combinations = []
            for combination in combinations:
                for letter in mapping[digit]:
                    new_combinations.append(combination + letter)
            combinations = new_combinations

        return combinations

class Solution_Recursive:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        phone = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }
        res = []

        def backtrack(combination, next_digits):
            if not next_digits:
                res.append(combination)
                return

            for letter in phone[next_digits[0]]:
                backtrack(combination + letter, next_digits[1:])

        backtrack("", digits)
        return res


class Solution_Python_Builtin:
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
        return list("".join(x) for x in list(product(*digits)))


# s = Solution()
# input_ = "2326"
# result = s.letterCombinations(input_)
# print(result)
"""

"""
