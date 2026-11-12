import math

class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        n = len(s)
        B = int(math.isqrt(n)) + 2  # 枚举0的个数到 sqrt(n) 级别即可

        # next0[i] = 从i开始往右第一个'0'的位置；没有则为n
        next0 = [n] * (n + 2)
        for i in range(n - 1, -1, -1):
            next0[i] = i if s[i] == '0' else next0[i + 1]

        ans = 0

        for i in range(n):
            first0 = next0[i]

            # k = 0：子串里没有0 => 永远满足 one >= 0
            # 右端点可以到 first0-1
            ans += first0 - i

            # k >= 1：枚举子串里0的个数
            pos = first0  # 第1个0
            for k in range(1, B + 1):
                if pos == n:  # 不足k个0了
                    break

                pos_next = next0[pos + 1]  # 第k+1个0
                upper = pos_next if pos_next != n else n

                # 满足长度 >= k² + k 的最小右端点
                lower = i + k * k + k - 1

                start_end = max(pos, lower)
                if start_end < upper:
                    ans += upper - start_end

                pos = pos_next

        return ans
