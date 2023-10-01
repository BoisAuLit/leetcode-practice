import heapq
import random

"""
Time complexity: O(N﹒logk)
Space complexity: O(k)
"""


class Solution_Min_Heap:
    def findKthLargest(self, nums, k):
        heap = []
        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)

        return heap[0]


class Solution_Quick_Select:
    def findKthLargest(self, nums, k):
        def quick_select(nums, k):
            pivot = random.choice(nums)
            left, mid, right = [], [], []

            for num in nums:
                if num > pivot:
                    left.append(num)
                elif num < pivot:
                    right.append(num)
                else:
                    mid.append(num)
            
            if k <= len(left):
                return quick_select(left, k)
            
            if len(left) + len(mid) < k:
                return quick_select(right, k - len(left) - len(mid))
            
            return pivot
        
        return quick_select(nums, k)

# class Solution_Quick_Select:
#     def findKthLargest(self, nums, k):
#         k = len(nums) - k

#         def quickSelect(l, r):
#             pivot, p = nums[r], l
#             for i in range(l, r):
#                 if nums[i] <= pivot:
#                     nums[p], nums[i] = nums[i], nums[p]
#                     p += 1
#             nums[p], nums[r] = nums[r], nums[p]
#             if p > k:
#                 return quickSelect(l, p - 1)
#             elif p < k:
#                 return quickSelect(p + 1, r)
#             else:
#                 return nums[p]

#         return quickSelect(0, len(nums) - 1)


s = Solution_Quick_Select()
input_ = [3, 2, 3, 1, 2, 4, 5, 5, 6]
k = 4

result = s.findKthLargest(input_, k)
print(result)

"""

"""
