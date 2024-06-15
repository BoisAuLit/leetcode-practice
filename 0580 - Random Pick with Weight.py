from typing import List
import random


"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def __init__(self, w: List[int]):
        self.prefix_sums = []
        prefix_sum = 0
        for weight in w:
            prefix_sum += weight
            self.prefix_sums.append(prefix_sum)
        self.total_sum = prefix_sum

    def pickIndex(self) -> int:
        target = self.total_sum * random.random()
        # run a binary search to find the target zone
        low, high = 0, len(self.prefix_sums)
        while low < high:
            mid = low + (high - low) // 2
            if target > self.prefix_sums[mid]:
                low = mid + 1
            else:
                high = mid
        return low


# class Solution:

#     def __init__(self, w: List[int]):
#         self.array = []
#         sum_ = 0

#         for index, num in enumerate(w):
#             sum_ += num
#             self.array.append({"weight": num, "index": index, "start": sum_ - num + 1, "end": sum_})
#         self.sum_ = sum_

#     def pickIndex(self) -> int:
#         random_int = randint(1, self.sum_)
#         print("random int:", random_int)
#         left = 0
#         right = len(self.array) - 1
#         while True:
#             mid = math.ceil((left + right) / 2)
#             if random_int > self.array[mid]["end"]:
#                 left = mid
#                 continue
#             elif random_int < self.array[mid]["start"]:
#                 right = mid-1
#             else:
#                 return self.array[mid]["index"]


s = Solution([1, 2, 3, 4])

for i in range(100):
    print(s.pickIndex())
