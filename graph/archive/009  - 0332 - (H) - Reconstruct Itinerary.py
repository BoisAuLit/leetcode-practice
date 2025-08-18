from typing import List
from collections import defaultdict
from pprint import pprint


class Solution:
    def findItinerary(self, tickets):
        targets = defaultdict(list)
        for a, b in sorted(tickets)[::-1]:
            targets[a] += (b,)
        pprint(targets)
        route = []

        def visit(airport):
            while targets[airport]:
                visit(targets[airport].pop())
            route.append(airport)

        visit("JFK")
        return route[::-1]


s = Solution()
tickets = [
    ["JFK", "SFO"],
    ["JFK", "ATL"],
    ["SFO", "ATL"],
    ["ATL", "JFK"],
    ["ATL", "SFO"],
]

result = s.findItinerary(tickets)
print(result)
