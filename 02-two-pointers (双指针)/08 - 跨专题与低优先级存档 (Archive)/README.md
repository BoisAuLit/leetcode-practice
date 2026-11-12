# 08 - 跨专题与低优先级存档 (Archive)

**这不是必刷目录。** 这里的题要么主算法不是双指针，要么迁移性低，
放在这里是为了保留已有的学习成果，同时不让它们占据主线。

## 目录内容

| | 题 | 难度 | 这一题新增的东西 |
|---|---|---|---|
| **P2** | [LC-0170 - Two Sum III - Data structure design](01%20-%20Hash%20Map%20%E4%B8%8E%E8%AE%BE%E8%AE%A1%E7%B1%BB%E4%BA%A4%E5%8F%89%E9%A2%98/01%20-%20LC-0170%20-%20Two%20Sum%20III%20-%20Data%20structure%20design) | E | 设计题：插入 / 查询的复杂度权衡 |
| **P2** | [LC-1695 - Maximum Erasure Value](02%20-%20Sliding%20Window%20%E4%BA%A4%E5%8F%89%E9%A2%98/01%20-%20LC-1695%20-%20Maximum%20Erasure%20Value) | M | 滑动窗口 + 哈希集合，不是对撞指针 |

## 两条跨专题说明

- **LC-0001 Two Sum**（P0）已按主算法归属迁到
  [01-arrays-hashing/01 - Hash Set 与 Hash Map 基础/01 - LC-0001 - Two Sum](../../01-arrays-hashing%20%28%E6%95%B0%E7%BB%84%E3%80%81%E5%93%88%E5%B8%8C%E8%A1%A8%29/01%20-%20Hash%20Set%20%E4%B8%8E%20Hash%20Map%20%E5%9F%BA%E7%A1%80/01%20-%20LC-0001%20-%20Two%20Sum)。
  输入无序 ⇒ 最优解是哈希表；排序再对撞是 O(n log n) 且会打乱要返回的下标。
  详见 [01 - Hash Map 与设计类交叉题/README.md](01%20-%20Hash%20Map%20%E4%B8%8E%E8%AE%BE%E8%AE%A1%E7%B1%BB%E4%BA%A4%E5%8F%89%E9%A2%98/README.md)。
- **LC-1695** 的核心是「窗口内元素互不相同」这个约束驱动的滑动窗口，对比见根
  [README.md](../README.md) 的「Two Pointers vs Sliding Window」。
  滑动窗口专题在 [03-sliding-window](../../03-sliding-window%20%28%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%29)。

## 什么时候回来看这里

准备到 P0 + P1 全部过关、开始刷公司题库之后。在那之前这两道题不值得花时间。
