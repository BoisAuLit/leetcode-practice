# 前缀和 / 差分 — 高频清单（盲区补齐）

> 你的文件夹是空的，相关题散在根目录。系统化它。
> 核心信号：**"子数组的和 = 某值"、"区间和查询"、"连续子数组满足某条件"、"区间批量加减"**

## 核心模式（一句话）
- 前缀和：`prefix[i] = nums[0]+...+nums[i-1]`，则 `子数组和(i,j) = prefix[j+1] - prefix[i]`。
- **前缀和 + 哈希表**是王炸组合：把"找子数组和 = k"变成"找 prefix[j] - k 是否出现过"，O(N) 解决。
- 差分数组：区间批量 +x，只在两端打标记，最后求前缀和还原——把 O(N) 区间更新降到 O(1)。

## 必做（按优先级）
- [ ] 0303 - Range Sum Query - Immutable（一维前缀和模板）
- [ ] 0304 - Range Sum Query 2D - Immutable ⭐️（二维前缀和，必会）
- [ ] 0525 - Contiguous Array（前缀和 + 哈希，0/1 转 -1/+1 的经典技巧）
- [ ] 0974 - Subarray Sums Divisible by K（前缀和 + 余数哈希）
- [ ] 0523 - Continuous Subarray Sum（前缀和 + 余数）
- [ ] 1248 - Count Number of Nice Subarrays（前缀和思想 / 滑窗）
- [ ] **1109 - Corporate Flight Bookings** ⭐️（差分数组模板题，必会）
- [ ] 1094 - Car Pooling（差分数组应用）
- [ ] 0370 - Range Addition（差分数组最纯粹的形式）

## 复习（你已做过）
- [ ] 0560 - Subarray Sum Equals K ⭐️⭐️⭐️（前缀和+哈希的代表作，必须闭卷秒写，根目录）
- [ ] 0238 - Product of Array Except Self（前缀积/后缀积，根目录）
- [ ] 0724 - Find Pivot Index（前缀和入门，根目录）
