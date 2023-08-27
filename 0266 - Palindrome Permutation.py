class Solution:
    def canPermutePalindrome(self, s: str) -> bool:
        counter = [0] * 128
        for c in s:
            counter[ord(c)] += 1
        odd_count = 0
        for count in counter:
            if count % 2 == 1:
                odd_count += 1
            if odd_count == 2:
                return False
        return True


s = Solution()

# Expecting False
input_ = "as"
result = s.canPermutePalindrome(input_)
print(result)

"""

"""
