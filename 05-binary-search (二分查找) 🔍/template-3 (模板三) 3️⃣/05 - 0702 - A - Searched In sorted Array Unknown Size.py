# """
# This is ArrayReader's API interface.
# You should not implement it, or speculate about its implementation
# """
class ArrayReader:
    def get(self, index: int) -> int:
        pass


class Solution:
    def search(self, reader: "ArrayReader", target: int) -> int:
        left = 0
        right = 1
        while True:
            next_ = reader.get(right)
            if next_ == -1 or next_ > target:
                break
            right *= 2
        while left <= right:
            mid = (left + right) // 2
            mid_value = reader.get(mid)
            if mid_value == target:
                return mid
            elif mid_value < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
