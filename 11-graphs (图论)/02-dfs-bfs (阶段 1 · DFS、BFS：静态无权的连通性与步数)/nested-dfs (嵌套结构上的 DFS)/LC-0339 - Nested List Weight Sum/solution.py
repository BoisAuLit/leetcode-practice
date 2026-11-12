"""LC-0339 - Nested List Weight Sum

阶段 1 · 嵌套结构上的 DFS · 会员题，手册未单列
题目在问：嵌套的整数列表，每个整数乘以它所在的深度（最外层深度 1），求总和
点是什么：一个 NestedInteger（整数或列表）   边是什么：列表 -> 它 getList() 里的每个孩子
和签名题比改了哪一行：200 的 DFS 在网格上找四个邻居；这里"邻居"就是 getList() 的孩子，多带一个 depth 向下传（depth + 1），
    碰到整数就加 getInteger() * depth；BFS 版本一层一层剥，剥到第几层 depth 就是几
"""
from typing import List
from collections import deque

"""
Time complexity: O()
Space complexity: O()
"""

class NestedInteger:
   def __init__(self, value=None):
       """
       If value is not specified, initializes an empty list.
       Otherwise initializes a single integer equal to value.
       """

   def isInteger(self):
       """
       @return True if this NestedInteger holds a single integer, rather than a nested list.
       :rtype bool
       """

   def add(self, elem):
       """
       Set this NestedInteger to hold a nested list and adds a nested integer elem to it.
       :rtype void
       """

   def setInteger(self, value):
       """
       Set this NestedInteger to hold a single integer equal to value.
       :rtype void
       """

   def getInteger(self):
       """
       @return the single integer that this NestedInteger holds, if it holds a single integer
       Return None if this NestedInteger holds a nested list
       :rtype int
       """

   def getList(self):
       """
       @return the nested list that this NestedInteger holds, if it holds a nested list
       Return None if this NestedInteger holds a single integer
       :rtype List[NestedInteger]
       """

##################################################################################################
##### ! Solution 1: 递归 DFS，depth 作为参数向下传
##### ! 时间复杂度: O(N)  N = 整数 + 列表的总个数，每个看一次   空间复杂度: O(D)  递归栈，D = 最大嵌套深度
##### ! 适用：本文件夹的模板写法，嵌套结构最自然的遍历；深度不会很大，不用担心递归上限
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_DFS:
    def depthSum(self, nestedList: List[NestedInteger]) -> int:

        def dfs(nested_list: List[NestedInteger], depth: int):
            total = 0
            for nested in nested_list:
                if nested.isInteger():
                    total += nested.getInteger() * depth
                else:
                    total += dfs(nested.getList(), depth + 1)
            return total

        return dfs(nestedList, 1)

##################################################################################################
##### ! Solution 2: BFS 按层剥，pop 右端、孩子 extendleft 到左端，一轮 len(queue) 正好是一层
##### ! 时间复杂度: O(N)   空间复杂度: O(W)  队列里最多放一层，W = 最宽的一层
##### ! 适用：不想递归时；层号 = depth，和 994 / 286 的"层数 = 步数"是同一个画面
##################################################################################################


class Solution_BFS_Queue:
    def depthSum(self, nestedList: List[NestedInteger]) -> int:
        queue = deque(nestedList)

        depth = 1
        total = 0

        while len(queue) > 0:
            for i in range(len(queue)):
                nested = queue.pop()
                if nested.isInteger():
                    total += nested.getInteger() * depth
                else:
                    queue.extendleft(nested.getList())
            depth += 1

        return total


##################################################################################################
##### ! Solution 3: 显式栈 DFS，栈里放 (元素, 深度)
##### ! 时间复杂度: O(N)   空间复杂度: O(N)  栈
##### ! 适用：递归版的直译，顺序不同但求和不在乎顺序；想避免递归又想保留"深度跟着元素走"的写法时用
##################################################################################################


class Solution_3:
    def depthSum(self, nestedList: List[NestedInteger]) -> int:
        total = 0
        stack = [(ni, 1) for ni in nestedList]  # ! 深度跟着元素进栈，等价于递归版的 depth 参数
        while stack:
            ni, depth = stack.pop()
            if ni.isInteger():
                total += ni.getInteger() * depth
            else:
                stack.extend((child, depth + 1) for child in ni.getList())
        return total


##################################################################################################
##### ! 本地测试用：上面的 NestedInteger 只是 LeetCode 给的接口壳子（方法体是空的），
##### ! 这里继承它补一个能跑的实现 + 一个把 Python 嵌套 list 转成 List[NestedInteger] 的小工具。LeetCode 上不用贴
##################################################################################################


class NestedIntegerImpl(NestedInteger):
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
            return NestedIntegerImpl(x)
        ni = NestedIntegerImpl()
        for child in x:
            ni.add(make(child))
        return ni

    return [make(x) for x in data]


s = Solution_DFS()
result = s.depthSum(build([[1, 1], 2, [1, 1]]))
print(result)  # 10
result = s.depthSum(build([1, [4, [6]]]))
print(result)  # 27
