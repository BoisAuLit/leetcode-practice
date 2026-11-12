"""LC-0470 - Implement Rand10() Using Rand7()

Level 1 · 03 Randomized Data Structures → Level 2 · 02 加权随机、蓄水池采样与洗牌

题目在问：只给一个均匀的 `rand7()`（返回 1..7），造一个均匀的 `rand10()`（返回 1..10）。
Follow-up 两问：① 期望调用几次 rand7？② 怎么降到最少？

### 拒绝采样（Rejection Sampling）：先造一个大的均匀分布，再「切整」

调两次 rand7 得到 7×7 = 49 个**等概率**的格子：

    idx = (rand7() - 1) * 7 + rand7()        # ! 1..49 均匀；这是「7 进制两位数」

49 不是 10 的倍数，所以只保留 1..40（40 是 ≤ 49 的最大 10 的倍数），落到 41..49 就**重来**。
保留的 40 个格子里 `(idx - 1) % 10 + 1` 把它们均匀地 10 个一组切开 ⟹ 每个结果 4/40 = 1/10。

### 为什么不能用「加法」或「取模」直接凑

- `rand7() + rand7()` 得到 2..14，是**三角分布**（7 的概率最大），不均匀。
- `rand7() % 5` 之类：7 不能被 5 整除，余数 0,1 各出现 2 次、2,3,4 各 1 次，不均匀。
均匀性只能来自**乘法组合 + 拒绝**：把两个独立均匀分布做成一个更大的均匀分布，再砍掉不能整除的尾巴。

### 期望调用次数（口述题）

每轮成功概率 p = 40/49，轮数服从几何分布，期望 49/40 轮，每轮 2 次 ⟹ **E = 2 · 49/40 ≈ 2.45 次**。
`Solution_2` 把被拒绝的 41..49 当成一个新的 rand9 回收利用，再和 rand7 组合成 63 格、保留 60 格……
期望降到约 2.19 次 —— 这就是 follow-up ② 的答案。
"""
from collections import Counter
import random


def rand7() -> int:
    return random.randint(1, 7)


##################################################################################################
##### ! Solution 1: 两次 rand7 造 49 格，保留 1..40，拒绝 41..49
##### ! 时间复杂度: 期望 O(1)（每轮成功概率 40/49；期望 2.45 次 rand7 调用）   空间复杂度: O(1)
##### ! 适用：面试标准答案。要会口述「为什么 40」和「期望调用次数 2·49/40」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def rand10(self) -> int:
        while True:
            idx = (rand7() - 1) * 7 + rand7()        # ! 1..49 均匀
            if idx <= 40:                            # ! 只留 10 的倍数那部分，其余拒绝重来
                return (idx - 1) % 10 + 1


##################################################################################################
##### ! Solution 2: 回收被拒绝的样本（Follow-up：降低期望调用次数）
##### ! 时间复杂度: 期望 ≈ 2.19 次 rand7 调用   空间复杂度: O(1)
##### ! 适用：面试官追问「能不能更少」时的答案。
#####         41..49 被拒绝时其实是一个均匀的 rand9，再乘 7 得到 63 格留 60；
#####         61..63 被拒绝时是均匀的 rand3，再乘 7 得到 21 格留 20；只有 21 这一格真正浪费
##################################################################################################


class Solution_2:
    def rand10(self) -> int:
        while True:
            a = (rand7() - 1) * 7 + rand7()          # ! 1..49
            if a <= 40:
                return (a - 1) % 10 + 1
            b = (a - 41) * 7 + rand7()               # ! a ∈ 41..49 是 rand9 → 1..63
            if b <= 60:
                return (b - 1) % 10 + 1
            c = (b - 61) * 7 + rand7()               # ! b ∈ 61..63 是 rand3 → 1..21
            if c <= 20:
                return (c - 1) % 10 + 1
            # ! c == 21：这一轮彻底浪费，重来


##################################################################################################
##### ! Solution 3: ❌ 错误写法 —— rand7() + rand7() 再取模（反面教材）
##### ! 时间复杂度: O(1)   空间复杂度: O(1)
##### ! 适用：只用于展示「加法得到三角分布，不均匀」；下面的卡方检验会把它判出来
##################################################################################################


class Solution_3:
    def rand10(self) -> int:
        return (rand7() + rand7()) % 10 + 1          # ! 2..14 不均匀 → 取模后仍不均匀


def chi_square(counts: Counter, trials: int, k: int = 10) -> float:
    e = trials / k
    return sum((counts[i] - e) ** 2 / e for i in range(1, k + 1))


if __name__ == "__main__":
    random.seed(470)
    N = 100000
    for cls in (Solution_1, Solution_2):
        cnt = Counter(cls().rand10() for _ in range(N))
        assert set(cnt) == set(range(1, 11))
        chi = chi_square(cnt, N)
        assert chi < 30, (cls.__name__, chi)         # ! 自由度 9 的卡方 99.9% 分位点 27.9
        print(f"{cls.__name__:12s} χ² = {chi:5.1f}（均匀）  频率 {[round(cnt[i] / N, 3) for i in range(1, 11)]}")

    # ! 统计 rand7 的期望调用次数，验证 2.45 vs 2.19
    calls = 0
    _orig = rand7
    def counting_rand7():
        global calls
        calls += 1
        return _orig()
    for cls, want in ((Solution_1, 2 * 49 / 40), (Solution_2, None)):
        calls = 0
        globals()["rand7"] = counting_rand7
        for _ in range(N):
            cls().rand10()
        globals()["rand7"] = _orig
        avg = calls / N
        if want:
            assert abs(avg - want) < 0.03, (avg, want)
        print(f"{cls.__name__:12s} 平均每次 rand10 调用 rand7 {avg:.3f} 次" + (f"（理论 {want:.3f}）" if want else "（回收后更少）"))

    cnt = Counter(Solution_3().rand10() for _ in range(N))
    chi = chi_square(cnt, N)
    assert chi > 1000, chi
    print(f"{'Solution_3':12s} χ² = {chi:.0f}（❌ 严重不均匀）  频率 {[round(cnt[i] / N, 3) for i in range(1, 11)]}")
    print("所有测试通过 ✓")
