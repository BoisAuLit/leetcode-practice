from collections import Counter

"""
这一题和 003 很像

"""

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""
        ct = Counter(t)
        
        match = 0
        l = 0
        cs = Counter()
        res = s + "*"
        for r, ch in enumerate(s):
            # 我们对不必要的字符不感兴趣
            if ch not in t:
                continue

            cs[ch] += 1

            if cs[ch] == ct[ch]:
                match += 1

            if match == len(ct):
                # 第一次找齐了包含 t 的 s 的子字符串，就对左边就行修剪，
                # 去掉不必要的 characters
                while True:
                    left_char = s[l]
                    if left_char in ct:
                        if cs[left_char] > ct[left_char]:
                            cs[left_char] -= 1
                        elif cs[left_char] == ct[left_char]:
                            break
                    l += 1
                if r - l + 1 < len(res):
                    res = s[l : r + 1]
        return res if len(res) < len(s) + 1 else ""


solution = Solution()
s = "aaabbbcdd"
t = "abcdd"
result = solution.minWindow(s, t)
print(result)
