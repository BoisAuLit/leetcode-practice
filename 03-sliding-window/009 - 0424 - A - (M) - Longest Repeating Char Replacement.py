class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        left = max_length = max_freq = 0
        count = {}

        for right, char in enumerate(s):
            count[char] = count.get(char, 0) + 1
            max_freq = max(max_freq, count[char])

            if (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1

            max_length = max(max_length, right - left + 1)

        return max_length


# # Test case 1: Expecting 4
# solution = Solution()
# s = "ABAB"
# k = 2
# result = solution.characterReplacement(s, k)
# print(result)

# Test case 2: Expecting 4
solution = Solution()
s = "AABABBA"
k = 1
result = solution.characterReplacement(s, k)
print(result)
