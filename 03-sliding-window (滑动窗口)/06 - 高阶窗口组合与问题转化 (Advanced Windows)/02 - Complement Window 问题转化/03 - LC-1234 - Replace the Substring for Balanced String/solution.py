"""LC-1234 - Replace the Substring for Balanced String

Level 1 · 06 高阶窗口组合与问题转化 → Level 2 · 02 Complement Window 问题转化

题目在问：字符串只含 Q W E R，长度 n 是 4 的倍数。可以把**一个子串**替换成任意字符串，使四种字母各出现 n/4 次。求最短子串长度。

### 转化：看窗口**外面**而不是窗口里面

被替换的子串可以变成任何东西，所以它能「补」任何缺口。
真正的约束在窗口**外面**：外面每种字母的个数都必须 **≤ n/4**（否则再怎么替换窗口都压不下去）。

    窗口 [l, r] 合法  ⟺  对每个字母 c：total[c] − window[c] <= n/4

于是题目变成「**最短**的窗口，使补集满足条件」—— 和 LC-1658（取两端使和为 x ⟺ 中间窗口和为 total − x）同一个「补集窗口」技巧。

### 模板：最短合法窗口（LC-0076 式）

    for r: 把 s[r] 加进窗口（outside[c] -= 1）
           while 窗口合法 且 l <= r:  best = min(best, r − l + 1); 把 s[l] 移出（outside[c] += 1）; l += 1

「合法就收缩」—— 最短窗口模板的标志（最长模板是「不合法才收缩」）。
注意 `l <= r` 不是必须的：窗口空时合法等价于整个字符串本身平衡，答案 0；用 `l <= r` 让空窗口也能被检查到，顺带处理答案 0。
"""


##################################################################################################
##### ! Solution 1: 补集窗口 + 最短合法窗口模板
##### ! 时间复杂度: O(n)（每步检查 4 个字母）   空间复杂度: O(1)
##### ! 适用：面试标准答案。outside 数组维护窗口外的计数；合法 = 四个都 <= n/4
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def balancedString(self, s: str) -> int:
        n = len(s); quota = n // 4
        outside = {c: s.count(c) for c in "QWER"}       # ! 初始窗口为空：全部在外面
        if all(v <= quota for v in outside.values()):
            return 0                                    # ! 已经平衡
        best, l = n, 0
        for r, ch in enumerate(s):
            outside[ch] -= 1                            # ! s[r] 进入窗口
            while l <= r and all(v <= quota for v in outside.values()):   # ! 合法就收缩
                best = min(best, r - l + 1)
                outside[s[l]] += 1; l += 1
        return best


##################################################################################################
##### ! Solution 2: 只盯着「超额」的字母 —— 把判定压成一个数
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：优化版：先算每种字母的超额 need[c] = max(0, total[c] − n/4)；窗口必须覆盖每种字母至少 need[c] 个。
#####         这就变成了 LC-0076 Minimum Window Substring（覆盖目标计数）—— 用「还差几种字母达标」的计数器 missing 判定 O(1)
##################################################################################################


class Solution_2:
    def balancedString(self, s: str) -> int:
        n = len(s); quota = n // 4
        need = {c: max(0, s.count(c) - quota) for c in "QWER"}   # ! 窗口里至少要有这么多
        missing = sum(1 for v in need.values() if v > 0)         # ! 还有几种字母没达标
        if missing == 0:
            return 0
        have = {c: 0 for c in "QWER"}
        best, l = n, 0
        for r, ch in enumerate(s):
            have[ch] += 1
            if have[ch] == need[ch]:                    # ! 刚好达标（need 为 0 的字母永远不会从 0 到 0 触发，因为 have 先到 1）
                missing -= 1
            while missing == 0:                         # ! 全部达标 → 记录并收缩
                best = min(best, r - l + 1)
                lc = s[l]
                if have[lc] == need[lc]:
                    missing += 1                        # ! 移出后这种字母将不达标
                have[lc] -= 1; l += 1
        return best


##################################################################################################
##### ! Solution 3: 暴力 O(n²)（真值基线）
##### ! 时间复杂度: O(n² · 4)   空间复杂度: O(1)
##### ! 适用：只用来对拍。枚举所有子串，检查「外面每种 <= n/4」
##################################################################################################


class Solution_3:
    def balancedString(self, s: str) -> int:
        n = len(s); quota = n // 4
        total = {c: s.count(c) for c in "QWER"}
        best = n
        for i in range(n):
            win = {c: 0 for c in "QWER"}
            if all(total[c] <= quota for c in "QWER"):
                return 0
            for j in range(i, n):
                win[s[j]] += 1
                if all(total[c] - win[c] <= quota for c in "QWER"):
                    best = min(best, j - i + 1); break
        return best


if __name__ == "__main__":
    import random
    cases = [("QWER", 0), ("QQWE", 1), ("QQQW", 2), ("QQQQ", 3), ("WQWRQQQW", 3)]
    for s, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().balancedString(s)
            assert got == want, (cls.__name__, s, got, want)
    rng = random.Random(1234)
    for _ in range(3000):
        n = 4 * rng.randint(1, 5)
        s = "".join(rng.choice("QWER") for _ in range(n))
        outs = [cls().balancedString(s) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (s, outs)
    print("所有测试通过 ✓")
