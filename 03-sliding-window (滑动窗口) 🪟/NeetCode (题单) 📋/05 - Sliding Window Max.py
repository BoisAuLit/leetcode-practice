from typing import List
import heapq
from collections import deque

class Solution_1:
    """
    Solution 1: Heap
    """
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        heap = []
        output = []
        for i in range(len(nums)):
            heapq.heappush(heap, (-nums[i], i))
            if i >= k - 1:
                while heap[0][1] <= i - k:
                    heapq.heappop(heap)
                output.append(-heap[0][0])
        return output


class Solution_2:
    """
    Solution 2: Deque
    """
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        output = []
        """
        deque 里存的是单调递增的 index
        也就是说:
            - deque 左边代表的元素是最老的 (靠左的)
            - deque 右边代表的元素是最新的 (靠右的)
        """
        q = deque()  # index

        """
        l 和 r 代表的是当前 sliding window 的边界
        """
        l = r = 0

        while r < len(nums):
            """
            规则 1:
                倘若deque 里的元素 X 比当前元素靠左, 且 X 小于当前元素
                那么 X 永远也当不了最大值, 所以可以安全地删除它
            """
            while q and nums[q[-1]] < nums[r]:
                q.pop()
            q.append(r)

            """
            规则 2:
            由于 deque 左边的元素 X 是最老的, X 可能已经小于左边界l, 所以将它们移除
            """
            if l > q[0]:
                q.popleft()

            if (r + 1) >= k:
                output.append(nums[q[0]])
                l += 1
            r += 1

        """
        deque 里的元素的 index 是单调递增的
        deque 里的元素的 index 代表的值是单调递减的
        deque[0] 所代表的元素永远是当前 sliding window 最大的元素
        """

        return output
