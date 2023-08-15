from typing import List
import math

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        count = 0
        for i in range(len(flowerbed)):
            # Check if the current plot is empty.
            if flowerbed[i] == 0:
                # Check if the left and right plots are empty.
                empty_left_plot = (i == 0) or (flowerbed[i - 1] == 0)
                empty_right_lot = (i == len(flowerbed) - 1) or (
                    flowerbed[i + 1] == 0
                )

                # If both plots are empty, we can plant a flower here.
                if empty_left_plot and empty_right_lot:
                    flowerbed[i] = 1
                    count += 1
                    if count >= n:
                        return True

        return count >= n


# Naïve approach
# class Solution:
#     def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
#         sum_ = 0
#         lp = 0
#         while lp < len(flowerbed) and flowerbed[lp] == 0:
#             lp += 1
#         if lp == len(flowerbed):
#             return (len(flowerbed) + 1) // 2 >= n
#         rp = len(flowerbed) - 1
#         while rp > -1 and flowerbed[rp] == 0:
#             rp -= 1
#         sum_ += math.floor((lp + 0.5) / 2) + math.floor(
#             (len(flowerbed) - 1 - rp + 0.5) / 2
#         )
#         if rp - lp <= 1:
#             return sum_ >= n
#         while lp < rp:
#             while lp < rp and flowerbed[lp] == 1:
#                 lp += 1
#             count = 0
#             while lp < rp and flowerbed[lp] == 0:
#                 count += 1
#                 lp += 1
#             sum_ += (count - 1) // 2
#         return sum_ >= n


s = Solution()


# Testing case 1
# Expecting True (sum_ should be 9)
# flowerbed = []
# flowerbed.extend([0, 0, 0, 0, 0])
# flowerbed.extend([1])
# flowerbed.extend([0, 0, 0, 0, 0])
# flowerbed.extend([1, 1])
# flowerbed.extend([0])
# flowerbed.extend([1])
# flowerbed.extend([0, 0, 0])
# flowerbed.extend([1, 1])
# flowerbed.extend([0, 0, 0, 0, 0, 0])
# flowerbed.extend([1])
# flowerbed.extend([0, 0, 0, 0])
# n = 2

# Testing case 2
# Expecting False (sum_ should be 0)
# flowerbed = [1]
# n = 0


# Testing case 3
# Expecting True (sum_ should be 1)
# flowerbed = [0]
# n = 1

# Testing case 4
# Expecting False (sum_ should be 0)
flowerbed = [1, 0]
n = 1

result = s.canPlaceFlowers(flowerbed, n)
print(f"The result is {result}")
