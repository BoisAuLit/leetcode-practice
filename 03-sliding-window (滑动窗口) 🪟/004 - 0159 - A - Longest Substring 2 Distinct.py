class Solution:
    def lengthOfLongestSubstringTwoDistinct(self, s: str) -> int:
        n = len(s)
        left = 0
        right = 0
        max_length = 0
        unique = 0
        count = [0] * 128

        while right < n:
            index = ord(s[right])
            count[index] += 1
            if count[index] == 1:
                unique += 1

            while unique >= 3:
                index = ord(s[left])
                count[index] -= 1
                if count[index] == 0:
                    unique -= 1
                left += 1
            max_length = max(max_length, right - left + 1)
            right += 1
        return max_length


# Test case 1: Expecting 3
s = Solution()
input_ = "eceba"
result = s.lengthOfLongestSubstringTwoDistinct(input_)
print(result)
