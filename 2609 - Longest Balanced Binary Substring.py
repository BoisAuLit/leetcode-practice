class Solution:
    def findTheLongestBalancedSubstring(self, s: str) -> int:
        i = 0
        while i < len(s) and s[i] != "0":
            i += 1
        result = 0
        while True:
            count_zero = count_one = 0
            while i < len(s) and s[i] == "0":
                count_zero += 1
                i += 1
            while i < len(s) and s[i] == "1":
                count_one += 1
                i += 1
            result = max(result, 2 * min(count_zero, count_one))
            if i == len(s):
                break
        return result


s = Solution()
# input_ = "01000111"  # Expecting 6 --> "000111"
# input_ = "00111" # Expecting 4 --> "0011"
input_ = "111"  # Expecting 0 --> ""

result = s.findTheLongestBalancedSubstring(input_)
print(result)

"""

"""
