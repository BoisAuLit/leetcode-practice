"""LC-0332 - Reconstruct Itinerary

合并自 2 个解法文件:
  1. 0332 - A - Reconstruct Itinerary - Hierholzer Recursive.py
  2. 0332 - B - Reconstruct Itinerary - Hierholzer Iterative.py
"""

from typing import List

from collections import defaultdict


# ============================================================================
# Solution 1: Hierholzer_Recursive    (原文件: 0332 - A - Reconstruct Itinerary - Hierholzer Recursive.py)
# ============================================================================

class Solution_1_Hierholzer_Recursive:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph = defaultdict(list)
        
        for src, dst in sorted(tickets, reverse=True):
            # The neighbors of the current node are sorted in reverse order
            graph[src].append(dst)
            
        itinerary = []
        def dfs(airport):
            while graph[airport]:
                dfs(graph[airport].pop())
            itinerary.append(airport)
        
        dfs("JFK")
        
        return itinerary[::-1]

# ============================================================================
# Solution 2: Hierholzer_Iterative    (原文件: 0332 - B - Reconstruct Itinerary - Hierholzer Iterative.py)
# ============================================================================

class Solution_2_Hierholzer_Iterative:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph = defaultdict(list)
        
        for src, dst in sorted(tickets, reverse=True):
            graph[src].append(dst)
        
        stack = ["JFK"]
        itinerary = []
        
        while stack:
            while graph[stack[-1]]:
                stack.append(graph[stack[-1]].pop())
            itinerary.append(stack.pop())
        
        return itinerary[::-1]
