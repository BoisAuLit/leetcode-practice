from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class SparseVector:
    def __init__(self, nums: List[int]):
        self.hashtable = {index: value for index, value in enumerate(nums) if value != 0}

    def dotProduct(self, vec: "SparseVector") -> int:
        sum_ = 0
        for key, value in self.hashtable.items():
            if key in vec.hashtable:
                sum_ += value * vec.hashtable[key]
        return sum_


nums1 = [1, 0, 0, 2, 3]
nums2 = [0, 3, 0, 4, 0]
vec1 = SparseVector(nums1)
vec2 = SparseVector(nums2)


result = vec1.dotProduct(vec2)
print(result)
