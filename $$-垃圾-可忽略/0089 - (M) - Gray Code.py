# result = [0]

# for i in range(5):
#     tmp = []

#     is_zero_first = True
#     for i in range(len(result)):

#         a = result[i] * 2 + (0 if is_zero_first else 1)
#         b = result[i] * 2 + (1 if is_zero_first else 0)
#         tmp.append(a)
#         tmp.append(b)
#         is_zero_first = not is_zero_first
#     result = tmp
# result = [bin(x) for x in result]
# print(result)

# print(0 << 1 + 1)

from typing import List

class Solution:
    def grayCode(self, n: int) -> List[int]:
        result = [0]
        for i in range(n):
            tmp = []
            zero_first = True
            for i in range(len(result)):
                a = result[i] * 2 + (0 if zero_first else 1)
                b = result[i] * 2 + (1 if zero_first else 0)
                tmp.append(a)
                tmp.append(b)
                zero_first = not zero_first
                result = tmp
        return result
    
s = Solution()
input_ = 2
result = s.grayCode(input_)
print(result)

