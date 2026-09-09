class Solution:
    def checkValidString(self, s: str) -> bool:
        lo, hi = 0, 0
        for c in s:
            if c == '(':
                lo += 1
                hi += 1
            elif c == ')':
                lo -= 1
                hi -= 1
            else:  # '*'
                lo -= 1   # 当 ')' 或空
                hi += 1   # 当 '('
            if hi < 0:        # 最乐观都救不了：右括号绝对过多
                return False
            lo = max(lo, 0)   # 下界不能为负：砍掉非法路径
        return lo == 0        # 存在一种方式让 balance 归零


s = Solution()
input_ = "((**)"
input_ = "(((*)"
input_ = "("
input_ = "(((((()*)(*)*))())())(()())())))((**)))))(()())()"
result = s.checkValidString(input_)
print(result)
