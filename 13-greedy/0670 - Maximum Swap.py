class Solution:
    def maximumSwap(self, num: int) -> int:
        buckets = [-1] * 10
        digits = list(str(num))
        for index, digit in enumerate(digits):
            buckets[int(digit)] = index
        for index, digit in enumerate(digits):
            for d in range(9, int(digit), -1):
                if buckets[d] > index:
                    digits[buckets[d]], digits[index] = (
                        digits[index],
                        digits[buckets[d]],
                    )
                    return int("".join(digits))
        return int("".join(digits))


s = Solution()
input_ = 2736
result = s.maximumSwap(input_)
print(result)
