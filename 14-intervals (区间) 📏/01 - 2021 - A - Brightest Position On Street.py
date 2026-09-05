import collections
import sys
from typing import List


class Solution:
    def brightestPosition(self, lights: List[List[int]]) -> int:
        # 1. 差分字典：key 是坐标，val 是亮度变化量
        d = collections.defaultdict(int)

        # 2. 把每一个灯的区间 [i-dis, i+dis] 转成差分
        for i, dis in lights:
            left = i - dis
            right = i + dis
            d[left] += 1  # 从 left 开始覆盖 +1
            d[right + 1] -= 1  # 从 right+1 开始不再覆盖 -1

        # 3. 扫描线：从最左到最右，把当前亮度 cur 加上变化量
        cur = 0  # 当前亮度
        max_val = -sys.maxsize  # 目前见过的最大亮度
        max_idx = -1  # 对应的最小坐标

        # sorted(d.items()) 按坐标从小到大遍历所有“事件点”
        for idx, delta in sorted(d.items()):
            cur += delta  # 应用这一点上的增减，得到当前亮度

            # 如果当前亮度超过历史最大值：
            if cur > max_val:
                max_val = cur  # 更新最大亮度
                max_idx = idx  # 记录第一次出现这个亮度的坐标

        return max_idx
