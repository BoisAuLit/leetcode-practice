from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        res = []
        curr = []
        # fmt: off
        mapping = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz"
        }
        # fmt: on

        def backtrack(i):
            if i == len(digits):
                res.append("".join(curr))
                return
            for ch in mapping[digits[i]]:
                curr.append(ch)
                backtrack(i + 1)
                curr.pop()

        backtrack(0)
        return res


s = Solution()
input_ = "34"
result = s.letterCombinations(input_)
print(result)
