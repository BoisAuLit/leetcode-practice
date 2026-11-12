"""LC-0433 - Minimum Genetic Mutation

阶段 0 · 状态图 BFS ○ 核心变体
题目在问：8 位基因串每次只能改一个字符，且改完必须在 bank 里，最少几次从 startGene 变到 endGene，到不了返回 -1
点是什么：一个 8 位基因串   边是什么：改一位(8 个位置 × 3 个别的字母 = 24 个候选邻居)，落点必须在 bank 里
和签名题比改了哪一行：752 的邻居是"拨一位 ±1"，deadends 是黑名单(禁止进入)；
    本题邻居是"改一位成 A/C/G/T"，bank 是白名单(只允许进入)。
    和 127 Word Ladder 完全同构，只是字母表从 26 缩到 4、长度固定 8、bank 最多 10 个。
"""
from collections import deque
from typing import List

GENES = "ACGT"

##################################################################################################
##### ! Solution 1: BFS，枚举 24 个候选邻居，只走 bank 里的
##### ! 时间复杂度: O(B · L · 4)  B = bank 大小, L = 8   空间复杂度: O(B · L)
##### ! 适用：752 / 127 的标准写法，状态图 BFS 的模板本身
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        if startGene == endGene:
            return 0
        bank_set = set(bank)  # ! 白名单：只有在 bank 里的串才算合法状态
        if endGene not in bank_set:
            return -1

        queue = deque([(startGene, 0)])
        visited = {startGene}
        while queue:
            gene, steps = queue.popleft()
            for i in range(8):
                for ch in GENES:
                    if ch == gene[i]:
                        continue
                    nxt = gene[:i] + ch + gene[i + 1:]  # ! 改一位 = 走一条边
                    if nxt == endGene:
                        return steps + 1
                    if nxt in bank_set and nxt not in visited:
                        visited.add(nxt)
                        queue.append((nxt, steps + 1))
        return -1


##################################################################################################
##### ! Solution 2: BFS，不枚举邻居，直接扫 bank 找"只差一位"的串
##### ! 时间复杂度: O(B^2 · L)   空间复杂度: O(B)
##### ! 适用：bank 很小(本题 <= 10)时更直观；127 里 bank 上千就不能这么扫
##################################################################################################


class Solution_2:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        if startGene == endGene:
            return 0

        def one_apart(a: str, b: str) -> bool:
            return sum(x != y for x, y in zip(a, b)) == 1  # ! 恰好差一位才有边

        queue = deque([(startGene, 0)])
        remaining = set(bank)  # ! 还没访问过的 bank 串；访问过就从里面删，兼当 visited
        while queue:
            gene, steps = queue.popleft()
            if gene == endGene:
                return steps
            for cand in list(remaining):
                if one_apart(gene, cand):
                    remaining.discard(cand)
                    queue.append((cand, steps + 1))
        return -1


##################################################################################################
##### ! Solution 3: 双向 BFS，起点和终点各扩一层，总是扩小的那一头
##### ! 时间复杂度: O(B · L · 4)  常数更小   空间复杂度: O(B · L)
##### ! 适用：起点终点都已知、分支多时(127 的升级写法)；本题 bank 太小，纯练手
##################################################################################################


class Solution_3:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        if startGene == endGene:
            return 0
        bank_set = set(bank)
        if endGene not in bank_set:
            return -1

        front, back = {startGene}, {endGene}
        visited = {startGene, endGene}
        steps = 0
        while front and back:
            if len(front) > len(back):  # ! 总是扩展小的那一头
                front, back = back, front
            steps += 1
            nxt_front = set()
            for gene in front:
                for i in range(8):
                    for ch in GENES:
                        if ch == gene[i]:
                            continue
                        nxt = gene[:i] + ch + gene[i + 1:]
                        if nxt in back:  # ! 两头碰上了
                            return steps
                        if nxt in bank_set and nxt not in visited:
                            visited.add(nxt)
                            nxt_front.add(nxt)
            front = nxt_front
        return -1


s = Solution_1()
startGene = "AACCGGTT"
endGene = "AAACGGTA"
bank = ["AACCGGTA", "AACCGCTA", "AAACGGTA"]
result = s.minMutation(startGene, endGene, bank)
print(result)  # 2
