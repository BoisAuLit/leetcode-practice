from typing import List


class Solution:
    def sequential_digits(
        self, nb_digits: int, low: int, high: int
    ) -> List[int]:
        start = int("".join(map(str, range(1, nb_digits + 1))))
        end = int("".join(map(str, range(10 - nb_digits, 10))))
        step = int("1" * nb_digits)
        result = []
        tmp = start
        while tmp <= end:
            if tmp < low or tmp > high:
                tmp += step
                continue
            result.append(tmp)
            tmp += step
        return result

    def sequentialDigits(self, low: int, high: int) -> List[int]:
        result = []
        for i in range(len(str(low)), len(str(high)) + 1):
            result.extend(self.sequential_digits(i, low, high))
        return result





s = Solution()

# Test case 1: Expecting [123, 234, 345, 456, 567, 678, 789, 1234, 2345]
low = 100
high = 3000

# Test case 2: Expecting [67,78,89,123]
low = 58
high = 155
result = s.sequentialDigits(low, high)
print(result)
