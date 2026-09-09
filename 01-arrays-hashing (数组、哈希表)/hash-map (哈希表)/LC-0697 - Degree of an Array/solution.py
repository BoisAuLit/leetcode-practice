"""LC-0697 - Degree of an Array

合并自 3 个解法文件:
  1. 0697-A - Degree Of An Array - (1 pass Hashtable).py
  2. 0697-B - Degree Of An Array - (1 pass Hashtable - better).py
  3. 0697-C - Degree Of An Array - (1 pass Hashtable - best 👍).py
"""

from typing import List


# ============================================================================
# Solution 1: Degree_Of_An_Array    (原文件: 0697-A - Degree Of An Array - (1 pass Hashtable).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

input__1 = [1, 2, 2, 3, 1]  # Expecting 6

# Runtime
# - 271 ms
# - Beats 26.3%
#
# Memory
# - 18.6 MB
# - Beats 20.96%

class Solution_1_Degree_Of_An_Array:
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

# ============================================================================
# Solution 2: better    (原文件: 0697-B - Degree Of An Array - (1 pass Hashtable - better).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

input__2 = [1, 2, 2, 3, 1, 4, 2]  # Expecting 6

# Runtime
# - 269 ms
# - Beats 26.8%
#
# Memory
# - 18.4 MB
# - Beats 22.7%

class Solution_2_better:
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

# ============================================================================
# Solution 3: best    (原文件: 0697-C - Degree Of An Array - (1 pass Hashtable - best 👍).py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(n)

input__3 = [1, 2, 2, 3, 1, 4, 2]  # Expecting 6

# Runtime
# - 242 ms
# - Beats 52.86%
#
# Memory
# - 17.7 MB
# - Beats 96.19%

class Solution_3_best(object):
    def findShortestSubArray(self, nums):
        left, right, count = {}, {}, {}
        for i, x in enumerate(nums):
            if x not in left:
                left[x] = i
            right[x] = i
            count[x] = count.get(x, 0) + 1

        result = len(nums)
        degree = max(count.values())
        for x in count:
            if count[x] == degree:
                result = min(result, right[x] - left[x] + 1)

        return result


if __name__ == "__main__":

    # --- Solution 1: Degree_Of_An_Array ---
    s = Solution_1_Degree_Of_An_Array()
    result = s.findShortestSubArray(input__1)
    print(result)

    # --- Solution 2: better ---
    s = Solution_2_better()
    result = s.findShortestSubArray(input__2)
    print(result)

    # --- Solution 3: best ---
    s = Solution_3_best()
    result = s.findShortestSubArray(input__3)
    print(result)
