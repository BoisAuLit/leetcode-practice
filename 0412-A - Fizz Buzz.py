from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def fizzBuzz(self, n: int) -> List[str]:
        result = []
        for i in range(1, n + 1):
            multiple_3 = i % 3 == 0
            multiple_5 = i % 5 == 0
            if multiple_3 and multiple_5:
                result.append("FizzBuzz")
            elif multiple_3:
                result.append("Fizz")
            elif multiple_5:
                result.append("Buzz")
            else:
                result.append(str(i))
        return result


s = Solution()
input_ = 15
result = s.fizzBuzz(input_)
print(result)
print(
    result
    == [
        "1",
        "2",
        "Fizz",
        "4",
        "Buzz",
        "Fizz",
        "7",
        "8",
        "Fizz",
        "Buzz",
        "11",
        "Fizz",
        "13",
        "14",
        "FizzBuzz",
    ]
)


"""
Runtime
- 65 ms
- Beats 15.77%

Memory
- 17.4 MB
- Beats 28.15%
"""
