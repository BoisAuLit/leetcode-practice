# Plus One 笔记（2026-09-10）

一开始将 carry 设定成 1 是非常正确的决定。

"+1" 本身就是最低位进来的进位，所以 `carry = 1` 起步，循环里统一 `carry, digits[i] = divmod(digits[i] + carry, 10)`，不用为 +1 单独写一行。
循环结束 carry 还是 1，说明全是 9，前面补一个 1。
