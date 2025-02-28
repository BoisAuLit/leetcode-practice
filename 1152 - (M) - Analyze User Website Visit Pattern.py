from typing import List
from collections import defaultdict, Counter
from itertools import combinations


class Solution:
    def mostVisitedPattern(
        self, username: List[str], timestamp: List[int], website: List[str]
    ) -> List[str]:
        users = defaultdict(list)
        for user, _, site in sorted(
            zip(username, timestamp, website), key=lambda x: x[1]
        ):
            users[user].append(site)
        patterns = Counter()
        for user, sites in users.items():
            patterns.update(Counter(set(combinations(sites, 3))))
        return max(sorted(patterns), key=patterns.get)


s = Solution()

# Test case 1: Expecting ["home","about","career"]


# fmt: off
username = ["joe", "joe", "joe", "james", "james", "james", "james", "mary", "mary", "mary"]
timestamp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
website = ["home", "about", "career", "home", "cart", "maps", "home", "home", "about", "career"]
# fmt: on

result = s.mostVisitedPattern(username, timestamp, website)
print(result)
