"""
Time complexity: O(n)
Space complexity: O(n)
"""

class Solution(object):
    def findShortestSubArray(self, nums):
        left, right, count = {}, {}, {}
        for i, x in enumerate(nums):
            if x not in left:
                left[x] = i
            right[x] = i
            count[x] = count.get(x, 0) + 1

        result = len(nums)
        degree = max(count.values())
        for x in count:
            if count[x] == degree:
                result = min(result, right[x] - left[x] + 1)

        return result


s = Solution()
input_ = [1, 2, 2, 3, 1, 4, 2]  # Expecting 6
# input_ = [1, 2, 2, 3, 1]  # Expecting 2
result = s.findShortestSubArray(input_)
print(result)

"""
Runtime
- 242 ms
- Beats 52.86%

Memory
- 17.7 MB
- Beats 96.19%
"""
