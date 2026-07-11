from typing import List
import heapq


class Solution:
    def maxAverageRatio(
        self, classes: List[List[int]], extraStudents: int
    ) -> float:
        max_heap = []
        ratio_sum = 0
        for index, (will_pass, total) in enumerate(classes):
            new_ratio = (will_pass + 1) / (total + 1)
            old_ratio = will_pass / total
            ratio_sum += old_ratio
            heapq.heappush(max_heap, (-(new_ratio - old_ratio), index))
        for i in range(extraStudents):
            contribution, index = heapq.heappop(max_heap)
            ratio_sum += -contribution
            will_pass, total = classes[index]
            classes[index] = will_pass + 1, total + 1
            old_ratio = (will_pass + 1) / (total + 1)
            new_ratio = (will_pass + 2) / (total + 2)
            heapq.heappush(max_heap, (-(new_ratio - old_ratio), index))
        return ratio_sum / len(classes)


# Test case 1: Expecting 0.53485
s = Solution()
classes = [[2, 4], [3, 9], [4, 5], [2, 10]]
extraStudents = 4
result = s.maxAverageRatio(classes, extraStudents)
print(result)
