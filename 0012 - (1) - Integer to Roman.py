class Solution:
    def intToRoman(self, num: int) -> str:
        mapping = {1: "IVX", 10: "XLC", 100: "CDM", 1000: "M"}
        result = []
        base = 1
        while num:
            digit = num % 10
            if digit == 0:
                base *= 10
                num //= 10
                continue
            letters = mapping[base]
            if 1 <= digit <= 3:
                result.append(letters[0] * digit)
            elif digit == 4:
                result.append(letters[0] + letters[1])
            elif digit == 5:
                result.append(letters[1])
            elif 6 <= digit <= 8:
                result.append(letters[1] + letters[0] * (digit - 5))
            else:
                result.append(letters[0] + letters[2])

            base *= 10
            num //= 10
        return "".join(reversed(result))


s = Solution()
input_ = 1349
result = s.intToRoman(input_)
print(result)
