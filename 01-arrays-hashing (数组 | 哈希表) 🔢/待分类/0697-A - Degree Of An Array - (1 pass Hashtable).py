from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def findShortestSubArray(self, nums: List[int]) -> int:
        mapping = {}
        max_frequency = 0
        max_frequency_numbers = []
        for index, number in enumerate(nums):
            if number not in mapping:
                mapping[number] = {
                    "first": index,
                    "last": index,
                    "frequency": 1,
                    "length": 1,
                }
            else:
                obj = mapping[number]
                obj["last"] = index
                obj["frequency"] += 1
                obj["length"] = obj["last"] - obj["first"] + 1
            frequency = mapping[number]["frequency"]
            if frequency > max_frequency:
                max_frequency_numbers = [number]
                max_frequency = frequency
            if frequency == max_frequency:
                max_frequency_numbers.append(number)
        return min(
            x["length"] for x in (mapping[y] for y in max_frequency_numbers)
        )


s = Solution()
# input_ = [1, 2, 2, 3, 1, 4, 2]  # Expecting 6
input_ = [1, 2, 2, 3, 1]  # Expecting 6
result = s.findShortestSubArray(input_)
print(result)

"""
Runtime
- 271 ms
- Beats 26.3%

Memory
- 18.6 MB
- Beats 20.96%
"""
