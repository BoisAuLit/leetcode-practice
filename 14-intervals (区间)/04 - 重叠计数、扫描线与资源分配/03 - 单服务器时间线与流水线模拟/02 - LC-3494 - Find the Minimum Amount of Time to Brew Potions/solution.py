# https://leetcode.com/problems/find-the-minimum-amount-of-time-to-brew-potions/

"""LC-3494 - Find the Minimum Amount of Time to Brew Potions

Level 1 · 04 重叠计数、扫描线与资源分配 → Level 2 · 03 单服务器时间线与流水线模拟

题目在问：`n` 个巫师排成**流水线**，`m` 瓶药依次通过。巫师 `i` 处理第 `j` 瓶的耗时是
`skill[i] * mana[j]`。每瓶药**必须在巫师之间无间隔地传递**（上一个巫师一做完，下一个必须立刻接手），
每个巫师按 `j = 0, 1, …` 的顺序处理。求最后一瓶药做完的最早时刻。

### 关键约束：每瓶药的「台阶」形状是固定的，只能整体平移

记 `pre[i] = skill[0] + … + skill[i-1]`（前缀和，`pre[0] = 0`）。
若第 `j` 瓶药在巫师 0 手上的开始时刻是 `s_j`，那么因为**不允许等待**：

```
巫师 i 开始处理第 j 瓶:  s_j + mana[j] * pre[i]
巫师 i 处理完第 j 瓶  :  s_j + mana[j] * pre[i+1]
```

⟹ 一整瓶药在时间轴上是一条**形状固定的台阶**（由 `mana[j]` 整体缩放），
**唯一的自由变量就是 `s_j`** —— 整条台阶只能左右平移。
这就是全题的突破口：`m` 个未知数，每个只有一维自由度。

### 递推：把台阶往右推到「刚好不撞上上一瓶」

巫师 `i` 必须先做完第 `j-1` 瓶才能接第 `j` 瓶：

```
s_j + mana[j] * pre[i]  >=  finish_{j-1}[i]        （对每个 i 都要成立）
⟹  s_j >= finish_{j-1}[i] − mana[j] * pre[i]
⟹  s_j = max_i ( finish_{j-1}[i] − mana[j] * pre[i] )      ← 取等号：越早越好
```

然后 `finish_j[i] = s_j + mana[j] * pre[i+1]`。

原有代码（`Solution`）里的 `push` 就是这个 `s_j`（它叫「量撞深」——
把上一瓶的右端和这一瓶的左端逐级相减，取最深的那一处），
`last_finish[i]` 就是 `finish_j[i]`。答案是 `finish_{m-1}[n-1]`。

**为什么取等号安全？** `s_j` 越大，所有约束都更松（不等式右边不变、左边变大），
所以可行集是一条射线 `[s_min, ∞)`；而目标是最小化最后的完成时刻，
它关于每个 `s_j` 单调不减 ⟹ 每一瓶都取各自的 `s_min` 一定最优。这也是 `Solution_2`
可以**二分**求 `s_j` 的理由（可行性关于 `s` 单调）。

### 和 LC-1701 的关系（为什么这两题编在同一层）

| | LC-1701 | LC-3494 本题 |
|---|---|---|
| 资源 | **1** 个厨师 | **n** 个巫师，串成流水线 |
| 一个任务占的形状 | 一段区间 `[s, s+d]` | 一条 n 级台阶，级长 `skill[i]·mana[j]` |
| 递推 | `free = max(free, arrival) + d` | `s_j = max_i(finish_{j-1}[i] − mana[j]·pre[i])` |
| 本质 | 单资源时间线 | 多资源**同步**时间线（flow shop） |

LC-1701 是 `n = 1` 的退化情形；本题把「一段区间」换成「一串刚性连接的区间」，
`max` 从「对 1 个资源取」变成「对 n 个资源取」。**同一个模式的两级台阶。**

### 两个坑

- **不能对每瓶药单独贪心取 `s_j = finish_{j-1}[n-1]`**（即「等上一瓶全做完」）：
  那会让巫师大量空转，答案偏大。必须逐级比较，只推到「最深的那处碰撞」为止。
- **整数溢出（C++ / Java）**：`n, m <= 5000`，`skill[i], mana[j] <= 5000`。
  答案量级可达 `pre[n] · mana ≈ (5000·5000) · 5000 = 1.25·10^11` ⟹ **爆 int32**，
  必须 `long long`。Python 不受影响。

### 三种实现

| | 解法 | 时间 | 空间 |
|---|---|---|---|
| `Solution` ⭐️ | 前缀和 + 逐瓶量撞深（原有代码） | O(n·m) | O(n) |
| `Solution_2` | 按约束定义**二分** `s_j`（真值基线 A） | O(n·m·log T) | O(n) |
| `Solution_3` | 从上一瓶的 `s` 开始**线性试探** `s_j`（真值基线 B） | 很慢，只测小数据 | O(n) |
"""


##################################################################################################
##### ! Solution 1: 前缀和 + 逐瓶「量撞深」整体右推（= 下面的 class Solution，用户原有代码，未改动）
##### ! 时间复杂度: O(n·m)   空间复杂度: O(n)
##### ! 适用：本题的标准解法，也是最优复杂度（n, m <= 5000 ⟹ 2.5·10^7 次运算）。
#####         base[i] 就是 skill 的前缀和（台阶形状，与 mana 无关 ⟹ 只算一次），
#####         push = max(上一瓶右端 − 这一瓶左端) 就是推导里的 s_j
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


from typing import List


class Solution:
    def minTime(self, skill: List[int], mana: List[int]) -> int:
        n = len(skill)

        # 台阶的"形状":base[i] = 前 i 个巫师的 skill 之和(还没乘 m)
        # 这就是你原来的 start 数组去掉 m,所以只需要算一次
        base = [0] * n
        for i in range(1, n):
            base[i] = base[i - 1] + skill[i - 1]

        last_finish = [0] * n
        for m in mana:
            # 量撞深:上一瓶右端 − 我的左端(我的左端 = base[i] * m)
            push = 0
            for i in range(n):
                push = max(push, last_finish[i] - base[i] * m)
            # 整体右推:我的右端 = 左端 + 这一级长度 + push
            for i in range(n):
                last_finish[i] = base[i] * m + skill[i] * m + push

        return last_finish[-1]


# # Test case 1: Expecting 110
# s = Solution()
# skill = [1, 5, 2, 4]
# mana = [5, 1, 4, 2]
# result = s.minTime(skill, mana)
# print(result)

# # Test case 2: Expecting 5
# s = Solution()
# skill = [1, 1]
# mana = [1, 2]
# result = s.minTime(skill, mana)
# print(result)

# # # Test case 3: Expecting 33
s = Solution()
skill = [1, 10, 1]
mana = [2, 1]
result = s.minTime(skill, mana)
print(result)


##################################################################################################
##### ! Solution 2: 按约束定义二分每瓶药的起始时刻（真值基线 A）
##### ! 时间复杂度: O(n·m·log T)   空间复杂度: O(n)
##### ! 适用：**不用闭式的 max**，只用「可行性」的定义：
#####         s 可行 ⟺ 对每个巫师 i 都有 s + mana[j]·pre[i] >= finish_{j-1}[i]。
#####         可行性关于 s 单调不减 ⟹ 可以二分出最小可行 s。
#####         它用来验证 Solution 的闭式推导没写错（而不是用公式验证公式）
##################################################################################################


class Solution_2:
    def minTime(self, skill: List[int], mana: List[int]) -> int:
        n = len(skill)
        pre = [0] * (n + 1)                         # ! pre[i] = skill[0..i-1] 之和
        for i in range(n):
            pre[i + 1] = pre[i] + skill[i]

        finish = [0] * n                            # ! 上一瓶药在各巫师处的完成时刻
        answer = 0
        for m in mana:
            def feasible(s: int) -> bool:           # ! 以 s 开始这一瓶，是否撞不到上一瓶
                return all(s + m * pre[i] >= finish[i] for i in range(n))

            lo, hi = 0, max(finish) + 1             # ! hi 一定可行（晚于上一瓶全部完成）
            while lo < hi:                          # ! 求最小可行 s ⟹ 下界二分
                mid = (lo + hi) // 2
                if feasible(mid):
                    hi = mid
                else:
                    lo = mid + 1
            s = lo
            finish = [s + m * pre[i + 1] for i in range(n)]
            answer = finish[-1]
        return answer


##################################################################################################
##### ! Solution 3: 从上一瓶的起点开始逐 1 试探（真值基线 B，只用于小数据）
##### ! 时间复杂度: O(n · Σs 的搜索步数)，可能极慢   空间复杂度: O(n)
##### ! 适用：最笨但最不可能写错的版本 —— 把「最小可行 s」真的一个一个试出来。
#####         用它来验证 Solution_2 的「可行性单调」这个前提本身成立
##################################################################################################


class Solution_3:
    def minTime(self, skill: List[int], mana: List[int]) -> int:
        n = len(skill)
        pre = [0] * (n + 1)
        for i in range(n):
            pre[i + 1] = pre[i] + skill[i]

        finish = [0] * n
        answer = 0
        for m in mana:
            s = 0
            while any(s + m * pre[i] < finish[i] for i in range(n)):
                s += 1                              # ! 一格一格往右推，直到不撞
            finish = [s + m * pre[i + 1] for i in range(n)]
            answer = finish[-1]
        return answer


if __name__ == "__main__":
    import random

    IMPLS = [Solution, Solution_2, Solution_3]

    # ! 官方样例（原文件底部的三个 driver 用例，全部打开来测）
    CASES = [
        ([1, 5, 2, 4], [5, 1, 4, 2], 110),      # ! 官方样例 1
        ([1, 1], [1, 2], 5),                    # ! 官方样例 2
        ([1, 10, 1], [2, 1], 33),               # ! 原文件里打开着的第三个用例
        ([1], [1], 1),                          # ! 边界：一个巫师一瓶药
        ([3], [1, 1, 1], 9),                    # ! 边界：单巫师 ⟹ 退化成顺序累加
        ([1, 1, 1], [1], 3),                    # ! 边界：一瓶药穿过三个巫师
    ]
    for skill, mana, want in CASES:
        for cls in IMPLS:
            got = cls().minTime(skill[:], mana[:])
            assert got == want, (cls.__name__, skill, mana, got, want)

    # ! 随机对拍：三种实现（闭式 / 二分 / 线性试探）两两必须一致
    random.seed(3494)
    for _ in range(3000):
        n = random.randint(1, 5)
        m = random.randint(1, 5)
        skill = [random.randint(1, 6) for _ in range(n)]
        mana = [random.randint(1, 6) for _ in range(m)]
        want = Solution_3().minTime(skill[:], mana[:])       # ! 最笨的那个当真值
        for cls in (Solution, Solution_2):
            got = cls().minTime(skill[:], mana[:])
            assert got == want, (cls.__name__, skill, mana, got, want)

    # ! 「等上一瓶全做完再开始」这个错误贪心，必须被证伪（否则推导就没意义了）
    def naive_wrong(skill, mana):
        n = len(skill)
        pre = [0] * (n + 1)
        for i in range(n):
            pre[i + 1] = pre[i] + skill[i]
        t = 0
        for mv in mana:
            t = t + mv * pre[n]              # ! 每瓶药都等前一瓶彻底离开流水线
        return t
    assert naive_wrong([1, 5, 2, 4], [5, 1, 4, 2]) > 110, "错误贪心居然没变大？推导要重看"

    # ! 规模守卫：n = m = 300 时闭式版要能瞬间算完（O(n·m)）
    big_skill = [random.randint(1, 5000) for _ in range(300)]
    big_mana = [random.randint(1, 5000) for _ in range(300)]
    assert Solution().minTime(big_skill, big_mana) == Solution_2().minTime(big_skill, big_mana)

    print("闭式 / 二分 / 线性试探三种实现：6 组定点 + 3000 组随机对拍 + 规模守卫全部一致 ✓")
    print("minTime([1,5,2,4], [5,1,4,2]) =", Solution().minTime([1, 5, 2, 4], [5, 1, 4, 2]))
    print("minTime([1,1], [1,2])         =", Solution().minTime([1, 1], [1, 2]))
    print("错误贪心（等上一瓶全做完）     =", naive_wrong([1, 5, 2, 4], [5, 1, 4, 2]), "> 110 ⟹ 偏大")
