"""LC-0444 - Sequence Reconstruction

阶段 3 · Kahn（按入度做 BFS） △ 扩展
题目在问：给一个排列 nums 和一堆它的子序列 sequences，这些子序列能不能"唯一"拼回 nums
点是什么：1..n   边是什么：每个 sequence 里相邻两个数 a, b 给一条 a -> b（a 必须在 b 前面）
和签名题比改了哪一行：207 只问"能不能排出来"，这里要"只能排出一种且就是 nums"：
                     Kahn 每一轮队列里必须恰好 1 个点（有 2 个就能互换 = 不唯一），且出队顺序逐位等于 nums
"""
from collections import deque
from typing import List

##################################################################################################
##### ! Solution 1: Kahn，每轮队列里只能有一个点
##### ! 时间复杂度: O(n + L)，L = 所有 sequence 的总长度   空间复杂度: O(n + L)
##### ! 适用：问"拓扑序是否唯一"的标准写法：唯一 <=> Kahn 过程中队列从不同时出现两个点
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def sequenceReconstruction(self, nums: List[int], sequences: List[List[int]]) -> bool:
        n = len(nums)
        graph = [set() for _ in range(n + 1)]
        indeg = [0] * (n + 1)
        for seq in sequences:
            for a, b in zip(seq, seq[1:]):
                if b not in graph[a]:  # 重边去重，否则入度会多算
                    graph[a].add(b)
                    indeg[b] += 1

        q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
        for x in nums:
            if len(q) != 1 or q[0] != x:
                return False  # ! 队列不止一个 = 顺序不唯一；队头不等于 nums 当前位 = 拼出来的不是 nums
            u = q.popleft()
            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return True  # n 个点按 nums 的顺序一个一个出完了队


##################################################################################################
##### ! Solution 2: 位置检查（nums 里每对相邻元素都得被某个 sequence 钉死）
##### ! 时间复杂度: O(n + L)   空间复杂度: O(n)
##### ! 适用：想清楚"唯一"的本质后的免拓扑写法：拓扑序唯一 <=> 拓扑序里相邻两点之间都有边；
##### !       这里拓扑序就是 nums，所以只需 nums[i] -> nums[i+1] 这 n-1 条边都在某个 sequence 里出现过
##################################################################################################


class Solution_2:
    def sequenceReconstruction(self, nums: List[int], sequences: List[List[int]]) -> bool:
        n = len(nums)
        pos = {x: i for i, x in enumerate(nums)}
        fixed = [False] * n  # fixed[i] = nums[i] 紧接着 nums[i+1] 这个关系被钉死了
        for seq in sequences:
            for a, b in zip(seq, seq[1:]):
                if pos[a] >= pos[b]:
                    return False  # 和 nums 的顺序矛盾（题目保证是子序列，这行只是保险）
                if pos[b] - pos[a] == 1:
                    fixed[pos[a]] = True  # ! 相邻对出现在同一个 sequence 里，这两个位置不能再被别人插队
        return all(fixed[:-1])  # ! n-1 对相邻关系全被钉死，nums 才是唯一解


s = Solution_1()
nums = [1, 2, 3]
sequences = [[1, 2], [1, 3], [2, 3]]
result = s.sequenceReconstruction(nums, sequences)
print(result)  # True
