from typing import List
from collections import deque


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # ! We only store indices in the deque
        dq = deque()
        res = []

        """
        ! Construct the initial monotonic queue
        Starting this moment, the deque will always 
        be in decreasing order
        """
        for i in range(k):
            while dq and nums[i] >= nums[dq[-1]]:
                dq.pop()
            dq.append(i)
        res.append(nums[dq[0]])

        for i in range(k, len(nums)):
            # ! Here we remove the left end because
            # ! the window moved to right
            if dq and dq[0] == i - k:
                dq.popleft()
            while dq and nums[i] >= nums[dq[-1]]:
                dq.pop()

            dq.append(i)
            # ! The first element in the deque is always the maximum
            res.append(nums[dq[0]])

        return res


s = Solution()
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = s.maxSlidingWindow(nums, k)
print(result)
