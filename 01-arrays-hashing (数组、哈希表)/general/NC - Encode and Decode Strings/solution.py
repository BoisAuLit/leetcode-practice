from typing import List


class Solution:
    def encode(self, strs: List[str]) -> str:
        if len(strs) == 0:
            return "NOTHING"
        result = []
        for str_ in strs:
            result.append(f"{len(str_)}#{str_}")
        return "".join(result)

    def decode(self, s: str) -> List[str]:
        if s == "NOTHING":
            return []

        result = []

        # Decode word one by one
        def extract(i: int) -> bool:
            digits = []
            while s[i] != "#":
                digits.append(s[i])
                i+=1
            length = int("".join(digits))
            result.append(s[i + 1 : i + 1 + length])
            return i + 1 + length

        i = 0
        while True:
            i = extract(i)
            if i == len(s):
                return result


input_ = ["cousin", "cousine", "coupon", "coupure"]
print(f"The input is {input_}")
s = Solution()
a1 = s.encode(input_)
a2 = s.decode(a1)
print(f"The output is {a2}")
