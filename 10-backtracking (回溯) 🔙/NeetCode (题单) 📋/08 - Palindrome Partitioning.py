from typing import List


"""
在字符串上不断"切一刀":只有切出来的那段是回文,才继续往后切;切到末尾就收获一个答案。
"""
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        res = []
        part = []


        def dfs(i):
            if i >= len(s):
                res.append(part.copy())
                return
            for j in range(i, len(s)):
                if self.isPali(s, i, j):
                    part.append(s[i:j+1])
                    dfs(j+1)
                    part.pop()

        dfs(0)
        return res

    def isPali(self, s, l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True
    