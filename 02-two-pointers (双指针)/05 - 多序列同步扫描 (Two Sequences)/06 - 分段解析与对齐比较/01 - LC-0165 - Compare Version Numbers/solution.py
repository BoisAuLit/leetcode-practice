"""LC-0165 - Compare Version Numbers

Level 1 · 05 多序列同步扫描 —— 分段解析 + 缺位补零对齐
题目在问：比较两个形如 `"1.01.2"` 的版本号。前导零无意义，缺失的段按 0 算。
      version1 > version2 返回 1，小于返回 -1，相等返回 0

决定性观察：
  1. 比较的单位不是**字符**而是**段（revision）**，而且要按**整数**比较，
     所以 `"1.01"` 和 `"1.001"` 相等 —— 字符串比较在这里是错的。
  2. 长度不同不需要特殊分支：**短的那一边后面全当 0**。
     `"1.0"` == `"1"`，`"1.0.1"` > `"1"`。这一条把所有边界情况一次性消掉。

循环不变量：两个指针各自停在「下一段的第一个字符」上。
  每轮各自吃掉一整段（到 '.' 或串尾为止），把两段作为整数比较；
  一侧耗尽后它每轮产出 0。循环在两侧都耗尽时结束。

为什么值得单独练：它和同层另外几题的指针推进规则都不同 ——
  - 392 子序列：只有匹配成功才推进其中一个指针
  - 844 退格：倒着扫，用计数器决定跳过
  - 1768 交替归并：严格轮流推进
  - 165 本题：**各自吃掉一整段再比较**，是"分段对齐"这一类的代表（IP 地址、时间串同理）

坑：
  - 不能用字符串直接比大小（`"10" < "9"` 字典序成立但数值不成立）
  - 前导零：转成 int 自动解决，自己手写解析时要注意
  - 长度不同的边界：补 0 而不是直接判长度；写成「长的那个更大」会在 `"1.0"` vs `"1"` 上错
"""


##################################################################################################
##### ! Solution 1: 双指针原地解析，缺位补 0
##### ! 时间复杂度: O(n + m)   空间复杂度: O(1)
##### ! 适用：不切分、不建列表，分段解析类题目的通用骨架（IP、时间、版本号）
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def compareVersion(self, version1: str, version2: str) -> int:
        i, j = 0, 0
        n, m = len(version1), len(version2)
        while i < n or j < m:                 # ! 任一侧还有内容就继续，耗尽的一侧产出 0
            a = 0
            while i < n and version1[i] != ".":
                a = a * 10 + int(version1[i]) # ! 边扫边累加，前导零自然被吃掉
                i += 1
            b = 0
            while j < m and version2[j] != ".":
                b = b * 10 + int(version2[j])
                j += 1
            if a != b:
                return 1 if a > b else -1
            i += 1                            # ! 跳过 '.'（越界也无所谓，下一轮的 while 会拦住）
            j += 1
        return 0


##################################################################################################
##### ! Solution 2: split + int + 补零对齐
##### ! 时间复杂度: O(n + m)   空间复杂度: O(n + m)
##### ! 适用：Python 里最好写的版本；面试先给它，再说"不想建列表就用双指针原地解析"
##################################################################################################


class Solution_2:
    def compareVersion(self, version1: str, version2: str) -> int:
        a = [int(x) for x in version1.split(".")]
        b = [int(x) for x in version2.split(".")]
        for i in range(max(len(a), len(b))):
            x = a[i] if i < len(a) else 0     # ! 缺位补 0，这是全部的边界处理
            y = b[i] if i < len(b) else 0
            if x != y:
                return 1 if x > y else -1
        return 0


if __name__ == "__main__":
    import random
    cases = [("1.2", "1.10", -1), ("1.01", "1.001", 0), ("1.0", "1.0.0", 0),
             ("0.1", "1.1", -1), ("1.0.1", "1", 1), ("7.5.2.4", "7.5.3", -1),
             ("1", "1", 0), ("1.0.0.0.0.1", "1", 1), ("100", "99.99.99", 1)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for v1, v2, want in cases:
            got = sol.compareVersion(v1, v2)
            assert got == want, f"{type(sol).__name__} {v1!r} vs {v2!r}: got {got}, want {want}"
    rng = random.Random(165)
    def gen():
        return ".".join(str(rng.choice([0, 1, 9, 10, 100, 0o7])).zfill(rng.randint(1, 3))
                        for _ in range(rng.randint(1, 4)))
    for _ in range(5000):
        v1, v2 = gen(), gen()
        want = Solution_2().compareVersion(v1, v2)
        assert Solution_1().compareVersion(v1, v2) == want, (v1, v2, want)
    print("2 个解法全过（含 5000 组随机对拍，覆盖前导零和长度不等）")
