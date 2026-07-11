from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        product = 1
        zero_indices = set()
        for index, number in enumerate(nums):
            if number == 0:
                zero_indices.add(index)
            else:
                product *= number
        result = []
        for index, number in enumerate(nums):
            if index in zero_indices:
                if len(zero_indices) >= 2:
                    result.append(0)
                else:
                    result.append(product)
            else:
                if len(zero_indices) >= 1:
                    result.append(0)
                else:
                    result.append(product // number)
        return result


s = Solution()
input_ = [1, 2, 3, 4]
result = s.productExceptSelf(input_)
print(result)
