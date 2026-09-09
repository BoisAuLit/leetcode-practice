from collections import Counter


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        c1 = Counter(s1)
        
        c2 = Counter()
        match = 0
        l = 0

        for r, ch in enumerate(s2):
            # 当前字符根本不属于 s1
            # 它不可能出现在任何合法排列中，所以窗口重置
            if c1[ch] == 0:
                match = 0
                c2 = Counter()
                l = r + 1
                continue

            c2[ch] += 1

            # 当前字符数量太多
            if c2[ch] > c1[ch]:
                # 删除 ch 之前的字符
                while s2[l] != ch:
                    left_char = s2[l]

                    # 删除前刚好匹配，删除后就不匹配了
                    if c2[left_char] == c1[left_char]:
                        match -= 1

                    c2[left_char] -= 1
                    l += 1

                # 删除窗口中最早出现的那个 ch
                l += 1
                c2[ch] -= 1

            elif c2[ch] == c1[ch]:
                match += 1

            if match == len(c1):
                return True

        return False
