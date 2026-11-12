"""LC-0273 - Integer to English Words

Level 1 · 03 整数运算与数位处理 → Level 2 · 02 字符串解析与大整数乘法

题目在问：把 0 ≤ num ≤ 2³¹−1 转成英文："1234567" → "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"。
Meta / Amazon 高频，没有算法，全是**分解结构 + 边角**。面试官看的是你能否把规则组织得不重不漏。

### 分解：每 3 位一组，组内规则相同，组间只差一个单位词

    1,234,567  →  [1] Million  [234] Thousand  [567]
    组内（0..999）：  百位 → "X Hundred"      后两位 → 查表（<20 直接查；≥20 = Tens + Ones）
    单位词：["", "Thousand", "Million", "Billion"]（2³¹ 不到万亿，4 个够）

### 四个边角（每个都是常见扣分点）

1. `num == 0` → "Zero"；但**组内的 0 不输出任何东西**（1,000,000 不是 "One Million Zero Thousand Zero"）。
2. 10..19 是不规则词，必须单独查表，不能拆成 Tens + Ones。
3. 组值为 0 时**单位词也不输出**（1,000,567 → "One Million Five Hundred Sixty Seven"，没有 "Thousand"）。
4. 空格：用列表收集词再 `" ".join`，不要手动拼空格 —— 否则末尾/中间会出现多余空格。

递归写法（`Solution_2`）把「小于 20 / 小于 100 / 小于 1000 / 更大」四种情形写成四个分支，是另一种同样清晰的组织方式。
"""


ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
        "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
UNITS = ["", "Thousand", "Million", "Billion"]


##################################################################################################
##### ! Solution 1: 每 3 位一组迭代，组内用 helper 转 0..999
##### ! 时间复杂度: O(1)（最多 4 组，每组常数工作）   空间复杂度: O(1)
##### ! 适用：面试标准答案。把 0..999 的转换独立成函数，主循环只负责切组 + 加单位词
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numberToWords(self, num: int) -> str:
        if num == 0:
            return "Zero"

        def chunk(n: int) -> list:
            """0..999 → 词列表（n == 0 时为空列表）。"""
            words = []
            if n >= 100:
                words += [ONES[n // 100], "Hundred"]
                n %= 100
            if n >= 20:
                words.append(TENS[n // 10])
                n %= 10
            if n:
                words.append(ONES[n])                 # ! 1..19 都在 ONES 里（含不规则的 10..19）
            return words

        words, unit = [], 0
        while num:
            num, group = divmod(num, 1000)
            if group:                                  # ! 组值为 0：既不输出数字也不输出单位词
                words = chunk(group) + ([UNITS[unit]] if unit else []) + words   # ! 高位组放前面
            unit += 1
        return " ".join(words)


##################################################################################################
##### ! Solution 2: 递归按量级分四种情形
##### ! 时间复杂度: O(1)   空间复杂度: O(1)（递归深度 ≤ 8）
##### ! 适用：另一种同样清晰的组织：<20 查表；<100 = Tens + rec(个位)；<1000 = rec(百位) Hundred + rec(余数)；
#####         否则找最大的单位 k 使 num >= 1000^k，= rec(num // 1000^k) UNIT + rec(余数)。
#####         每个分支都用 "rest 非零才拼" 的写法自动处理组内 0
##################################################################################################


class Solution_2:
    def numberToWords(self, num: int) -> str:
        if num == 0:
            return "Zero"

        def rec(n: int) -> str:
            if n < 20:
                return ONES[n]
            if n < 100:
                return (TENS[n // 10] + " " + rec(n % 10)).strip()
            if n < 1000:
                return (ONES[n // 100] + " Hundred " + rec(n % 100)).strip()
            for k, unit in ((9, "Billion"), (6, "Million"), (3, "Thousand")):
                if n >= 10 ** k:
                    return (rec(n // 10 ** k) + " " + unit + " " + rec(n % 10 ** k)).strip()
            raise AssertionError

        return rec(num)


##################################################################################################
##### ! Solution 3: 字符串切片版 —— 先 zfill 到 12 位，切成 4 段各 3 位
##### ! 时间复杂度: O(1)   空间复杂度: O(1)
##### ! 适用：喜欢「先把输入规整成固定格式」的人。缺点是要从字符串转回 int 判 0；
#####         好处是组的下标和单位词下标直接对齐，不需要 divmod 循环
##################################################################################################


class Solution_3:
    def numberToWords(self, num: int) -> str:
        if num == 0:
            return "Zero"
        s = str(num).zfill(12)                         # ! 固定 4 组 × 3 位
        groups = [int(s[i:i + 3]) for i in range(0, 12, 3)]
        out = []
        for g, unit in zip(groups, ["Billion", "Million", "Thousand", ""]):
            if g == 0:
                continue
            h, t, o = g // 100, (g % 100) // 10, g % 10
            words = []
            if h: words += [ONES[h], "Hundred"]
            if t >= 2:
                words.append(TENS[t])
                if o: words.append(ONES[o])
            elif t * 10 + o:
                words.append(ONES[t * 10 + o])         # ! 0..19
            if unit: words.append(unit)
            out += words
        return " ".join(out)


if __name__ == "__main__":
    import random
    cases = [
        (123, "One Hundred Twenty Three"),
        (12345, "Twelve Thousand Three Hundred Forty Five"),
        (1234567, "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"),
        (1234567891, "One Billion Two Hundred Thirty Four Million Five Hundred Sixty Seven Thousand Eight Hundred Ninety One"),
        (0, "Zero"), (10, "Ten"), (19, "Nineteen"), (20, "Twenty"), (100, "One Hundred"),
        (1000, "One Thousand"), (1000000, "One Million"), (1000010, "One Million Ten"),
        (100000000, "One Hundred Million"), (2147483647, "Two Billion One Hundred Forty Seven Million Four Hundred Eighty Three Thousand Six Hundred Forty Seven"),
        (1000567, "One Million Five Hundred Sixty Seven"),            # ! 千位组为 0 → 不输出 Thousand
    ]
    for n, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().numberToWords(n)
            assert got == want, (cls.__name__, n, got, want)
    rng = random.Random(273)
    for _ in range(20000):
        n = rng.choice([rng.randint(0, 999), rng.randint(0, 10 ** 6), rng.randint(0, 2 ** 31 - 1), rng.randint(0, 9) * 10 ** rng.randint(0, 9)])
        outs = [cls().numberToWords(n) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (n, outs)
        assert "  " not in outs[0] and outs[0] == outs[0].strip()   # ! 没有多余空格
    print("所有测试通过 ✓（样例 + 20000 随机对拍）")
