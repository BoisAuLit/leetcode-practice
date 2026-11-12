"""LC-0937 - Reorder Data in Log Files

Level 1 · 06 低优先级与跨专题题目

题目在问：每条日志 = 标识符 + 内容。内容是字母的叫「字母日志」，是数字的叫「数字日志」。
要求：字母日志排前面，**按内容字典序**，内容相同按标识符；数字日志**保持原顺序**排在后面。
Amazon 高频热身题 —— 考的是**排序键的设计**和**稳定排序**。

### 一个排序键解决全部要求

    key(log) = (0, content, identifier)   # 字母日志
             = (1,)                         # 数字日志：键相同 → 稳定排序保持原顺序

Python 的 `sorted` 是稳定的（Timsort），所以所有数字日志键都是 `(1,)` 时它们的相对顺序不变 —— 这正是题目要的。
面试里一定要说出「我依赖的是稳定排序」，Java 的 `Arrays.sort(Object[])` 也是稳定的（TimSort），C++ 要用 `stable_sort`。

### 另一条路：分两组

把字母日志和数字日志分开：字母组按 `(content, id)` 排，数字组不动，再拼接。O(n log n) 同样，但不依赖稳定性 —— 当被问「如果排序不稳定怎么办」时用它回答。

### 边角

- 标识符后面可能有多个单词；`split(" ", 1)` 只切第一刀，内容整体比较。
- 判断「字母 or 数字」只看内容的**第一个字符**（题目保证内容同质）。
"""
from typing import List


##################################################################################################
##### ! Solution 1: 单一排序键 + 稳定排序
##### ! 时间复杂度: O(n log n · L)（L 为日志长度，比较字符串）   空间复杂度: O(n)
##### ! 适用：面试标准答案，一个 key 函数搞定；要说出「依赖稳定排序」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def reorderLogFiles(self, logs: List[str]) -> List[str]:
        def key(log: str):
            ident, content = log.split(" ", 1)
            if content[0].isdigit():
                return (1,)                            # ! 所有数字日志键相同 → 稳定排序保持原顺序
            return (0, content, ident)                 # ! 字母日志：先内容再标识符
        return sorted(logs, key=key)


##################################################################################################
##### ! Solution 2: 分两组再拼接（不依赖排序稳定性）
##### ! 时间复杂度: O(n log n · L)   空间复杂度: O(n)
##### ! 适用：面试官追问「如果语言的排序不稳定」时的答案；数字组原样保留
##################################################################################################


class Solution_2:
    def reorderLogFiles(self, logs: List[str]) -> List[str]:
        letters, digits = [], []
        for log in logs:
            ident, content = log.split(" ", 1)
            (digits if content[0].isdigit() else letters).append(log)
        letters.sort(key=lambda log: tuple(reversed(log.split(" ", 1))))   # ! (content, ident)
        return letters + digits


##################################################################################################
##### ! Solution 3: 显式比较器（cmp_to_key）—— Java 风格，把规则写成 if 链
##### ! 时间复杂度: O(n log n · L)   空间复杂度: O(n)
##### ! 适用：面试用 Java/C++ 时的对应写法；Python 里用 functools.cmp_to_key。注意数字日志之间返回 0（相等）才能保序
##################################################################################################


class Solution_3:
    def reorderLogFiles(self, logs: List[str]) -> List[str]:
        from functools import cmp_to_key

        def cmp(a: str, b: str) -> int:
            ia, ca = a.split(" ", 1)
            ib, cb = b.split(" ", 1)
            da, db = ca[0].isdigit(), cb[0].isdigit()
            if da and db:
                return 0                               # ! 数字 vs 数字：相等 → 稳定排序保序
            if da != db:
                return 1 if da else -1                 # ! 字母在前
            return (ca > cb) - (ca < cb) or (ia > ib) - (ia < ib)

        return sorted(logs, key=cmp_to_key(cmp))


if __name__ == "__main__":
    import random
    cases = [
        (["dig1 8 1 5 1", "let1 art can", "dig2 3 6", "let2 own kit dig", "let3 art zero"],
         ["let1 art can", "let3 art zero", "let2 own kit dig", "dig1 8 1 5 1", "dig2 3 6"]),
        (["a1 9 2 3 1", "g1 act car", "zo4 4 7", "ab1 off key dog", "a8 act zoo"],
         ["g1 act car", "a8 act zoo", "ab1 off key dog", "a1 9 2 3 1", "zo4 4 7"]),
        (["a2 act car", "a1 act car"], ["a1 act car", "a2 act car"]),      # ! 内容相同按标识符
    ]
    for logs, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().reorderLogFiles(logs)
            assert got == want, (cls.__name__, got, want)
    rng = random.Random(937)
    words = ["act", "car", "zoo", "off", "key"]
    for _ in range(2000):
        logs = []
        for i in range(rng.randint(1, 12)):
            ident = rng.choice(["a", "b", "z"]) + str(rng.randint(1, 3))
            content = " ".join(rng.choice(words) for _ in range(rng.randint(1, 3))) if rng.random() < 0.5 else " ".join(str(rng.randint(0, 9)) for _ in range(rng.randint(1, 3)))
            logs.append(ident + " " + content)
        outs = [cls().reorderLogFiles(logs) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (logs, outs)
    print("所有测试通过 ✓")
