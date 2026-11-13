# Arrays & Hashing 学习体系（43 题）

为 Silicon Valley SWE / AI Engineer 的算法面试与 OA 准备。文件夹编号是**学习优先级**，不是题号。

| 标签 | 含义 |
|---|---|
| **P0** | 核心必练，要能闭卷默写 |
| **P1** | 重要补充，要能讲清思路和复杂度 |
| **P2** | 低优先级 / 跨专题，资料保留，现阶段不投入同等精力 |

## 一句话抓住这一类

这 47 道题不是 47 个算法，只有**四个核心观察**：

1. **查找要快就换空间** —— Set 问存在、Map 问「对应的那个东西」。（Level 01）
2. **数量比数值重要** —— 计数表是一种压缩；桶排序和投票法都是在计数之上再省一层。（Level 02）
3. **区间问题先看两端** —— 任何「区间 f」只要能写成 `g(右端) ⊖ g(左端)`，就能用前缀状态 O(1) 回答。（Level 03）
4. **值域就是下标就不需要额外空间** —— 值落在 1..n 时，数组本身可以当哈希表用。（Level 04）

Level 05 是两道基础字符串操作，Level 06 是保留资料。

## 01 - Hash Set 与 Hash Map 基础（9 题）

| | 题 | 难度 | Core Pattern | 为什么学它 / 和前面的区别 | 复杂度 |
|---|---|---|---|---|---|
| **P0** | [LC-0001 - Two Sum](01%20-%20Hash%20Set%20%E4%B8%8E%20Hash%20Map%20%E5%9F%BA%E7%A1%80/01%20-%20LC-0001%20-%20Two%20Sum) | E | Complement Lookup（查补数） | 哈希表换空间省时间的原型：边扫边把见过的数存起来，查 `target - x`。整个 Level 01 都是它的变形 | O(n) / O(n) |
| **P0** | [LC-0217 - Contains Duplicate](01%20-%20Hash%20Set%20%E4%B8%8E%20Hash%20Map%20%E5%9F%BA%E7%A1%80/02%20-%20LC-0217%20-%20Contains%20Duplicate) | E | Hash Set Membership（存在性） | 只问「有没有重复」，连下标都不用 → Set 就够。学会区分「要不要下标」决定用 Set 还是 Map | O(n) / O(n) |
| **P0** | [LC-0242 - Valid Anagram](01%20-%20Hash%20Set%20%E4%B8%8E%20Hash%20Map%20%E5%9F%BA%E7%A1%80/03%20-%20LC-0242%20-%20Valid%20Anagram) | E | Character Frequency（字符计数） | 从「存在性」升级到「数量相等」。26 个字母的计数数组就是定长哈希表，空间算 O(1) | O(n) / O(1) |
| **P0** | [LC-0049 - Group Anagrams](01%20-%20Hash%20Set%20%E4%B8%8E%20Hash%20Map%20%E5%9F%BA%E7%A1%80/04%20-%20LC-0049%20-%20Group%20Anagrams) 📦 | M | Canonical Key + Grouping（规范键分组） | 第一次出现「键要自己设计」：排序后的字符串或 26 长度计数元组，都能让同组落进同一个桶 | O(nk) / O(nk) |
| **P0** | [LC-0128 - Longest Consecutive Sequence](01%20-%20Hash%20Set%20%E4%B8%8E%20Hash%20Map%20%E5%9F%BA%E7%A1%80/05%20-%20LC-0128%20-%20Longest%20Consecutive%20Sequence) 📦 | M | Hash Set + Sequence Start（只从序列头起跳） | 反直觉的 O(n)：只在 `x-1 不在集合里` 时才往上数，保证每个元素最多被走一次。不是排序题 | O(n) / O(n) |
| **P0** | [LC-0036 - Valid Sudoku](01%20-%20Hash%20Set%20%E4%B8%8E%20Hash%20Map%20%E5%9F%BA%E7%A1%80/06%20-%20LC-0036%20-%20Valid%20Sudoku) 📦 | M | 多约束集合并行维护 | 一次遍历同时喂三组 Set（行、列、3x3 宫）。练的是「一个循环维护多个不变量」 | O(1)（固定 81 格） |
| **P1** | [LC-0205 - Isomorphic Strings](01%20-%20Hash%20Set%20%E4%B8%8E%20Hash%20Map%20%E5%9F%BA%E7%A1%80/07%20-%20LC-0205%20-%20Isomorphic%20Strings) | E | Bijection（双向映射） | 和 0049 的区别：那题要把多个键归并到一组，这题要保证**一一对应**，所以必须两张表互查 | O(n) / O(1) |
| **P1** | [LC-0380 - Insert Delete GetRandom O(1)](01%20-%20Hash%20Set%20%E4%B8%8E%20Hash%20Map%20%E5%9F%BA%E7%A1%80/08%20-%20LC-0380%20-%20Insert%20Delete%20GetRandom%20O%281%29) | M | Hash Map + Dynamic Array（设计题） | 唯一一道设计题。数组负责 O(1) 随机、哈希表负责 O(1) 定位，删除靠「和末尾交换」 | 三个操作均摊 O(1) / O(n) |
| **P1** | [LC-0454 - 4Sum II](01%20-%20Hash%20Set%20%E4%B8%8E%20Hash%20Map%20%E5%9F%BA%E7%A1%80/09%20-%20LC-0454%20-%204Sum%20II) | M | Meet in the Middle（折半配对） | Two Sum 的升级：把「一个数」换成「一对数」，O(n⁴) 压到 O(n²)。和 3Sum/4Sum 完全不同（那两题要去重+双指针） | O(n²) / O(n²) |

## 02 - Frequency Counting 与 Top K（7 题）

| | 题 | 难度 | Core Pattern | 为什么学它 / 和前面的区别 | 复杂度 |
|---|---|---|---|---|---|
| **P0** | [LC-0347 - Top K Frequent Elements](02%20-%20Frequency%20Counting%20%E4%B8%8E%20Top%20K/01%20-%20LC-0347%20-%20Top%20K%20Frequent%20Elements) 📦 | M | Frequency Map + Bucket Sort | 本层的签名题。桶排序把「按频率排序」做到 O(n)；堆是 O(n log k) 的替代，Quickselect 不必记 | O(n) / O(n) |
| **P0** | [LC-0169 - Majority Element](02%20-%20Frequency%20Counting%20%E4%B8%8E%20Top%20K/02%20-%20LC-0169%20-%20Majority%20Element) | E | Boyer-Moore Majority Vote | **不是哈希题**。「候选+计数」的对消法把空间压到 O(1)，是这一层唯一不靠计数表的解法 | O(n) / O(1) |
| **P1** | [LC-0387 - First Unique Character in a String](02%20-%20Frequency%20Counting%20%E4%B8%8E%20Top%20K/03%20-%20LC-0387%20-%20First%20Unique%20Character%20in%20a%20String) | E | 频率统计 + 顺序扫描 | 两遍扫描的典型：第一遍统计、第二遍按原顺序找。和 0169 的区别是它必须保留位置信息 | O(n) / O(1) |
| **P1** | [LC-0383 - Ransom Note](02%20-%20Frequency%20Counting%20%E4%B8%8E%20Top%20K/04%20-%20LC-0383%20-%20Ransom%20Note) | E | Multiset Containment（多重集包含） | 计数表相减，所有「A 能不能拼出 B」的题都是这一招 | O(n+m) / O(1) |
| **P1** | [LC-0409 - Longest Palindrome](02%20-%20Frequency%20Counting%20%E4%B8%8E%20Top%20K/05%20-%20LC-0409%20-%20Longest%20Palindrome) | E | 奇偶频率的贡献 | 从「数个数」变成「用个数算答案」：每个字母贡献 `c // 2 * 2`，最后有奇数就 +1 | O(n) / O(1) |
| **P1** | [LC-0697 - Degree of an Array](02%20-%20Frequency%20Counting%20%E4%B8%8E%20Top%20K/06%20-%20LC-0697%20-%20Degree%20of%20an%20Array) | E | 频率 + First/Last Occurrence | 一张表存三样东西（次数、首次、末次）。练的是「一次遍历顺手把要用的都记下来」 | O(n) / O(n) |
| **P1** | [LC-0229 - Majority Element II](02%20-%20Frequency%20Counting%20%E4%B8%8E%20Top%20K/07%20-%20LC-0229%20-%20Majority%20Element%20II) | M | 推广的 Boyer-Moore（两个候选） | > n/3 最多两个答案 → 两组候选 + **第二遍验证**。169 能省验证是因为题目保证答案存在，这题不能省 | O(n) / O(1) |

## 03 - Prefix Sum 与 Prefix-Suffix（6 题）

| | 题 | 难度 | Core Pattern | 为什么学它 / 和前面的区别 | 复杂度 |
|---|---|---|---|---|---|
| **P0** | [LC-0238 - Product of Array Except Self](03%20-%20Prefix%20Sum%20%E4%B8%8E%20Prefix-Suffix/01%20-%20LC-0238%20-%20Product%20of%20Array%20Except%20Self) 📦 | M | Prefix Product × Suffix Product | 前缀**积**不是前缀和。不许用除法逼你左右各扫一遍，输出数组复用成前缀积可做到 O(1) 额外空间 | O(n) / O(1) 额外 |
| **P0** | [LC-0560 - Subarray Sum Equals K](03%20-%20Prefix%20Sum%20%E4%B8%8E%20Prefix-Suffix/02%20-%20LC-0560%20-%20Subarray%20Sum%20Equals%20K) | M | Prefix Sum + 出现**次数** | 本层签名题：`sum(i..j)=k` ⟺ `pre[j]-pre[i]=k`。问**几个** → 哈希表存次数，边扫边累加 | O(n) / O(n) |
| **P1** | [LC-0724 - Find Pivot Index](03%20-%20Prefix%20Sum%20%E4%B8%8E%20Prefix-Suffix/03%20-%20LC-0724%20-%20Find%20Pivot%20Index) | E | Left Sum / Total Sum | 最朴素的前缀和应用，不需要哈希表。用来建立「前缀 + 总和 = 后缀」这个直觉 | O(n) / O(1) |
| **P0** | [LC-0525 - Contiguous Array](03%20-%20Prefix%20Sum%20%E4%B8%8E%20Prefix-Suffix/04%20-%20LC-0525%20-%20Contiguous%20Array) | M | 0→-1 + 第一次出现的**下标** | 和 0560 的关键区别：问**最长** → 哈希表存首次出现的位置，且只写一次（写成覆盖就变求最短） | O(n) / O(n) |
| **P0** | [LC-0974 - Subarray Sums Divisible by K](03%20-%20Prefix%20Sum%20%E4%B8%8E%20Prefix-Suffix/05%20-%20LC-0974%20-%20Subarray%20Sums%20Divisible%20by%20K) | M | Prefix Sum Modulo + 余数计数 | 键从「前缀和」换成「前缀和的余数」。必须说清负数取模：Python 的 % 恒非负，C++/Java 要 `((x%k)+k)%k` | O(n) / O(k) |
| **P1** | [LC-0304 - Range Sum Query 2D - Immutable](03%20-%20Prefix%20Sum%20%E4%B8%8E%20Prefix-Suffix/06%20-%20LC-0304%20-%20Range%20Sum%20Query%202D%20-%20Immutable) | M | 2D Prefix Sum + 容斥 | 一维推到二维：`大 - 上 - 左 + 左上`。padding 一圈 0 省掉所有边界特判。预处理换查询速度的典型 | 构造 O(mn) / 查询 O(1) |

## 04 - Array Index Mapping 与 In-place Marking（5 题）

| | 题 | 难度 | Core Pattern | 为什么学它 / 和前面的区别 | 复杂度 |
|---|---|---|---|---|---|
| **P1** | [LC-0448 - Find All Numbers Disappeared in an Array](04%20-%20Array%20Index%20Mapping%20%E4%B8%8E%20In-place%20Marking/01%20-%20LC-0448%20-%20Find%20All%20Numbers%20Disappeared%20in%20an%20Array) | E | Negative Marking（负号标记） | 值域恰好 1..n → 数组自己就是哈希表，用正负号当「出现过」的一位标记 | O(n) / O(1) |
| **P1** | [LC-0442 - Find All Duplicates in an Array](04%20-%20Array%20Index%20Mapping%20%E4%B8%8E%20In-place%20Marking/02%20-%20LC-0442%20-%20Find%20All%20Duplicates%20in%20an%20Array) | M | 同一套负号标记 | 和 0448 一字之差：标记时发现已经是负的，说明这个数第二次出现 | O(n) / O(1) |
| **P0** | [LC-0041 - First Missing Positive](04%20-%20Array%20Index%20Mapping%20%E4%B8%8E%20In-place%20Marking/03%20-%20LC-0041%20-%20First%20Missing%20Positive) | H | Cyclic Placement（原地归位） | 本层最难也最值钱：答案必在 1..n+1，把 v 换到下标 v-1。内层必须 while，且比较值不比较下标（防重复死循环） | O(n) / O(1) |
| **P0** | [LC-0287 - Find the Duplicate Number](04%20-%20Array%20Index%20Mapping%20%E4%B8%8E%20In-place%20Marking/04%20-%20LC-0287%20-%20Find%20the%20Duplicate%20Number) | M | Floyd 判圈（函数图） | **唯一不能改数组**的一题，所以标记法全部失效。把 `i → nums[i]` 看成函数图，重复值就是入环点 | O(n) / O(1) |
| **P1** | [LC-0073 - Set Matrix Zeroes](04%20-%20Array%20Index%20Mapping%20%E4%B8%8E%20In-place%20Marking/05%20-%20LC-0073%20-%20Set%20Matrix%20Zeroes) | M | 用第一行/第一列当标记位 | 标记思想的二维版：额外空间不够就把矩阵自己的边当作标记区，再单独处理第一行第一列 | O(mn) / O(1) |

## 05 - String Encoding 与 Compression（2 题）

| | 题 | 难度 | Core Pattern | 为什么学它 / 和前面的区别 | 复杂度 |
|---|---|---|---|---|---|
| **P0** | [LC-0271 - Encode and Decode Strings](05%20-%20String%20Encoding%20%E4%B8%8E%20Compression/01%20-%20LC-0271%20-%20Encode%20and%20Decode%20Strings) | M | Length-prefix Encoding（长度前缀编码） | 为什么不能用分隔符：任何分隔符都可能出现在内容里。写成 `len#payload` 后解码只需按长度切，天然无歧义 | 编解码各 O(n) / O(n) |
| **P1** | [LC-0443 - String Compression](05%20-%20String%20Encoding%20%E4%B8%8E%20Compression/02%20-%20LC-0443%20-%20String%20Compression) | M | Read / Write 双指针原地压缩 | 和上一题不是同一个模板：这题练的是**原地改写 + 返回新长度**，read 指针永远不落后于 write 指针 | O(n) / O(1) |

## 06 - 低优先级与跨专题题目（14 题）

**这不是必刷文件夹。** 作用是保存已有学习成果，不让低迁移性题目占据主线。

| | 题 | 难度 | 为什么放在这里 |
|---|---|---|---|
| **P2** | [LC-0219 - Contains Duplicate II](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/01%20-%20LC-0219%20-%20Contains%20Duplicate%20II) | E | 滑动窗口更合适（窗口大小 k 的 Set），放这里只因为它也用哈希表 |
| **P2** | [LC-0290 - Word Pattern](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/02%20-%20LC-0290%20-%20Word%20Pattern) | E | 和 LC-0205 的双向映射思想几乎重复，练完 0205 就够了 |
| **P2** | [LC-0350 - Intersection of Two Arrays II](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/03%20-%20LC-0350%20-%20Intersection%20of%20Two%20Arrays%20II) | E | 排序 + 双指针或计数表都行，技巧含量低 |
| **P2** | [LC-0349 - Intersection of Two Arrays](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/04%20-%20LC-0349%20-%20Intersection%20of%20Two%20Arrays) | E | 0350 的去重版，更简单 |
| **P2** | [LC-0953 - Verifying an Alien Dictionary](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/05%20-%20LC-0953%20-%20Verifying%20an%20Alien%20Dictionary) | E | 字母序重映射，纯模拟 |
| **P2** | [LC-1207 - Unique Number of Occurrences](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/06%20-%20LC-1207%20-%20Unique%20Number%20of%20Occurrences) | E | Counter 的 values 去重，两行题 |
| **P2** | [LC-0645 - Set Mismatch](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/07%20-%20LC-0645%20-%20Set%20Mismatch) | E | 和 Level 04 的 index mapping 高度重复 |
| **P2** | [LC-0243 - Shortest Word Distance](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/08%20-%20LC-0243%20-%20Shortest%20Word%20Distance) | E | 线性扫描记上一次位置，更接近双指针 |
| **P2** | [LC-0266 - Palindrome Permutation](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/09%20-%20LC-0266%20-%20Palindrome%20Permutation) | E | 0409 的子集（只问能不能，不问长度） |
| **P2** | [LC-0389 - Find the Difference](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/10%20-%20LC-0389%20-%20Find%20the%20Difference) | E | 计数差 / 异或，一行题 |
| **P2** | [LC-2768 - Number of Black Blocks](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/11%20-%20LC-2768%20-%20Number%20of%20Black%20Blocks) | M | 二维计数 + 容斥，题面复杂、迁移性低 |
| **P2** | [LC-3440 - Reschedule Meetings for Maximum Free Time II](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/12%20-%20LC-3440%20-%20Reschedule%20Meetings%20for%20Maximum%20Free%20Time%20II) | M | 核心是 Greedy + Prefix/Suffix Max，不是普通前缀和 |
| **P2** | [LC-3234 - Count the Number of Substrings With Dominant Ones](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/13%20-%20LC-3234%20-%20Count%20the%20Number%20of%20Substrings%20With%20Dominant%20Ones) | M | 专门的子串计数技巧，当前阶段性价比低 |
| **P2** | [LC-2048 - Next Greater Numerically Balanced Number](06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/14%20-%20LC-2048%20-%20Next%20Greater%20Numerically%20Balanced%20Number) | M | 暴力枚举 + 数位性质，和数组哈希关系不大 |

📦 = 该题文件夹里有 `_neetcode/` 子目录，保存着 NeetCode 版本的原始题面与解法（同一道题，不单独占位置）。

## Pattern Recognition Guide（看到什么想到什么）

| 题面信号 | 第一反应 | 代表题 |
|---|---|---|
| 要快速判断「见过没有」 | Hash Set | 0217 / 0128 |
| 要「见过的那个东西」本身（下标、位置） | Hash Map | 0001 / 0243 |
| 要数出现次数 | Frequency Map / Counter | 0242 / 0383 / 0387 |
| 要把「长得一样的」归到一起 | 设计一个 Canonical Key | 0049 |
| 要出现次数最多的 K 个 | Bucket Sort（O(n)）或 Heap（O(n log k)）| 0347 |
| 要 > n/k 的众数，且要求 O(1) 空间 | Boyer-Moore，k-1 组候选 + 验证 | 0169 / 0229 |
| 数**有多少个**和为 target 的子数组 | 前缀和 + 哈希表存**次数** | 0560 |
| 求**最长**的、满足前缀状态相等的区间 | 前缀和 + 哈希表存**首次出现的下标** | 0525 |
| 区间和能被 K 整除 | 前缀和**取模** + 余数计数 | 0974 |
| 不许用除法 / 要左右两边的信息 | Prefix × Suffix 两遍扫描 | 0238 |
| 矩阵多次查询子矩形和 | 2D 前缀和 + 容斥，padding 一圈 0 | 0304 |
| 值域恰好是 1..n，要 O(1) 空间 | 下标映射：原地归位或负号标记 | 0041 / 0448 / 0442 |
| 值域是 1..n 但**不许改数组** | Floyd 判圈 | 0287 |
| 要把任意字符串列表编码成一个串 | Length-prefix Encoding `len#payload` | NC Encode/Decode |
| 要 O(1) 的 insert / delete / getRandom | Hash Map + Dynamic Array，删除换末尾 | 0380 |

## 三道最容易混的题，放在一起记

它们都是「前缀状态 + 哈希表」，但**存什么、什么时候写**完全不同：

| | 问的是 | 键 | 值 | 写入时机 |
|---|---|---|---|---|
| **0560** | 有几个 | 前缀和 | 出现**次数** | 每次都写 |
| **0525** | 最长多长 | 前缀和（0 记作 -1）| **首次出现的下标** | 只在键不存在时写 |
| **0974** | 有几个 | 前缀和的**余数** | 出现**次数** | 每次都写 |

三题都需要一个哨兵（`{0: -1}` 或 `cnt[0] = 1`）代表空前缀，漏了它就会丢掉「从下标 0 开始」的那些答案。

## 什么时候可以改输入数组

Level 04 的五道题全靠「能不能改 nums」分家：

- **可以改**（题目没有禁止）→ 原地归位 / 负号标记，O(1) 额外空间：0041、0442、0448、0073

- **不能改**（题目明确要求）→ 标记法全部失效，改用 Floyd 判圈：0287

面试里要主动问一句「输入可以修改吗」，这是这一层的得分点。

## 推荐刷题顺序

```
打地基   0001 → 0217 → 0242 → 0049 → 0128
加约束   0036 → 0205 → 0454 → 0380
学计数   0347 → 0169 → 0229 → 0387 → 0383 → 0409 → 0697
前缀状态 0724 → 0238 → 0560 → 0525 → 0974 → 0304
下标映射 0448 → 0442 → 0041 → 0287 → 0073
字符串   NC Encode/Decode → 0443
```

每一行内部是递进关系，跨行可以并行。P2 的 14 道题留到复习期再翻，不要在主线上花时间。

## 共享资料

- `_resources/unclassified/asset-001 - 3197 - ALL - Find the Minimum Area to Cover All Ones II.pdf`
  —— 原来错放在 LC-2768 文件夹里，内容实际是 **LC-3197** 的官方题解（本仓库目前只有 LC-3195，在 `15-math-geometry/matrix/`）。没有删除，挪到这里等你决定去处。



---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-0249 Group Shifted Strings](<./01 - Hash Set 与 Hash Map 基础/10 - LC-0249 - Group Shifted Strings>) | `01 - Hash Set 与 Hash Map 基础` | 规范化键 = 相邻字母差 mod 26（az 与 ba 必须同组）；和 LC-0049 同套路 | 环绕是全部考点；Premium 题 |
| [LC-0791 Custom Sort String](<./02 - Frequency Counting 与 Top K/08 - LC-0791 - Custom Sort String>) | `02 - Frequency Counting 与 Top K` | 计数 + 按 order 输出 = 26 桶的桶排序；不在 order 里的字母也要输出 | LC-0049 式「规范化输出」 |
| [LC-0523 Continuous Subarray Sum](<./03 - Prefix Sum 与 Prefix-Suffix/07 - LC-0523 - Continuous Subarray Sum>) | `03 - Prefix Sum 与 Prefix-Suffix` | P[j] ≡ P[i] (mod k)；只记余数首次位置 + 哨兵 {0:-1}，长度 j-i>=2 | LC-0560 / LC-0974 之间的一环 |
| [LC-0937 Reorder Data in Log Files](<./06 - 低优先级与跨专题题目/15 - LC-0937 - Reorder Data in Log Files>) | `06 - 低优先级与跨专题题目` | 单一排序键 (0,content,id) / (1,)，数字日志靠**稳定排序**保序；要说出依赖稳定性 | Amazon 热身 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
