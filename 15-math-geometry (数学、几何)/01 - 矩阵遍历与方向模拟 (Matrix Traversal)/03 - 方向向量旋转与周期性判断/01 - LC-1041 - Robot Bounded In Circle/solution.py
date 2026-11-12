"""LC-1041 - Robot Bounded In Circle

Level 1 · 01 矩阵遍历与方向模拟 → Level 2 · 03 方向向量旋转与周期性判断

题目在问：机器人从 `(0, 0)` 朝北，**无限重复**同一串指令（`G` 前进 / `L` 左转 / `R` 右转），
问它的轨迹是否被限制在某个有限圆内。

### 这题不是矩阵题，为什么放在「方向模拟」这一层

它用的是和 LC-0054 / LC-0885 **完全相同**的方向机制：
一个方向向量 `(dx, dy)` + 一次 90° 旋转。区别只是这里没有网格边界，
所以旋转的**代数性质**（阶为 4 的旋转群）成了全部的考点。

```python
dx, dy = -dy, dx     # ! 左转 90°（逆时针）：(0,1) → (-1,0) 北 → 西
dx, dy = dy, -dx     # ! 右转 90°（顺时针）：(0,1) → (1,0)  北 → 东
```

### 判据：只需要走**一遍**指令

走完一遍后，记净位移 `v = (x, y)`、朝向的旋转量 `R`（相对初始朝北）。则

> **有界 ⟺ `v == (0, 0)` 或 `R != I`（朝向变了）**

**情况一：`R == I`（走完一遍还是朝北）**
第 k 遍的位移和第一遍完全一样 ⟹ k 遍后在 `k·v`。
`v == 0` ⟹ 永远在原点，有界；`v != 0` ⟹ 位置线性发散，无界。

**情况二：`R != I`**，一定有界。因为 k 遍之后的总位移是

```
v + Rv + R²v + R³v + … = (I + R + R² + …) v
```

而 `R` 是 90° / 180° / 270° 旋转：

| `R` | 阶 | 为什么和为零 |
|---|---|---|
| 180° | 2 | `I + R = 0`（`Rv = -v`）⟹ **两遍**回原点 |
| 90° 或 270° | 4 | `I + R + R² + R³ = 0`（四个方向两两抵消）⟹ **四遍**回原点 |

⟹ 每 2 或 4 遍必定回到原点，轨迹是闭合回路 ⟹ 有界。∎

**这就是「为什么模拟 4 遍就够」的证明** —— 原有代码（`Solution`）走 4 遍再看是否回原点，
正确性恰好来自 `I + R + R² + R³ = 0`；而 `Solution_2` 把它压缩成了一遍 + 一个判据。

### 容易错的地方

- **`"GL"` → True**：一遍之后在 `(0, 1)` 且朝西，位移非零但朝向变了 ⟹ 有界（走 4 遍画一个正方形）。
  只看「位移是否为零」会误判成 False。
- **`"GG"` → False**：朝向没变、位移 `(0, 2)` ⟹ 每遍往北 2 格，发散。
- **纯转向 `"LLRR"` → True**：位移为零，直接有界。
- `L` / `R` 的旋转公式写反只会让「左右互换」，而题目对左右是对称的 ⟹ **测试照样全绿**。
  写的时候对着 `(0,1) → (-1,0)` 验一次，别靠测试兜底。

### 四种实现

| | 解法 | 时间 | 空间 |
|---|---|---|---|
| `Solution` | 字典存方向 + 走 4 遍（原有代码） | O(4n) | O(1) |
| `Solution_2` ⭐️ | 走一遍 + 判据 | O(n) | O(1) |
| `Solution_3` | 复数：`pos += d`，`d *= 1j` | O(n) | O(1) |
| `Solution_4` | 暴力：模拟 200 / 400 遍比最远距离（真值基线） | O(n·轮数) | O(1) |
"""


##################################################################################################
##### ! Solution 1: 字典存方向表 + 模拟 4 遍（= 下面的 class Solution，用户原有代码，未改动）
##### ! 时间复杂度: O(4n)   空间复杂度: O(1)
##### ! 适用：最不需要推导的写法 —— 直接用上面证明里的「4 遍必回原点」。
#####         directions[d] = (dx, dy, 左转后, 右转后)，把旋转写成查表，一行都不会错
##################################################################################################


from typing import List, Tuple

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    directions = {"N": (0, 1, "W", "E"), "S": (0, -1, "E", "W"), "W": (-1, 0, "S", "N"), "E": (1, 0, "N", "S")}

    def walk(self, direction: str, current_position: Tuple[int, int], instructions: List[str]):
        for step in instructions:
            if step == "G":
                x, y = Solution.directions[direction][0], Solution.directions[direction][1]
                current_position = (current_position[0] + x, current_position[1]+y)
            else:
                if step == "L":
                    direction = Solution.directions[direction][2]
                else:
                    direction = Solution.directions[direction][3]
        return direction, current_position

    def isRobotBounded(self, instructions: str) -> bool:
        direction = "N"
        current_position = (0, 0)
        for _ in range(4):
            direction, current_position = self.walk(direction, current_position, instructions)
            if current_position == (0, 0):
                return True

        return False


s = Solution()
input_ = "GGLLGG" # True
# input_ = "GG" # False
# input_ = "GL" # True

result = s.isRobotBounded(input_)
print(result)


##################################################################################################
##### ! Solution 2: 走一遍 + 判据（有界 ⟺ 位移为零 或 朝向改变）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：面试首选。把「模拟 4 遍」换成一个代数判据，
#####         省掉 4 倍常数，也把考点从「会模拟」提升到「知道旋转群的阶是 4」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def isRobotBounded(self, instructions: str) -> bool:
        x = y = 0
        dx, dy = 0, 1                       # ! 初始朝北
        for ch in instructions:
            if ch == "G":
                x += dx
                y += dy
            elif ch == "L":
                dx, dy = -dy, dx            # ! 逆时针 90°：(0,1) → (-1,0) 北 → 西
            else:
                dx, dy = dy, -dx            # ! 顺时针 90°：(0,1) → (1,0)  北 → 东
        # ! 位移为零 ⟹ 原地闭合；朝向变了 ⟹ 2 或 4 遍后旋转和为零，必定闭合
        return (x == 0 and y == 0) or (dx, dy) != (0, 1)


##################################################################################################
##### ! Solution 3: 复数视角（旋转 = 乘以 i）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：想一眼看出「旋转群的阶是 4」时 —— 因为 i⁴ == 1 本来就是这件事。
#####         代码里没有任何 (dx, dy) 的分量运算，左转就是 *= 1j
##################################################################################################


class Solution_3:
    def isRobotBounded(self, instructions: str) -> bool:
        pos = 0 + 0j
        d = 1j                              # ! 朝北 = +i
        for ch in instructions:
            if ch == "G":
                pos += d
            elif ch == "L":
                d *= 1j                     # ! 乘 i = 逆时针 90°
            else:
                d *= -1j                    # ! 乘 -i = 顺时针 90°
        return pos == 0 or d != 1j


##################################################################################################
##### ! Solution 4: 暴力真值基线 —— 模拟 200 遍和 400 遍，比最远距离是否还在长
##### ! 时间复杂度: O(n·轮数)   空间复杂度: O(1)
##### ! 适用：**不用任何结论**，只用「有界」的定义（轨迹落在有限圆内）。
#####         它是下面穷举对拍的真值来源 —— 用它来验证「4 遍判据」本身是对的，
#####         而不是用判据去验证判据
##################################################################################################


class Solution_4:
    def isRobotBounded(self, instructions: str) -> bool:
        def farthest(rounds: int) -> int:
            x = y = 0
            dx, dy = 0, 1
            best = 0
            for _ in range(rounds):
                for ch in instructions:
                    if ch == "G":
                        x += dx
                        y += dy
                    elif ch == "L":
                        dx, dy = -dy, dx
                    else:
                        dx, dy = dy, -dx
                best = max(best, abs(x) + abs(y))
            return best

        # ! 轮数翻倍后最远距离不再变大 ⟹ 轨迹有界（无界时位移按 k·v 线性增长，必然变大）
        return farthest(400) == farthest(200)


if __name__ == "__main__":
    from itertools import product

    IMPLS = [Solution, Solution_2, Solution_3]

    # ! 官方样例
    CASES = [
        ("GGLLGG", True),       # ! 官方样例 1：走出去再走回来
        ("GG", False),          # ! 官方样例 2：一路向北，发散
        ("GL", True),           # ! 官方样例 3：位移非零但朝向变了 ⟹ 4 遍画一个正方形
        ("", True),             # ! 边界：空指令，原地不动
        ("LLRR", True),         # ! 边界：只转不走，位移为零
        ("GLGLGLGL", True),     # ! 一遍就画完一个正方形，回到原点
        ("GRGRGRGR", True),     # ! 同上，反方向
        ("GGGG", False),        # ! 纯平移
        ("GLGR", False),        # ! 朝向转回北，净位移 (−1, 1) ⟹ 发散
    ]
    for ins, want in CASES:
        assert Solution_4().isRobotBounded(ins) == want, ("真值基线自己错了", ins)
        for cls in IMPLS:
            got = cls().isRobotBounded(ins)
            assert got == want, (cls.__name__, ins, got, want)

    # ! 穷举对拍：长度 0..8 的所有 {G,L,R} 串（共 9841 个），全部和暴力基线一致
    total = 0
    for length in range(0, 9):
        for tup in product("GLR", repeat=length):
            ins = "".join(tup)
            want = Solution_4().isRobotBounded(ins)
            for cls in IMPLS:
                got = cls().isRobotBounded(ins)
                assert got == want, (cls.__name__, ins, got, want)
            total += 1

    print(f"三种 O(n) 解法 vs 暴力真值基线：9 组定点 + 穷举 {total} 个指令串，全部一致 ✓")
    print('isRobotBounded("GGLLGG") =', Solution_2().isRobotBounded("GGLLGG"))
    print('isRobotBounded("GG")     =', Solution_2().isRobotBounded("GG"))
    print('isRobotBounded("GL")     =', Solution_2().isRobotBounded("GL"))
