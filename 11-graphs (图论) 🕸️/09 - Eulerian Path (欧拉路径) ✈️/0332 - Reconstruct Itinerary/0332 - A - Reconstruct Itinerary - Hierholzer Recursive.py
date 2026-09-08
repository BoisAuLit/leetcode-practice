"""
📌 信号→模式: 用完所有票的字典序最小行程 → 欧拉路径 Hierholzer：后序 append 再反转
📅 首次: 2025-09-06 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List
from collections import defaultdict

class Solution:
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
