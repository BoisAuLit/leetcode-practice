from typing import List
import heapq


class Solution:
    def minAbsoluteDifference(self, nums: List[int], x: int) -> int:
        sortedNums = sorted((nums[i], i) for i in range(len(nums)))
        heapLeft, heapRight = [], []
        minDiff = float("inf")

        for i in range(len(sortedNums)):
            val, index = sortedNums[i]
            # min heap. smallest indices pop off (look for match on left side)
            heapq.heappush(heapLeft, (index, val))

            # max heap. biggest indices pop off (look for match on right side)
            heapq.heappush(heapRight, (-index, val))

            # because of sorting, everything in either heap is already less than val. so we just need to do an index check
            # heapLeft we use to check whether current number can be the front half
            while heapLeft and heapLeft[0][0] + x <= index:
                minDiff = min(minDiff, val - heapq.heappop(heapLeft)[1])

            # heapRight we use to check whether current number can be back half
            while heapRight and heapRight[0][0] + x <= -index:
                minDiff = min(minDiff, val - heapq.heappop(heapRight)[1])
            # note that we don't mind popping these off, because we are always checking their distance with the closest valid partner
        return minDiff


# # Test case 1: Expecting 0
# s = Solution()
# nums = [4, 3, 2, 4]
# x = 2
# result = s.minAbsoluteDifference(nums, x)
# print(result)

# Test case 1: Expecting 1
s = Solution()
nums = [5, 3, 2, 10, 15]
x = 1
result = s.minAbsoluteDifference(nums, x)
print(result)
