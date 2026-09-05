from typing import List


class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        seq_length = 10
        n = len(s)
        if n <= seq_length:
            return []

        # rolling hash parameters: base 4
        base = 4
        aL = pow(base, seq_length)

        # convert string to array of integers
        to_int = {"A": 0, "C": 1, "G": 2, "T": 3}
        nums = [to_int.get(s[i]) for i in range(n)]

        hash_ = 0
        seen, output = set(), set()
        # iterate over all sequences of length L
        for start in range(n - seq_length + 1):
            # compute hash of the current sequence in O(1) time
            if start != 0:
                # aL = 4^10
                hash_ = hash_ * base - nums[start - 1] * aL + nums[start + seq_length - 1]

            # compute hash of the first sequence in O(L) time
            else:
                for i in range(seq_length):
                    hash_ = hash_ * base + nums[i]

            # update output and hashset of seen sequences
            if hash_ in seen:
                output.add(s[start : start + seq_length])
            seen.add(hash_)
        return list(output)


# Naïve implmentation
# class Solution:
#     def findRepeatedDnaSequences(self, s: str) -> List[str]:
#         n = len(s)
#         if n < 11:
#             return []
#         counter = Counter()
#         result = []
#         for i in range(9, n):
#             sequence = s[i + 1 - 10 : i + 1]
#             counter[sequence] += 1
#             if counter[sequence] == 2:
#                 result.append(sequence)
#         return result


# Test case 1: Expecting ["AAAAACCCCC","CCCCCAAAAA"]
s = Solution()
input_ = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
result = s.findRepeatedDnaSequences(input_)
print(result)
