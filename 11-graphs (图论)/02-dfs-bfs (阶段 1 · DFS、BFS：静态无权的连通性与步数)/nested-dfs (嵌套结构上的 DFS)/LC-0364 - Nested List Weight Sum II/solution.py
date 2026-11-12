"""LC-0364 - Nested List Weight Sum II

阶段 1 · 嵌套结构上的 DFS · 会员题，手册未单列
题目在问：和 339 一样的嵌套列表，但权重反过来：最深的整数权重 1，最外层权重 maxDepth；求加权和
点是什么：一个 NestedInteger   边是什么：列表 -> 它 getList() 里的每个孩子
和签名题比改了哪一行：339 的权重 = depth；本题权重 = maxDepth - depth + 1，但 maxDepth 要走完才知道，于是
    要么走两遍（先求 maxDepth，再按权重加），
    要么一遍 BFS 用"前缀累加"：每剥一层就把到目前为止见过的整数和再加一遍，外层的数自然被多加了几次，
    要么一遍 DFS 记 (整数和 S, Σ int · depth 记作 D, maxDepth)，答案 = (maxDepth + 1) · S - D
"""
from typing import List


##################################################################################################
##### ! Solution 1: 两遍 BFS，第一遍只数层数拿 maxDepth，第二遍按 maxDepth - depth + 1 加权
##### ! 时间复杂度: O(N)  N = 整数 + 列表总数，走两遍还是 O(N)   空间复杂度: O(W)  一层的宽度
##### ! 适用：最直观的写法，先想到它；缺点是要走两遍
##################################################################################################


class Solution:
    def depthSumInverse(self, nestedList) -> int:
        # Step 1： Use bfs to get max depth, bfs is so cute
        level = nestedList
        max_depth = 0
        while level:
            # ! ⚠️ 边界：这里的 maxDepth 是"剥了几层"，题面定义是"整数的最大深度"；最深处若是空列表（如 [1, [[]]]）会多算一层，
            # !    答案 2 而题面是 1。LeetCode editorial 同款写法能 AC，说明用例里没有；按题面定义的写法见 Solution 3
            max_depth += 1
            next_level = []
            for elem in level:
                if not elem.isInteger():
                    next_level.extend(elem.getList())
            level = next_level

        # Step 2: Do bfs again to get the final result
        level = nestedList
        curr_depth = 0
        res = 0
        while level:
            curr_depth += 1
            next_level = []
            for elem in level:
                if not elem.isInteger():
                    next_level.extend(elem.getList())
                else:
                    res += elem.getInteger() * (max_depth - curr_depth + 1)
            level = next_level
        return res


##################################################################################################
##### ! 本地测试用的 NestedInteger（LeetCode 上已经给了接口，不用贴）+ 把 Python 嵌套 list 转成 List[NestedInteger] 的小工具
##################################################################################################


class NestedInteger:
    def __init__(self, value=None):
        self._int = value
        self._list = [] if value is None else None

    def isInteger(self):
        return self._list is None

    def add(self, elem):
        self._list.append(elem)

    def setInteger(self, value):
        self._int, self._list = value, None

    def getInteger(self):
        return self._int

    def getList(self):
        return self._list


def build(data: list) -> List[NestedInteger]:
    def make(x):
        if isinstance(x, int):
            return NestedInteger(x)
        ni = NestedInteger()
        for child in x:
            ni.add(make(child))
        return ni

    return [make(x) for x in data]


##################################################################################################
##### ! Solution 2: 一遍 BFS，"前缀累加"：每剥一层，把到目前为止所有整数的和再加一遍
##### ! 时间复杂度: O(N)  只走一遍   空间复杂度: O(W)
##### ! 适用：最短、最漂亮的写法，面试里一说就能写；第 d 层的整数被加了 (maxDepth - d + 1) 次，正好是它的权重
##### !       和 Solution 1 一样按"剥了几层"算深度，最深处是空列表时会多算一层（见上面 ⚠️），按题面定义要用 Solution 3
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution（三种并列正确，它一遍、最短、不用先知道 maxDepth）
##################################################################################################


class Solution_2:
    def depthSumInverse(self, nestedList: List[NestedInteger]) -> int:
        level = nestedList
        unweighted = 0  # ! 到目前为止见过的所有整数之和（不带权）
        weighted = 0  # ! 答案
        while level:
            next_level = []
            for elem in level:
                if elem.isInteger():
                    unweighted += elem.getInteger()
                else:
                    next_level.extend(elem.getList())
            weighted += unweighted  # ! 关键行：每剥完一层就把累计和整个加一遍，外层的数留在 unweighted 里被反复加
            level = next_level
        return weighted


##################################################################################################
##### ! Solution 3: 一遍 DFS 记三个数 (S = 整数和, D = Σ int · depth, maxDepth)，答案 = (maxDepth + 1) · S - D
##### ! 时间复杂度: O(N)   空间复杂度: O(D)  递归栈
##### ! 适用：把 339 的结果直接拿来用：权重 maxDepth - depth + 1 展开后 = (maxDepth + 1) · int - int · depth，
##### !       后一项就是 339 的答案；maxDepth 只在碰到整数时更新（按题面"整数的最大深度"），空列表不算
##################################################################################################


class Solution_3:
    def depthSumInverse(self, nestedList: List[NestedInteger]) -> int:
        max_depth = 0

        def dfs(items: List[NestedInteger], depth: int) -> tuple:
            nonlocal max_depth
            s = d = 0
            for elem in items:
                if elem.isInteger():
                    v = elem.getInteger()
                    s += v
                    d += v * depth  # ! 这一项就是 339
                    max_depth = max(max_depth, depth)
                else:
                    cs, cd = dfs(elem.getList(), depth + 1)
                    s += cs
                    d += cd
            return s, d

        s, d = dfs(nestedList, 1)
        return (max_depth + 1) * s - d


s = Solution_2()
result = s.depthSumInverse(build([[1, 1], 2, [1, 1]]))
print(result)  # 8
result = s.depthSumInverse(build([1, [4, [6]]]))
print(result)  # 17
