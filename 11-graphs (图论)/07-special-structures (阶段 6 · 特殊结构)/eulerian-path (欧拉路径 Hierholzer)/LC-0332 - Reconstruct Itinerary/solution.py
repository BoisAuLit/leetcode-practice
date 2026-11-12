"""LC-0332 - Reconstruct Itinerary

合并自 2 个解法文件:
  1. 0332 - A - Reconstruct Itinerary - Hierholzer Recursive.py
  2. 0332 - B - Reconstruct Itinerary - Hierholzer Iterative.py

阶段 6 · 特殊结构 · 欧拉路径 Hierholzer ○ 核心
题目在问：从 JFK 出发把所有机票用完(每张恰好一次)，有多条行程时取字典序最小的
点是什么：机场   边是什么：机票(有向边)；题目保证至少存在一条用完所有票的行程 = 欧拉路径一定存在
和模板比改了哪一行：Hierholzer 本体是"走到没票可用才把当前机场记下来(后序入栈)，最后整体反转"；
  字典序最小：邻居倒序排好，每次 pop() 拿到的就是最小的那个
为什么不能贪心直接走：先走字典序小的可能提前走进死胡同、把别的票留着用不完；
  后序入栈正好把死胡同"接到最后面"，反转后它就在行程末尾
"""

from typing import List

from collections import defaultdict


# ============================================================================
# Solution 1: Hierholzer_Recursive    (原文件: 0332 - A - Reconstruct Itinerary - Hierholzer Recursive.py)
# ============================================================================

##################################################################################################
##### ! Solution 1: Hierholzer 递归版 (后序入栈再反转)
##### ! 时间复杂度: O(E log E)   空间复杂度: O(V + E)   排序一次，每张票 pop 一次；递归深度 = 票数
##### ! 适用：最短最常考；票数 ≤ 300，递归不会爆栈
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

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

##################################################################################################
##### ! Solution 2: Hierholzer 迭代版 (显式栈)
##### ! 时间复杂度: O(E log E)   空间复杂度: O(V + E)
##### ! 适用：票数大到递归会爆栈时；栈顶没票可走就弹出记录，和递归版的后序入栈是同一个动作
##################################################################################################

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


s = Solution_1_Hierholzer_Recursive()
tickets = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
result = s.findItinerary(tickets)
print(result)  # ['JFK', 'MUC', 'LHR', 'SFO', 'SJC']

tickets = [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
result = s.findItinerary(tickets)
print(result)  # ['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO']
