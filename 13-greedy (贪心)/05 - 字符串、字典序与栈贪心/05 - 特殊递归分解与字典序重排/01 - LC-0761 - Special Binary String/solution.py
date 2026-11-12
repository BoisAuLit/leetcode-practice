class Solution:
    def makeLargestSpecial(self, s: str) -> str:
        i = 0

        def dfs() -> str:
            nonlocal i
            res = ""
            tokens = []
            while i < len(s) and not res:
                if s[i] == "1":
                    i += 1
                    tokens.append(dfs())
                else:
                    i += 1
                    res += "1"
            prefix = bool(res)
            for token in reversed(sorted(tokens)):
                res += token
            if prefix:
                res += "0"
            return res

        return dfs()


s = Solution()
input_ = "11011000"
result = s.makeLargestSpecial(input_)
print(result)
