"""LC-2115 - Find All Possible Recipes from Given Supplies

阶段 3 · Kahn（按入度做 BFS） ○ 核心
题目在问：手里有一些原料，菜谱里哪些菜做得出来（做出来的菜也能当别的菜的原料）
点是什么：原料和菜，都是字符串   边是什么：ingredient -> recipe，"有了这个才能做那个"
和签名题比改了哪一行：207 的入度 = 先修课数，这里入度 = 配方里的原料数；
                     207 从所有入度 0 的点出发，这里只从 supplies 出发（缺的原料永远减不到 0，靠它的菜就做不了）
"""
from collections import defaultdict, deque
from typing import List

##################################################################################################
##### ! Solution 1: Kahn（从 supplies 出发按入度 BFS）
##### ! 时间复杂度: O(N + S + I)，N 道菜、S 种原料、I = 所有配方的原料总数   空间复杂度: O(N + I)
##### ! 适用：依赖关系当有向边、问"哪些点最终能被满足"；互相依赖（成环）的菜自然永远出不了队
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        graph = defaultdict(list)  # 原料 -> 需要它的菜
        indeg = {}  # ! 菜的入度 = 还差几种原料
        for r, ings in zip(recipes, ingredients):
            indeg[r] = len(ings)
            for x in ings:
                graph[x].append(r)

        q = deque(supplies)  # ! 起点只有手里的原料，不是"所有入度 0 的点"
        ans = []
        while q:
            x = q.popleft()
            for r in graph[x]:
                indeg[r] -= 1
                if indeg[r] == 0:  # 原料凑齐，这道菜做好了，它自己也能当原料继续往下传
                    ans.append(r)
                    q.append(r)
        return ans


##################################################################################################
##### ! Solution 2: DFS + 记忆化（"做这道菜先把它的原料做出来"）
##### ! 时间复杂度: O(N + S + I)   空间复杂度: O(N + S)（memo + 递归栈）
##### ! 适用：自顶向下想问题时；进入一道菜先标成"做不出"，递归途中又碰到自己 = 配方成环 = 真的做不出
##################################################################################################


class Solution_2:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        need = dict(zip(recipes, ingredients))
        can = {x: True for x in supplies}  # memo：True 有 / 能做，False 做不出

        def dfs(x: str) -> bool:
            if x in can:
                return can[x]
            if x not in need:
                return False  # 既不是原料也不是菜
            can[x] = False  # ! 先标 False 当"正在做"：递归途中再碰到 x 说明配方成环
            can[x] = all(dfs(y) for y in need[x])
            return can[x]

        return [r for r in recipes if dfs(r)]


s = Solution_1()
recipes = ["bread", "sandwich", "burger"]
ingredients = [["yeast", "flour"], ["bread", "meat"], ["sandwich", "meat", "bread"]]
supplies = ["yeast", "flour", "meat"]
result = s.findAllRecipes(recipes, ingredients, supplies)
print(result)  # ['bread', 'sandwich', 'burger']
