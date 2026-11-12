"""LC-1603 - Design Parking System

Level 1 · 05 有状态 API、缓冲区与模拟 → Level 2 · 03 多对象状态与增量平均值

题目在问：三种车位（大/中/小）各有若干个，`addCar(carType)` 有空位就占一个并返回 True。
Easy，但它是 Amazon / Apple 电面的常见「暖场设计题」：考的是**用数据结构替代 if/else 分支**，以及把状态表达得干净。

### 从 if/else 到查表

    if carType == 1: big -= 1 ...   ← 三个几乎一样的分支，加一种车型就要再抄一遍
    slots[carType] -= 1             ← 一张表；carType 直接当下标

carType 是 1/2/3，所以把 `slots = [0, big, medium, small]` 多留一个 0 号位，省掉 `carType - 1` 的减法 —— 这是面试里顺手能说出来的细节。

### 追问方向（面试官会往这走）

- 「要支持 `removeCar`」→ 数组改成剩余数直接 +1；
- 「要知道**哪辆车**停在哪」→ 每种车位一个集合 / 栈存车牌；
- 「并发」→ 每种车位一把锁，或者用原子计数。
这些都不改变「按类型查表」这个骨架。
"""


##################################################################################################
##### ! Solution 1: 剩余车位数组，carType 直接当下标
##### ! 时间复杂度: addCar O(1)   空间复杂度: O(1)
##### ! 适用：面试标准答案；slots[0] 是占位，让 carType 1/2/3 不用减一
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self, big: int, medium: int, small: int):
        self.slots = [0, big, medium, small]      # ! 下标 = carType

    def addCar(self, carType: int) -> bool:
        if self.slots[carType] == 0:
            return False
        self.slots[carType] -= 1
        return True


##################################################################################################
##### ! Solution 2: if / else 三分支（反面教材：功能正确但不可扩展）
##### ! 时间复杂度: O(1)   空间复杂度: O(1)
##### ! 适用：只用来对照 —— 三段几乎相同的代码是「应该查表」的信号
##################################################################################################


class Solution_2:
    def __init__(self, big: int, medium: int, small: int):
        self.big, self.medium, self.small = big, medium, small

    def addCar(self, carType: int) -> bool:
        if carType == 1:
            if self.big == 0:
                return False
            self.big -= 1
        elif carType == 2:
            if self.medium == 0:
                return False
            self.medium -= 1
        else:
            if self.small == 0:
                return False
            self.small -= 1
        return True


##################################################################################################
##### ! Solution 3: 为追问预留的版本 —— 每种车位记录停着的车（支持 removeCar / 查询）
##### ! 时间复杂度: addCar / removeCar O(1)   空间复杂度: O(车位总数)
##### ! 适用：面试官问「怎么知道哪辆车在哪」「车要能开走」时的扩展；骨架仍是按 carType 查表
##################################################################################################


class Solution_3:
    def __init__(self, big: int, medium: int, small: int):
        self.capacity = [0, big, medium, small]
        self.parked = [set(), set(), set(), set()]   # ! parked[carType] = 停在这类车位的车牌集合
        self._auto = 0                                # ! 没给车牌时自动编号

    def addCar(self, carType: int, plate=None) -> bool:
        if len(self.parked[carType]) >= self.capacity[carType]:
            return False
        if plate is None:
            self._auto += 1; plate = f"auto-{self._auto}"
        self.parked[carType].add(plate)
        return True

    def removeCar(self, carType: int, plate) -> bool:
        if plate not in self.parked[carType]:
            return False
        self.parked[carType].remove(plate)
        return True


if __name__ == "__main__":
    for cls in (Solution_1, Solution_2, Solution_3):
        p = cls(1, 1, 0)
        out = [p.addCar(1), p.addCar(2), p.addCar(3), p.addCar(1)]
        assert out == [True, True, False, False], (cls.__name__, out)
    p = Solution_3(1, 0, 0)
    assert p.addCar(1, "AB-123") and not p.addCar(1, "CD-456")
    assert p.removeCar(1, "AB-123") and p.addCar(1, "CD-456")
    print("所有测试通过 ✓")
