"""LC-0735 - Asteroid Collision

Level 1 · 01 基础栈、括号与消除 —— Stack Simulation（栈模拟）+ 连锁碰撞
题目在问：正数向右飞、负数向左飞，同向永不相撞，相遇时小的爆炸、同样大两个都炸，求最终状态。

决定性观察：
  1. **只有「栈顶是正数（向右）」且「当前是负数（向左）」才会相撞**，其他三种组合都安全：
         右右 → 同向，追不上
         左左 → 同向
         左右 → 背离，越飞越远
     这一条判断写错，整道题就错了。
  2. 一颗向左飞的陨石可能**连续撞掉好几颗**向右的 —— 所以是 `while` 不是 `if`。
  3. 栈里存的是「已经稳定下来、不会再被右侧影响」的陨石序列。

碰撞的三种结局（必须全部覆盖）：
     |栈顶| < |当前|  → 栈顶爆炸，继续和新的栈顶比（循环）
     |栈顶| == |当前| → 两个都爆炸，当前陨石消失，停止
     |栈顶| > |当前|  → 当前陨石爆炸，停止

实现技巧：用一个 `alive` 标志表示「当前陨石还活着吗」，循环结束后才决定要不要入栈。
      直接在 while 里 break/else 很容易漏掉「同归于尽」那一支。

Loop Invariant：栈从栈底到栈顶是「若干个向左的（已经撞无可撞）+ 若干个向右的」，
      向右的那一段才是后续可能被撞的部分。

复杂度：O(n) 时间（每颗陨石最多入栈一次、出栈一次），O(n) 空间。

边界：
  - [5,10,-5]   → [5,10]（-5 撞不过 10）
  - [8,-8]      → []（同归于尽）
  - [10,2,-5]   → [10]（-5 先撞掉 2，再被 10 撞掉）
  - [-2,-1,1,2] → [-2,-1,1,2]（全部背离，一次都不撞）
  - [1,-2,-2,-2]→ [-2,-2,-2]
"""

from typing import List


##################################################################################################
##### ! Solution 1: 栈模拟 + alive 标志处理连锁碰撞
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：一切「相邻元素按规则相互抵消 / 吞并」的模拟题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack: List[int] = []
        for a in asteroids:
            alive = True
            # ! 唯一会相撞的组合：栈顶向右(>0) 且 当前向左(<0)
            while alive and a < 0 and stack and stack[-1] > 0:
                if stack[-1] < -a:
                    stack.pop()          # ! 栈顶更小 → 栈顶炸，当前继续往左撞
                elif stack[-1] == -a:
                    stack.pop()          # ! 一样大 → 两个都炸
                    alive = False
                else:
                    alive = False        # ! 栈顶更大 → 当前炸
            if alive:
                stack.append(a)
        return stack


##################################################################################################
##### ! Solution 2: 同样的栈模拟，但用 for-else 的写法（少一个标志变量）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：喜欢紧凑写法时；逻辑和 Solution_1 完全一致，只是控制流不同
##################################################################################################


class Solution_2:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack: List[int] = []
        for a in asteroids:
            while stack and a < 0 < stack[-1]:
                if stack[-1] + a < 0:    # ! |栈顶| < |a| → 栈顶炸掉，继续比
                    stack.pop()
                    continue
                if stack[-1] + a == 0:   # ! 同归于尽
                    stack.pop()
                break                    # ! 不管是「当前炸」还是「同归于尽」，当前都不入栈
            else:
                stack.append(a)          # ! while 没有 break 才执行：一路活到最后
        return stack


##################################################################################################
##### ! Solution 3: 反复扫描直到稳定（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：正确性参照；也最接近题目字面描述
##################################################################################################


class Solution_3:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        cur = list(asteroids)
        changed = True
        while changed:
            changed = False
            for i in range(len(cur) - 1):
                if cur[i] > 0 > cur[i + 1]:          # ! 相邻的一对正在相撞
                    if cur[i] < -cur[i + 1]:
                        cur = cur[:i] + cur[i + 1:]
                    elif cur[i] > -cur[i + 1]:
                        cur = cur[:i + 1] + cur[i + 2:]
                    else:
                        cur = cur[:i] + cur[i + 2:]
                    changed = True
                    break
        return cur


if __name__ == "__main__":
    import random

    cases = [[5, 10, -5], [8, -8], [10, 2, -5], [-2, -1, 1, 2], [1, -2, -2, -2], [-2, 2], [1]]
    for a in cases:
        r = Solution_1().asteroidCollision(a)
        assert r == Solution_2().asteroidCollision(a) == Solution_3().asteroidCollision(a), a
        print(f"{a} -> {r}")

    for _ in range(500):                 # ! 随机对拍，小值域专打「同归于尽」
        a = [random.choice([-3, -2, -1, 1, 2, 3]) for _ in range(random.randint(0, 9))]
        assert (Solution_1().asteroidCollision(a)
                == Solution_2().asteroidCollision(a)
                == Solution_3().asteroidCollision(a)), a
    print("随机对拍 500 组通过 ✓")
