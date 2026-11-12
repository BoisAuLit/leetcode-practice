"""LC-0408 - Valid Word Abbreviation

Level 1 · 05 多序列同步扫描 → Level 2 · 06 分段解析与对齐比较

题目在问：`abbr` 是否是 `word` 的合法缩写 —— 缩写里的数字 k 表示「跳过 k 个字母」，
数字**不能有前导零**、**不能是 0**、**相邻两个数字不能挨着**（"i12iz4n" 不合法，因为 "12" 会被解读成一个数，但题面保证不会出现 "1" "2" 相邻的歧义写法 —— 实际判定靠「数字段开头不能是 '0'」）。
Meta 电面前 15 分钟的热身题，考的是**双指针逐段对齐 + 边角**，不是算法。

### 双指针：i 走 word，j 走 abbr

    abbr[j] 是字母  →  必须 word[i] == abbr[j]，两边同时 +1
    abbr[j] 是数字  →  读出整个数 k（开头是 '0' 直接 False），i += k
    结束时 i == len(word) 且 j == len(abbr) 才合法（任何一边提前跑完或越界都 False）

### 四个边角

1. 前导零：`abbr = "a01"` 不合法（"01" 开头是 0）；`"a0b"` 同样不合法（0 本身也以 '0' 开头）。
2. 跳过数量超过剩余字母：`word = "ab", abbr = "a3"` → i 越界 → False。
3. abbr 结尾是数字：循环结束后要检查 i 是否**恰好**等于 len(word)。
4. 两边都空：`"" / ""` → True（题目保证非空，但代码天然处理）。
"""


##################################################################################################
##### ! Solution 1: 双指针逐段对齐
##### ! 时间复杂度: O(n + m)   空间复杂度: O(1)
##### ! 适用：面试标准答案。数字段用内层 while 一次读完；前导零在读到第一位时就判
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        i = j = 0
        n, m = len(word), len(abbr)
        while i < n and j < m:
            if abbr[j].isdigit():
                if abbr[j] == "0":                     # ! 前导零 / 数字 0 都不合法
                    return False
                k = 0
                while j < m and abbr[j].isdigit():     # ! 读出整个数
                    k = k * 10 + int(abbr[j]); j += 1
                i += k                                 # ! 跳过 k 个字母（可能越界，循环条件兜底）
            else:
                if word[i] != abbr[j]:
                    return False
                i += 1; j += 1
        return i == n and j == m                       # ! 两边必须同时恰好走完


##################################################################################################
##### ! Solution 2: 正则切段 —— 把 abbr 切成 [字母串 | 数字串] 交替的 token，再按 token 对齐
##### ! 时间复杂度: O(n + m)   空间复杂度: O(m)
##### ! 适用：想把「解析」和「比较」分成两步时更好读；也更容易扩展（例如允许通配符）
##################################################################################################


class Solution_2:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        import re
        tokens = re.findall(r"[a-z]+|\d+", abbr)
        if "".join(tokens) != abbr:                    # ! abbr 里有非法字符
            return False
        i = 0
        for t in tokens:
            if t.isdigit():
                if t[0] == "0":
                    return False
                i += int(t)
            else:
                if word[i:i + len(t)] != t:            # ! 切片比较：越界时切片变短，自然不等
                    return False
                i += len(t)
        return i == len(word)


##################################################################################################
##### ! Solution 3: 把 abbr 展开成正则再 fullmatch（短但「作弊」，面试里只能当备注）
##### ! 时间复杂度: O(n + m)（正则构造 + 匹配）   空间复杂度: O(m)
##### ! 适用：说明「数字 k = 任意 k 个字母」等价于正则 `.{k}`；前导零单独检查
##################################################################################################


class Solution_3:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        import re
        if re.search(r"(?<!\d)0", abbr):               # ! 某个数字段以 0 开头
            return False
        pattern = re.sub(r"\d+", lambda m: ".{%d}" % int(m.group()), abbr)
        return re.fullmatch(pattern, word) is not None


if __name__ == "__main__":
    import random, string
    cases = [
        ("internationalization", "i12iz4n", True), ("apple", "a2e", False), ("substitution", "s10n", True),
        ("substitution", "sub4u4", True), ("substitution", "12", True), ("substitution", "su3i1u2on", True),
        ("substitution", "substitution", True), ("substitution", "s55n", False), ("substitution", "s010n", False),
        ("substitution", "s0ubstitution", False), ("a", "2", False), ("ab", "a3", False), ("hi", "1", False),
        ("hi", "2", True), ("", "", True), ("a", "a0", False),
    ]
    for w, a, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().validWordAbbreviation(w, a)
            assert got == want, (cls.__name__, w, a, got, want)

    # ! 随机对拍：从 word 随机生成「合法缩写」和「扰动后的缩写」，三种实现必须一致
    rng = random.Random(408)
    def gen_abbr(word):
        out, i = [], 0
        while i < len(word):
            if rng.random() < 0.4:
                k = rng.randint(1, len(word) - i)
                out.append(str(k)); i += k
            else:
                out.append(word[i]); i += 1
        return "".join(out)
    for _ in range(5000):
        word = "".join(rng.choice("abc") for _ in range(rng.randint(1, 12)))
        abbr = gen_abbr(word)
        if rng.random() < 0.5:                         # ! 随机扰动一位
            p = rng.randrange(len(abbr))
            abbr = abbr[:p] + rng.choice("abc0123") + abbr[p + 1:]
        outs = [cls().validWordAbbreviation(word, abbr) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (word, abbr, outs)
    print("所有测试通过 ✓（样例 + 5000 随机对拍）")
