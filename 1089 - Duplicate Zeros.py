from typing import List

"""
Time complexity: O(N)
Space complexity: O(1)
"""


# Solution 1 --> In place
class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
        zeroes = arr.count(0)
        n = len(arr)
        for i in range(n-1, -1, -1):
            if i + zeroes < n:
                arr[i + zeroes] = arr[i]
            if arr[i] == 0: 
                zeroes -= 1
                if i + zeroes < n:
                    arr[i + zeroes] = 0


"""
Time complexity: O(N)
Space complexity: O(N)
"""

# Solution --> 2
class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
        duplicate = arr.copy()
        i1 = i2 = 0
        length = len(arr)
        while i2 < length:
            if duplicate[i1] == 0:
                arr[i2] = 0
                if i2 + 1 >= length:
                    break
                arr[i2 + 1] = 0
                i2 += 1
            else:
                arr[i2] = duplicate[i1]
            i1 += 1
            i2 += 1


s = Solution()

# Expecting [1,0,0,2,3,0,0,4]
input_ = [1, 0, 2, 3, 0, 4, 5, 0]
result = s.duplicateZeros(input_)

print(input_)

"""

"""
