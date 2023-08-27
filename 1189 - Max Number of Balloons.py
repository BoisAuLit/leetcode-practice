from collections import defaultdict


class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        letters = set("balon")
        counter = defaultdict(lambda: 0)
        for char in text:
            if char in letters:
                counter[char] += 1
        if len(counter) < 5:
            return 0
        counter["l"] //= 2
        counter["o"] //= 2
        return min(counter.values())

s = Solution()

# Expecting 1
text = "nlaebolko"

# Expecting 2
# text = "loonbalxballpoon"

result = s.maxNumberOfBalloons(text)


print(result)

"""

"""
