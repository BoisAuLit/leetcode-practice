from typing import List
import bisect

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def suggestedProducts(
        self, products: List[str], searchWord: str
    ) -> List[List[str]]:
        products.sort()
        result = []
        for i in range(1, len(searchWord) + 1):
            j = bisect.bisect_left(products, searchWord[:i])

            result.append(
                [p for p in products[j : j + 3] if p.startswith(searchWord[:i])]
            )
        return result


s = Solution()

products = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
searchWord = "mouse"

# products = ["havana"]
# searchWord = "tatiana"
result = s.suggestedProducts(products, searchWord)
print(result)
