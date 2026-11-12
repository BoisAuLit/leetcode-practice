"""LC-0957 - Prison Cells After N Days
https://leetcode.com/problems/prison-cells-after-n-days/description/

Floyd 判圈 · 把"状态"当成链表节点，next 指针 = 演化一天
题目在问：8 间牢房，每天同时变化(两邻居相同则有人，否则空；两端永远空)，问第 n 天长什么样。n 可以到 1e9
为什么是 Floyd 的题：状态空间有限(2^8 = 256，而且第一天之后两端固定为 0，只剩 2^6 = 64 个)，
  每个状态的下一天唯一确定 → 这就是一张函数图 → 从任何起点走下去必然进环，于是 1e9 天可以折叠成环长以内

和链表版的对应关系：
  节点 = 8 元组状态        next(node) = get_next(state)        head = tuple(cells)
  mu  = 进环前的尾巴长度   lam = 环长                          第 n 天 = mu + (n - mu) % lam 步

坑：
  1. 两端必须强制归 0，不能用"邻居相同"去算 cells[0] 和 cells[7]（它们没有两个邻居）
  2. 折叠只能在进环之后做：n < mu 时尾巴上的状态不重复，必须老老实实走 n 步
  3. 状态要用 tuple 不能用 list —— 要进 set / dict 做比较和哈希
"""

##################################################################################################
##### ! Solution 1: Floyd 判圈三阶段（相遇 → 求 mu → 求 lam）+ 折叠 n
##### ! 时间复杂度: O(mu + lam) = O(1)   空间复杂度: O(1)   状态空间上界 256，只存常数个状态
##### ! 适用: 本题最优；O(1) 空间，而且不依赖任何魔数，换成别的演化规则照样能用
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution_1:
    def prisonAfterNDays(self, cells: list[int], n: int) -> list[int]:
        def get_next(state):
            return (0,) + tuple(
                int(state[i - 1] == state[i + 1])
                for i in range(1, 7)
            ) + (0,)

        start = tuple(cells)

        # Phase 1: Find intersection
        slow = fast = start

        while True:
            slow = get_next(slow)
            fast = get_next(get_next(fast))

            if slow == fast:
                break

        # Phase 2: Find cycle entrance (mu)
        slow = start
        mu = 0

        while slow != fast:
            slow = get_next(slow)
            fast = get_next(fast)
            mu += 1

        # Phase 3: Find cycle length (lam)
        lam = 1
        fast = get_next(slow)

        while slow != fast:
            fast = get_next(fast)
            lam += 1

        # Phase 4: Skip complete cycles
        if n >= mu:
            n = mu + (n - mu) % lam

        state = start
        for _ in range(n):
            state = get_next(state)

        return list(state)


##################################################################################################
##### ! Solution 2: 哈希表记"状态 → 第几天"
##### ! 时间复杂度: O(mu + lam) = O(1)   空间复杂度: O(mu + lam) = O(1)，但常数是 256 个状态
##### ! 适用: 面试最容易想到、也最容易讲清楚的写法；不需要推 Floyd 的三个阶段
##### ! 和 Floyd 的取舍: 多花一份状态表换来不用推公式，mu 和 lam 直接从表里读出来
##################################################################################################


def _step(state: tuple[int, ...]) -> tuple[int, ...]:
    """演化一天。两端强制 0（坑 1），中间 6 格看两邻居是否相同。"""
    return (0,) + tuple(int(state[i - 1] == state[i + 1]) for i in range(1, 7)) + (0,)


class Solution_2:
    def prisonAfterNDays(self, cells: list[int], n: int) -> list[int]:
        state = tuple(cells)
        seen = {state: 0}      # ! 状态 → 它是第几天出现的
        history = [state]      # ! 第 d 天的状态，折叠完要靠它直接取答案

        for day in range(1, n + 1):
            state = _step(state)
            if state in seen:
                mu = seen[state]           # ! 环的入口在第 mu 天
                lam = day - mu             # ! 环长
                return list(history[mu + (n - mu) % lam])
            seen[state] = day
            history.append(state)

        return list(state)  # ! n 太小，还没来得及重复就走完了


##################################################################################################
##### ! Solution 3: 魔数 —— n = (n - 1) % 14 + 1，然后老实走
##### ! 时间复杂度: O(14) = O(1)   空间复杂度: O(1)   最短的代码
##### ! 适用: 知道答案时的速通写法；面试里要能解释 14 是怎么来的，否则是在背答案
##### ! 14 的来历: 穷举全部 256 个初始状态，环长只有 1、7、14 三种，都整除 14，
##### !   所以"过 14 天"等价于"原地不动"。减 1 加 1 是因为题目保证 n >= 1，
##### !   要把 n = 14 映射到 14 而不是 0（% 14 会把 14 变成 0，等于一天都不走，错）
##################################################################################################


class Solution_3:
    def prisonAfterNDays(self, cells: list[int], n: int) -> list[int]:
        n = (n - 1) % 14 + 1  # ! 坑: 不能写 n % 14，n = 14 会变成 0

        state = tuple(cells)
        for _ in range(n):
            state = _step(state)

        return list(state)


if __name__ == "__main__":
    def naive(cells, n):
        """逐天模拟，只用来对拍。n 大了会很慢，所以只喂小 n。"""
        state = tuple(cells)
        for _ in range(n):
            state = _step(state)
        return list(state)

    cases = [
        ([0, 1, 0, 1, 1, 0, 0, 1], 7, [0, 0, 1, 1, 0, 0, 0, 0]),
        ([1, 0, 0, 1, 0, 0, 1, 0], 1000000000, [0, 0, 1, 1, 1, 1, 1, 0]),
    ]

    sols = [Solution_1(), Solution_2(), Solution_3()]

    for i, sol in enumerate(sols, 1):
        ok = all(sol.prisonAfterNDays(list(c), n) == want for c, n, want in cases)

        # 对拍: 全部 256 个初始状态 x n = 1..40，和逐天模拟比
        for mask in range(256):
            c = [(mask >> b) & 1 for b in range(8)]
            for n in range(1, 41):
                if sol.prisonAfterNDays(list(c), n) != naive(c, n):
                    ok = False
                    print(f"   Solution_{i} 不一致: cells={c} n={n}")
                    break
            if not ok:
                break

        print(f"Solution_{i}: {'✅ 官方用例 + 256x40 组对拍全过' if ok else '❌'}")
