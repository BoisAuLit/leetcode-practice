class Solution:
    def numberOfWays(self, s: str) -> int:
        ways = 0
        one = zero = zero_one = one_zero = 0
        for c in s:
            if c == "0":
                zero += 1
                one_zero += one
                ways += zero_one
            else:
                one += 1
                zero_one += zero
                ways += one_zero
        return ways


# class Solution:
#     def numberOfWays(self, s: str) -> int:
#         cluster0 = []
#         cluster1 = []
#         ones_so_far = 0
#         zeroes_so_far = 0
#         index = 0

#         while True:
#             one_start_index = index
#             while index < len(s) and s[index] == "1":
#                 ones_so_far += 1
#                 index += 1
#             if index > one_start_index:
#                 cluster1.append((one_start_index, index - 1, zeroes_so_far))
#             if index >= len(s):
#                 break
#             zero_start_index = index
#             while index < len(s) and s[index] == "0":
#                 zeroes_so_far += 1
#                 index += 1
#             cluster0.append((zero_start_index, index - 1, ones_so_far))
#             if index >= len(s):
#                 break

#         def computer_cluster(cluster: List[Tuple[int, int, int]]) -> int:
#             if len(cluster) < 2:
#                 return 0

#             result = 0
#             for i in range(0, len(cluster) - 1):
#                 for j in range(i + 1, len(cluster)):
#                     s1, e1, c1 = cluster[i]
#                     s2, e2, c2 = cluster[j]
#                     result += (e1 - s1 + 1) * (e2 - s2 + 1) * (c2 - c1)
#             return result

#         return computer_cluster(cluster0) + computer_cluster(cluster1)


s = Solution()

# Test case 1: Expecting 6
# input_ = "001101"

# Test case 2: Expecting 3
input_ = "10001"

result = s.numberOfWays(input_)
print(result)
