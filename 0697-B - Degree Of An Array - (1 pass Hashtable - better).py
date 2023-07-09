from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def findShortestSubArray(self, nums: List[int]) -> int:
        mapping = {}
        max_frequency = 0
        most_frequent_number_min_length = -1
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
                max_frequency = frequency
                most_frequent_number_min_length = mapping[number]["length"]
            if frequency == max_frequency:
                most_frequent_number_min_length = min(
                    most_frequent_number_min_length, mapping[number]["length"]
                )
        return most_frequent_number_min_length


s = Solution()
input_ = [1, 2, 2, 3, 1, 4, 2]  # Expecting 6
# input_ = [1, 2, 2, 3, 1]  # Expecting 2
result = s.findShortestSubArray(input_)
print(result)

"""
Runtime
- 269 ms
- Beats 26.8%

Memory
- 18.4 MB
- Beats 22.7%
"""
