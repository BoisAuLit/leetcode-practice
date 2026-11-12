"""LC-0997 - Find the Town Judge

阶段 0 · 建图、隐式图、状态图 · 度(入度、出度) ○ 核心
题目在问：n 个人、一堆 "a 信任 b" 的有向边，找那个被其他 n-1 个人都信任、自己谁也不信任的人；没有就 -1
点是什么：人(1..n)   边是什么：a 信任 b 的有向边
和签名题比改了哪一行：不用遍历，只数度：入度 == n-1 且 出度 == 0 的点就是法官
"""
from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


##################################################################################################
##### ! Solution 1: 入度表 + 出度表(用户原版，class 名为 Solution)
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n + E)   E = len(trust)，每个人存两张名单
##### ! 适用：想把"谁信任他 / 他信任谁"两张名单都留下来看的时候；只要个数的话下面 Solution_2 一张数组就够
##################################################################################################


class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        trust_mapping = [
            {"people_trusting_him": [], "people_he_trusts": []}
            for _ in range(n)
        ]
        for pair in trust:
            trust_mapping[pair[0] - 1]["people_he_trusts"].append(pair[1])
            trust_mapping[pair[1] - 1]["people_trusting_him"].append(pair[0])
        for index, t in enumerate(trust_mapping):
            if (
                len(t["people_he_trusts"]) == 0
                and len(t["people_trusting_him"]) == n - 1
            ):
                return index + 1
        return -1




##################################################################################################
##### ! Solution 2: 一张数组记 "入度 - 出度"
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n)   被信任 +1、信任别人 -1，法官的分数正好是 n-1
##### ! 适用：最常考、最短的写法；"入度 n-1 且 出度 0" 合成一个数就能判
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        score = [0] * (n + 1)  # 多开一格，人 1..n 直接当下标
        for a, b in trust:
            score[a] -= 1  # ! a 信任了别人 → 出度 +1 → 扣分
            score[b] += 1  # ! b 被信任 → 入度 +1 → 加分
        for i in range(1, n + 1):
            if score[i] == n - 1:  # ! 只有"出度 0 且 入度 n-1"才能凑到 n-1
                return i
        return -1


##################################################################################################
##### ! Solution 3: 候选人淘汰(同 277 Find the Celebrity 的套路)
##### ! 时间复杂度: O(n + E)   空间复杂度: O(1)   不建任何表，只留一个候选人
##### ! 适用：面试追问 "能不能不开 O(n) 数组"；一条 a→b 边同时说明 a 不是法官、b 还可能是
##################################################################################################


class Solution_3:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        # ! 第一轮：谁信任过别人，谁就出局；最后剩下的那个是唯一候选
        out = [False] * (n + 1)
        for a, _ in trust:
            out[a] = True
        candidate = -1
        for i in range(1, n + 1):
            if not out[i]:
                if candidate != -1:
                    return -1  # ! 两个人都没信任过任何人 → 不可能有人被所有人信任
                candidate = i
        if candidate == -1:
            return -1
        # ! 第二轮：验证候选人确实被其他 n-1 个人信任(trust 里无重复边，数边数即可)
        cnt = sum(1 for _, b in trust if b == candidate)
        return candidate if cnt == n - 1 else -1


s = Solution()

# Expecting 2
# n = 2
# trust = [[1, 2]]

# Expecting 3
# n = 3
# trust = [[1,3],[2,3]]

# Expecting -1
n = 3
trust = [[1,3],[2,3],[3,1]]


result = s.findJudge(n, trust)
print(result)

"""
Runtime
- 770 ms
- Beats 45.96%

Memory
- 22.3 MB
- Beats 13.28%
"""
