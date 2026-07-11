class Solution:
    def findTheLongestBalancedSubstring(self, s: str) -> int:
        i = 0
        result = 0
        while i < len(s):
            zeroes = ones = 0
            while i < len(s) and s[i] == "0":
                zeroes += 1
                i += 1
            while i < len(s) and s[i] == "1":
                ones += 1
                i += 1
            result = max(result, 2 * min(zeroes, ones))
        return result


s = Solution()
# input_ = "01000111"  # Expecting 6 --> "000111"
# input_ = "00111" # Expecting 4 --> "0011"
input_ = "111"  # Expecting 0 --> ""

result = s.findTheLongestBalancedSubstring(input_)
print(result)

"""

"""
