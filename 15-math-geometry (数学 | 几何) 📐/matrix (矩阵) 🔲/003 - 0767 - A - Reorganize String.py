from collections import Counter
from itertools import chain

"""
1. If the most frequent letter's count > half the length,
then it's impossible to re-arrange

2. Continously put most frequent elements one by one to the
"even_indices + odd_indices" array
"""

class Solution:
    def reorganizeString(self, s: str) -> str:
        counter = Counter(s)
        letter, max_count = counter.most_common()[0]

        
        if max_count > (len(s) + 1) // 2:
            return ""


        ans = [""] * len(s)
        index = 0

        def character_iterator():
            for letter, count in counter.most_common():
                for _ in range(count):
                    yield letter

        indices = range(len(s))
        for index, letter in zip(
            chain(indices[::2], indices[1::2]), character_iterator()
        ):
            ans[index] = letter

        return "".join(ans)


s = Solution()
input_ = "dsfsdfqsdfezvcddegrf"
# input_ = "aaab"
# input_ = "aab"
result = s.reorganizeString(input_)
print(result)
