from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])

        # 约定:backtrack(r, c, i) 回答"从格子 (r, c) 开始,能不能拼出 word[i:]"
        # 越界和字符不匹配都在被调用方检查,调用方直接递归不用先判断,少写一堆边界代码
        def backtrack(r, c, i):
            # i 走到头 = word 已经全部匹配完,成功
            # 必须放在越界检查之前:最后一个字符匹配后会递归到一个可能越界的格子
            if i == len(word):
                return True
            if not (0 <= r < m and 0 <= c < n) or board[r][c] != word[i]:
                return False

            # 就地打标记表示"这个格子在当前路径上",防止同一格被重复使用。
            # 题目保证 board 只有英文字母,所以 "#" 不可能撞上真实字符
            board[r][c] = "#"

            # or 会短路:任一方向成功就不再试后面的,和"谁 True 就 return True"等价。
            # 但这里先把结果存进 found,是为了让下面的还原**无论成功失败都会执行** ——
            # 若直接 return True,成功路径就会跳过还原,把 "#" 永久留在入参 board 里。
            # (展开成四个 or 而不是 any(生成器):递归调用次数是百万级,
            #  每次新建生成器对象反而慢 70%)
            found = (backtrack(r, c + 1, i + 1) or backtrack(r, c - 1, i + 1)
                     or backtrack(r + 1, c, i + 1) or backtrack(r - 1, c, i + 1))

            # 回溯:撤销标记。此处 board[r][c] 必然等于 word[i](上面刚验证过),
            # 所以不需要额外用 ch 变量把原字符存起来
            board[r][c] = word[i]
            return found

        # 每个格子都试一次当起点
        return any(backtrack(x, y, 0) for x in range(m) for y in range(n))


s = Solution()
# fmt: off
board=[["a"]]
# fmt: on
word = "a"
result = s.exist(board, word)
print(result)
