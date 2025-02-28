from typing import List
import heapq

# ! Using min heap.
# ! Underlying list is of size k
# ! Whenever size exceeds k, then pop the smallest element
# ! To get the smallest element, we just get [0]
class Solution1:
    def findKthLargest(self, nums, k):
        heap = []
        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)
        
        return heap[0]


# ! Using max heap.
# ! Underlying list size is not limited
class Solution2:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        nums = [-x for x in nums]

        heapq.heapify(nums)
        return -heapq.nsmallest(k, nums)[-1]

        # result = -1
        # for i in range(k):
        #     result = -heapq.heappop(nums)
        # return result

s = Solution2()
nums = [3,2,1,5,6,4]
k = 2
result = s.findKthLargest(nums, k)
print(result)


