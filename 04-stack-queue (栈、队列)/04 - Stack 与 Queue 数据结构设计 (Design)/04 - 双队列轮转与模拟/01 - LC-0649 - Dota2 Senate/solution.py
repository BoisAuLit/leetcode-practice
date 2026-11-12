"""LC-0649 - Dota2 Senate（第二轮自主新增）

Level 1 · 04 Stack 与 Queue 数据结构设计 —— 两个队列 + 轮转（Rotation）的经典模拟
题目在问：'R' 和 'D' 两派议员按给定顺序循环发言，每人可以禁掉一名对方议员，
         双方都最优策略，问最后哪一派获胜。

为什么新增它（和本章其他题的区别）：
  本章前面的题（346 / 622 / 232 / 225）都在**实现**队列；这道题是**用**队列的
  「循环轮转」语义去解一个博弈模拟 —— 队列在这里不是被实现的对象，而是建模工具。
  它补上了「FIFO + 重新入队 = 循环队列」这个在 BFS 之外最常见的队列用法，
  而且不需要任何新数据结构。

决定性观察：
  1. **最优策略是什么？** 轮到我时，我应该禁掉**下一个即将发言的对方议员**。
     理由：禁更靠后的对方议员没有意义 —— 排在前面的那个会先发言、先伤害我方。
     这个贪心是本题唯一需要想的东西。
  2. 把两派的**下标**分别放进两个队列（天然按发言顺序排好）。
     每一轮比较两个队首下标 `r` 和 `d`：**下标小的先发言，它禁掉对方那个**。
  3. 幸存者要参加下一轮，所以把它以 `下标 + n` 重新入队 —— 这正好表达了「绕回下一轮」，
     并且保证跨轮次的先后关系仍然能用下标大小直接比较。
  4. 哪一方的队列先空，另一方获胜。

为什么 `+n` 是对的：原下标在 `[0, n)`，加 n 之后落在 `[n, 2n)`，
      仍然保持同一轮内的相对顺序，并且一定排在本轮所有未发言者之后。

Loop Invariant：两个队列各自按「下一次发言时刻」升序排列；
      队首分别是双方下一个要发言的人。

复杂度：每一轮至少淘汰一个人，总淘汰次数 < n；每次操作 O(1) ⇒ **O(n) 时间，O(n) 空间**。

边界：
  - "RD"    → "Radiant"（R 先手禁掉 D）
  - "RDD"   → "Dire"（R 禁掉第一个 D，第二个 D 禁掉 R）
  - "DDRRR" → "Dire"（两个 D 先手各禁掉一个 R，幸存的 R 再被禁）
  - 全 "R"  → "Radiant"
  - 单字符  → 该派获胜
"""

from collections import deque


##################################################################################################
##### ! Solution 1: 两个下标队列 + 下标 +n 重新入队（标准解）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：所有「多方按固定顺序循环行动、每次淘汰一个对手」的轮转模拟
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def predictPartyVictory(self, senate: str) -> str:
        n = len(senate)
        radiant = deque(i for i, c in enumerate(senate) if c == "R")
        dire = deque(i for i, c in enumerate(senate) if c == "D")
        while radiant and dire:
            r, d = radiant.popleft(), dire.popleft()
            # ! 下标小的先发言，它禁掉刚取出的对方那个（对方不再入队 = 被禁）
            if r < d:
                radiant.append(r + n)   # ! +n 表示「排到下一轮去」
            else:
                dire.append(d + n)
        return "Radiant" if radiant else "Dire"


##################################################################################################
##### ! Solution 2: 单队列 + 两个「待抵消的禁票数」计数器（不用两个队列）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：用来看清「谁禁谁」其实可以退化成一对计数器；思路等价于 Solution_1
##################################################################################################


class Solution_2:
    def predictPartyVictory(self, senate: str) -> str:
        q = deque(senate)
        ban_r = ban_d = 0          # ! 挂在各派头上、还没兑现的禁票
        count_r = senate.count("R")
        count_d = len(senate) - count_r
        while count_r and count_d:
            c = q.popleft()
            if c == "R":
                if ban_r:          # ! 自己先被禁掉一张
                    ban_r -= 1
                    count_r -= 1
                else:
                    ban_d += 1     # ! 否则禁对方下一个
                    q.append(c)
            else:
                if ban_d:
                    ban_d -= 1
                    count_d -= 1
                else:
                    ban_r += 1
                    q.append(c)
        return "Radiant" if count_r else "Dire"


##################################################################################################
##### ! Solution 3: 直接按题意一轮一轮地重建字符串（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 验证「禁下一个对手」这个贪心确实等价于逐轮模拟
##################################################################################################


class Solution_3:
    def predictPartyVictory(self, senate: str) -> str:
        cur = list(senate)
        while "R" in cur and "D" in cur:
            banned = [False] * len(cur)
            for i, c in enumerate(cur):
                if banned[i]:
                    continue                            # ! 本轮已被禁，没有发言权
                for j in list(range(i + 1, len(cur))) + list(range(0, i)):
                    if not banned[j] and cur[j] != c:   # ! 禁掉循环意义下的下一个对手
                        banned[j] = True
                        break
            # ! 关键：轮末才结算。本轮发过言但随后被禁的人，下一轮同样出局
            cur = [c for i, c in enumerate(cur) if not banned[i]]
        return "Radiant" if "R" in cur else "Dire"


if __name__ == "__main__":
    import random

    cases = ["RD", "RDD", "DDRRR", "RRR", "D", "R", "DRRDRDRDRDDRDRDR"]
    for s in cases:
        r = Solution_1().predictPartyVictory(s)
        assert r == Solution_2().predictPartyVictory(s) == Solution_3().predictPartyVictory(s), s
        print(f"{s!r} -> {r}")

    for _ in range(300):                 # ! 随机对拍
        s = "".join(random.choice("RD") for _ in range(random.randint(1, 12)))
        assert (Solution_1().predictPartyVictory(s)
                == Solution_2().predictPartyVictory(s)
                == Solution_3().predictPartyVictory(s)), s
    print("随机对拍 300 组通过 ✓")
