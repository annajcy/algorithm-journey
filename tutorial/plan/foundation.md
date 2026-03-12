# 基础阶段

> [返回课程总览](overview.md)

## 阶段说明

| 项目 | 内容 |
| --- | --- |
| 适合人群 | 已完成入门复习，准备系统补齐 `必备` 专题 |
| 主语言 | C++ |
| 内容范围 | 只覆盖 `019-098` 的 `必备` 内容 |
| 前置要求 | 已掌握基础数据结构、递归、二分、树遍历 |
| 推荐学习方式 | 按专题推进，优先吃透主干模板和高频题型 |
| 题目来源说明 | `src/` 中 Java 代码只作为题目来源，讲解与模板全部使用 C++ |
| 建议节奏 | 6 周完成，30 课 |

## 每日 Codeforces 思维题训练

| 项目 | 内容 |
| --- | --- |
| 训练定位 | 偏 `模型识别 + 分类讨论`，建立题意到常见算法模型的映射能力 |
| 题目级别 | `Div2 B -> Div2 C` |
| 每日题量 | 1 题为主，偶尔 2 题 |
| 建议限时 | 35-45 分钟 |
| 执行规则 | 先独立思考，再写关键思路，再编码，最后复盘；优先选和当周主线专题接近的题；开始记录“这题为什么不是贪心/二分/DP/图论”的错判原因；只建议在周末或复盘日偶尔加到 2 题 |

## 本阶段知识地图

| Week | 知识域 | 训练类型 | 为什么这样排 |
| --- | --- | --- | --- |
| Week 1 | `基础编码`、`数据结构` | `模板课`、`结构原理` | 从输入输出、递归、排序和堆开始，把必备阶段重新接到入门之后 |
| Week 2 | `数据结构`、`树` | `结构原理`、`专题题` | 继续补齐链表、设计题、二叉树等高频面试和竞赛主干 |
| Week 3 | `树`、`数论`、`字符串`、`数据结构` | `结构原理`、`专题题` | 把树、数论预备、Trie、前缀和、差分等基础方法串起来 |
| Week 4 | `数据结构`、`图论` | `模板课`、`专题题` | 从滑窗和单调结构过渡到并查集、BFS 和图存储 |
| Week 5 | `图论`、`DP` | `结构原理`、`专题题` | 先收图论主干，再切入最核心的 DP 基础模型 |
| Week 6 | `DP`、`综合复盘` | `专题题`、`综合题`、`复盘课` | 用 DP 进阶、贪心博弈和总复盘完成必备阶段收束 |

每周课程主线之外，持续执行 `每日 1 题` 的 Codeforces 思维训练，且选题尽量贴合本周主线专题。

## 课程模板

- 课程主题
- 学习目标
- 对应原课
- 知识点讲解（C++）
- 题目来源（src Java）
- C++ 模板
- 习题
- 复盘要点
- 完成标准

这条模板用于课程主线；每日 Codeforces 思维题训练按阶段规则单独执行，不展开到 `Day 1 ~ Day 7`。

## 快速跳转

- [Week 1](#week-1)
- [Week 2](#week-2)
- [Week 3](#week-3)
- [Week 4](#week-4)
- [Week 5](#week-5)
- [Week 6](#week-6)

## Week 1

| 知识域 | 训练类型 | 本周目标 |
| --- | --- | --- |
| `基础编码`、`数据结构` | `模板课`、`结构原理` | 把输入输出、递归、分治排序、随机化和堆这一批主干模板重新接起来 |

### 课程 01：算法笔试输入输出、递归与 Master

- 学习目标：恢复 OJ 输入输出规范和递归分析框架
- 对应原课：019、020
- 知识点讲解（C++）：高效输入输出、递归设计三问、Master 公式
- 题目来源（src Java）：`src/class019/Code05_Kattio.java`、`src/class019/Code06_FastReaderWriter.java`、`src/class020/GetMaxValue.java`
- C++ 模板：`fast io` 模板、递归框架模板
- 习题：写一份稳定的 OJ 模板；做 2 道递归分析题
- 复盘要点：递归先定状态和返回值，再谈转移
- 完成标准：能手写比赛级输入模板并解释 Master 公式

### 课程 02：递归过程设计与 N 皇后

- 学习目标：恢复回溯、枚举和剪枝套路
- 对应原课：038、039、040
- 知识点讲解（C++）：子序列、排列组合、嵌套递归、N 皇后剪枝与位运算优化
- 题目来源（src Java）：`src/class038/Code01_Subsequences.java`、`src/class038/Code03_Permutations.java`、`src/class039/Code02_DecodeString.java`、`src/class040/NQueens.java`
- C++ 模板：回溯模板、表达式递归模板、位运算版 N 皇后模板
- 习题：做 2 道回溯题；手写位运算版 N 皇后
- 复盘要点：回溯题先定搜索树，再写剪枝
- 完成标准：能解释一个回溯过程的状态和剪枝点

### 课程 03：归并排序与归并分治

- 学习目标：恢复分治排序和统计类问题套路
- 对应原课：021、022
- 知识点讲解（C++）：归并排序、归并统计、小和、逆序对
- 题目来源（src Java）：`src/class021/Code01_MergeSort.java`、`src/class022/Code01_SmallSum1.java`、`src/class022/Code02_ReversePairs.java`
- C++ 模板：归并排序模板、归并统计模板
- 习题：做 2 道归并统计题
- 复盘要点：关键在于利用“左右部分已排序”
- 完成标准：能识别是否能用归并分治顺带统计信息

### 课程 04：快速排序与随机选择

- 学习目标：恢复三路划分与随机化思想
- 对应原课：023、024
- 知识点讲解（C++）：荷兰国旗、随机快排、快速选择、期望复杂度
- 题目来源（src Java）：`src/class023/Code01_QuickSort.java`、`src/class024/RandomizedSelect.java`
- C++ 模板：三路快排模板、快速选择模板
- 习题：手写三路快排；做 1 道第 k 小题
- 复盘要点：随机化是为了降低最坏分布风险
- 完成标准：能用三路划分处理重复值数组

### 课程 05：堆结构、堆排序与堆题

- 学习目标：恢复优先队列和动态最值维护
- 对应原课：025、027
- 知识点讲解（C++）：堆的数组实现、堆排序、合并 K 路、区间覆盖
- 题目来源（src Java）：`src/class025/Code01_HeapSort.java`、`src/class027/Code01_MergeKSortedLists.java`、`src/class027/Code02_MaxCover.java`
- C++ 模板：`priority_queue` 模板、手写堆模板
- 习题：做 2 道堆题；手写堆排序
- 复盘要点：堆用于维护当前最值，不提供全局有序遍历
- 完成标准：能判断一题是否适合用堆维护答案

## Week 2

| 知识域 | 训练类型 | 本周目标 |
| --- | --- | --- |
| `数据结构`、`树` | `结构原理`、`专题题` | 通过链表、设计题和树高频题把最常用结构做扎实 |

### 课程 06：哈希表、有序表、基数排序与排序总览

- 学习目标：恢复容器选型和排序方法论
- 对应原课：026、028、029
- 知识点讲解（C++）：`unordered_map`、`map`、比较器、基数排序、排序方法适用场景
- 题目来源（src Java）：`src/class026/Code01_HashSetAndHashMap.java`、`src/class026/Code02_TreeSetAndTreeMap.java`、`src/class026/Code03_Comparator.java`、`src/class028/Code01_RadixSort.java`
- C++ 模板：哈希表模板、有序表模板、自定义比较器模板
- 习题：整理容器复杂度；做 2 道容器选型题
- 复盘要点：先看操作集合，再选数据结构
- 完成标准：能快速判断该用哈希、堆还是有序表

### 课程 07：位运算进阶

- 学习目标：补齐异或技巧、位图和位运算四则运算
- 对应原课：030、031、032、033
- 知识点讲解（C++）：异或性质、判幂、位图、位运算实现加减乘除
- 题目来源（src Java）：`src/class030/Code03_MissingNumber.java`、`src/class031/Code01_PowerOfTwo.java`、`src/class032/Code01_Bitset.java`、`src/class033/BitOperationAddMinusMultiplyDivide.java`
- C++ 模板：位图模板、位运算工具模板
- 习题：做 2 道异或题；实现一个位图；写出位运算加法
- 复盘要点：位运算题核心是性质，不是技巧堆砌
- 完成标准：能熟练处理判幂、异或找数、位图压缩

### 课程 08：链表高频技巧

- 学习目标：恢复复杂链表题的常见套路
- 对应原课：034
- 知识点讲解（C++）：相交链表、k 组反转、复制随机链表、找环、链表排序
- 题目来源（src Java）：`src/class034/Code01_IntersectionOfTwoLinkedLists.java`、`src/class034/Code02_ReverseNodesInkGroup.java`、`src/class034/Code03_CopyListWithRandomPointer.java`、`src/class034/Code05_LinkedListCycleII.java`
- C++ 模板：快慢指针模板、k 组反转模板、随机链表复制模板
- 习题：做 3 道链表综合题
- 复盘要点：复杂链表题先拆成若干局部重连
- 完成标准：能稳定处理环、相交、分组反转

### 课程 09：数据结构设计高频题

- 学习目标：恢复设计类题的接口与复杂度意识
- 对应原课：035
- 知识点讲解（C++）：LRU、随机集合、中位数维护、频率栈
- 题目来源（src Java）：`src/class035/Code01_SetAllHashMap.java`、`src/class035/Code02_LRU.java`、`src/class035/Code03_InsertDeleteRandom.java`、`src/class035/Code05_MedianFinder.java`
- C++ 模板：LRU 模板、随机集合模板、双堆中位数模板
- 习题：手写 LRU；做 1 道设计题
- 复盘要点：设计题先定操作复杂度目标
- 完成标准：能解释 LRU 或随机集合的复杂度来源

### 课程 10：二叉树高频题 I

- 学习目标：恢复基础树题的遍历、构造与序列化
- 对应原课：036
- 知识点讲解（C++）：层序遍历、序列化、反序列化、建树、完全二叉树判断
- 题目来源（src Java）：`src/class036/Code01_LevelOrderTraversal.java`、`src/class036/Code05_PreorderSerializeAndDeserialize.java`、`src/class036/Code07_PreorderInorderBuildBinaryTree.java`
- C++ 模板：层序遍历模板、序列化模板、建树模板
- 习题：做 3 道遍历/建树题
- 复盘要点：树题先明确你要收集的信息类型
- 完成标准：能独立完成基础树题模板书写

## Week 3

| 知识域 | 训练类型 | 本周目标 |
| --- | --- | --- |
| `树`、`数论`、`字符串`、`数据结构` | `结构原理`、`专题题` | 把树、数论、Trie、前缀和与差分这些基础模型打通 |

### 课程 11：二叉树高频题 II

- 学习目标：恢复 LCA、BST 与树上信息收集
- 对应原课：037
- 知识点讲解（C++）：最近公共祖先、BST 判定、平衡树、树形打家劫舍
- 题目来源（src Java）：`src/class037/Code01_LowestCommonAncestor.java`、`src/class037/Code04_BalancedBinaryTree.java`、`src/class037/Code07_HouseRobberIII.java`
- C++ 模板：LCA 模板、BST 判定模板、树上返回信息模板
- 习题：做 2 道 LCA/BST 题；做 1 道树形 DP 入门题
- 复盘要点：树题解法上限取决于返回值设计
- 完成标准：能用“返回信息”视角描述树题

### 课程 12：数论预备、打表找规律与数据量猜解法

- 学习目标：恢复数学直觉和“从数据范围反推解法”的能力
- 对应原课：041、042、043、097、098
- 知识点讲解（C++）：gcd/lcm、同余、打表找规律、质数判断、筛法、快速幂
- 题目来源（src Java）：`src/class041/Code01_GcdAndLcm.java`、`src/class042/Code01_AppleMinBags.java`、`src/class043/Code01_KillMonsterEverySkillUseOnce.java`、`src/class097/Code04_EhrlichAndEuler.java`、`src/class098/Code01_QuickPower.java`
- C++ 模板：gcd 模板、筛法模板、快速幂模板、暴力对拍模板
- 习题：做 2 道数论基础题；做 1 道打表规律题
- 复盘要点：先做数学化简，再做算法优化
- 完成标准：能独立写出 gcd、快速幂、筛法模板

### 课程 13：前缀树与相关题目

- 学习目标：恢复 Trie 与异或 Trie 的建模能力
- 对应原课：044、045
- 知识点讲解（C++）：Trie 插入查询、前缀统计、异或 Trie、字符串搜索
- 题目来源（src Java）：`src/class044/Code01_TrieTree.java`、`src/class045/Code02_TwoNumbersMaximumXor.java`、`src/class045/Code03_WordSearchII.java`
- C++ 模板：字符串 Trie 模板、异或 Trie 模板
- 习题：手写 1 个字符串 Trie；做 2 道 Trie 题
- 复盘要点：Trie 的本质是按字符或按位逐层决策
- 完成标准：能从零写出字符串 Trie 和异或 Trie

### 课程 14：前缀和与子数组问题

- 学习目标：恢复前缀和与哈希统计套路
- 对应原课：046
- 知识点讲解（C++）：区间和、和为目标值、最长/个数统计、哈希优化
- 题目来源（src Java）：`src/class046/Code01_PrefixSumArray.java`、`src/class046/Code02_LongestSubarraySumEqualsAim.java`、`src/class046/Code03_NumberOfSubarraySumEqualsAim.java`
- C++ 模板：前缀和模板、前缀和 + 哈希模板
- 习题：做 3 道前缀和题
- 复盘要点：很多区间问题都能转成两个前缀的差
- 完成标准：能识别哪些子数组题可转化为前缀和

### 课程 15：差分与二维预处理

- 学习目标：恢复区间修改和矩阵预处理套路
- 对应原课：047、048
- 知识点讲解（C++）：一维差分、等差差分、二维前缀和、二维差分、离散化
- 题目来源（src Java）：`src/class047/Code01_CorporateFlightBookings.java`、`src/class047/Code02_ArithmeticSequenceDifference.java`、`src/class048/Code01_PrefixSumMatrix.java`、`src/class048/Code03_DiffMatrixLuogu.java`
- C++ 模板：差分模板、二维前缀和模板、二维差分模板
- 习题：做 2 道区间修改题；做 1 道二维前缀和题
- 复盘要点：预处理的价值是把多次查询降到 O(1) 或 O(log n)
- 完成标准：能无参考写出一维差分和二维前缀和

## Week 4

| 知识域 | 训练类型 | 本周目标 |
| --- | --- | --- |
| `数据结构`、`图论` | `模板课`、`专题题` | 从数组技巧自然过渡到并查集、BFS 和图存储与拓扑排序 |

### 课程 16：滑动窗口与双指针

- 学习目标：恢复窗口维护与边界移动的题感
- 对应原课：049、050
- 知识点讲解（C++）：定长窗口、不定长窗口、左右指针、快慢指针
- 题目来源（src Java）：`src/class049/Code01_MinimumSizeSubarraySum.java`、`src/class049/Code02_LongestSubstringWithoutRepeatingCharacters.java`、`src/class049/Code03_MinimumWindowSubstring.java`、`src/class050/Code01_SortArrayByParityII.java`
- C++ 模板：滑动窗口模板、双指针模板
- 习题：做 3 道窗口题；总结窗口成立条件
- 复盘要点：窗口成立的前提是状态可维护且边界单调
- 完成标准：能快速判断窗口题和前缀和题的边界

### 课程 17：二分答案、单调栈、单调队列

- 学习目标：恢复三类高频技巧的适用条件
- 对应原课：051、052、053、054、055
- 知识点讲解（C++）：答案二分判定、最近更大更小、窗口最值维护
- 题目来源（src Java）：`src/class051/Code01_KokoEatingBananas.java`、`src/class052/Code01_LeftRightLess.java`、`src/class053/Code01_MaximumWidthRamp.java`、`src/class054/Code01_SlidingWindowMaximum.java`
- C++ 模板：答案二分模板、单调栈模板、单调队列模板
- 习题：做 1 道二分答案题；做 2 道单调结构题
- 复盘要点：先找单调性或局部最优结构
- 完成标准：能判断一题更适合二分还是单调结构

### 课程 18：并查集

- 学习目标：恢复集合合并与连通性维护
- 对应原课：056、057
- 知识点讲解（C++）：路径压缩、按规模合并、连通块问题、映射并查集
- 题目来源（src Java）：`src/class056/Code01_UnionFindNowCoder.java`、`src/class057/Code01_MostStonesRemovedWithSameRowOrColumn.java`
- C++ 模板：标准并查集模板、映射并查集模板
- 习题：手写标准并查集；做 2 道连通块题
- 复盘要点：并查集维护的是集合代表元，不是遍历过程
- 完成标准：能独立写出带路径压缩的并查集

### 课程 19：洪水填充、BFS、双向广搜

- 学习目标：恢复层次遍历和最短步数问题解法
- 对应原课：058、062、063
- 知识点讲解（C++）：Flood Fill、普通 BFS、多源 BFS、双向 BFS
- 题目来源（src Java）：`src/class058/Code01_NumberOfIslands.java`、`src/class062/Code01_AsFarFromLandAsPossible.java`、`src/class063/Code01_WordLadder.java`
- C++ 模板：网格 BFS 模板、多源 BFS 模板、双向 BFS 模板
- 习题：做 2 道网格 BFS 题；做 1 道双向 BFS 题
- 复盘要点：BFS 的关键是按层扩展
- 完成标准：能稳定写出网格 BFS 和双向 BFS

### 课程 20：建图、拓扑排序与图存储

- 学习目标：恢复竞赛风格建图和 DAG 基础处理
- 对应原课：059、060
- 知识点讲解（C++）：邻接表、链式前向星、入度数组、Kahn 拓扑排序
- 题目来源（src Java）：`src/class059/Code01_CreateGraph.java`、`src/class059/Code02_TopoSortDynamicNowcoder.java`、`src/class060/Code01_FoodLines.java`
- C++ 模板：链式前向星模板、拓扑排序模板
- 习题：手写链式前向星；做 2 道 DAG 题
- 复盘要点：图题先定存图方式，再选算法
- 完成标准：能在比赛输入下快速建图

## Week 5

| 知识域 | 训练类型 | 本周目标 |
| --- | --- | --- |
| `图论`、`DP` | `结构原理`、`专题题` | 先吃下最短路和最小生成树，再切入线性和二维 DP 主干 |

### 课程 21：最小生成树与最短路 I

- 学习目标：恢复加权图中的主干算法
- 对应原课：061、064
- 知识点讲解（C++）：Kruskal、Prim、Dijkstra、堆优化、分层图最短路
- 题目来源（src Java）：`src/class061/Code01_Kruskal.java`、`src/class061/Code02_PrimStatic.java`、`src/class064/Code01_DijkstraLeetcode.java`
- C++ 模板：Kruskal 模板、Prim 模板、Dijkstra 模板
- 习题：做 1 道 MST 题；做 2 道 Dijkstra 题
- 复盘要点：先区分“连通代价最小”和“路径代价最小”
- 完成标准：能快速分辨 MST 和最短路模型

### 课程 22：最短路 II

- 学习目标：补齐负权和全源最短路体系
- 对应原课：065
- 知识点讲解（C++）：Bellman-Ford、SPFA、Floyd、A*
- 题目来源（src Java）：`src/class065/Code01_AStarAlgorithm.java`、`src/class065/Code02_Floyd.java`、`src/class065/Code03_BellmanFord.java`、`src/class065/Code04_SPFA.java`
- C++ 模板：Bellman-Ford 模板、SPFA 模板、Floyd 模板
- 习题：做 1 道负权最短路题；总结各算法适用条件
- 复盘要点：遇到负权边先重新判断算法合法性
- 完成标准：能说明四种最短路算法的适用场景

### 课程 23：一维 DP 与子数组 DP

- 学习目标：恢复线性 DP 的建模能力
- 对应原课：066、070、071、072
- 知识点讲解（C++）：从递归到 DP、最大子数组和、LIS、多子数组选择
- 题目来源（src Java）：`src/class066/Code01_FibonacciNumber.java`、`src/class070/Code01_MaximumSubarray.java`、`src/class071/Code04_MaximumSum3UnoverlappingSubarrays.java`、`src/class072/Code01_LongestIncreasingSubsequence.java`
- C++ 模板：线性 DP 模板、LIS 模板
- 习题：做 3 道一维 DP；做 1 道 LIS 题
- 复盘要点：DP 先定义状态，再考虑优化
- 完成标准：能把简单递归改写成一维 DP

### 课程 24：二维/三维 DP

- 学习目标：恢复多维状态设计
- 对应原课：067、068、069
- 知识点讲解（C++）：二维状态、网格 DP、三维状态设计、空间压缩意识
- 题目来源（src Java）：`src/class067/Code01_MinimumPathSum.java`、`src/class068/Code01_DistinctSubsequences.java`、`src/class069/Code01_OnesAndZeroes.java`
- C++ 模板：二维 DP 模板、三维 DP 基础模板
- 习题：做 2 道二维 DP；做 1 道三维 DP
- 复盘要点：维度增加时先问每一维是否必要
- 完成标准：能自己定义二维或三维状态

### 课程 25：背包 DP I

- 学习目标：恢复 01、完全、分组背包主干模型
- 对应原课：073、074
- 知识点讲解（C++）：01 背包、完全背包、分组背包、有依赖背包
- 题目来源（src Java）：`src/class073/Code01_01Knapsack.java`、`src/class073/Code05_DependentKnapsack.java`、`src/class074/Code01_PartitionedKnapsack.java`
- C++ 模板：01 背包模板、完全背包模板、分组背包模板
- 习题：做 3 道背包题；总结循环顺序差异
- 复盘要点：背包最容易错在枚举方向
- 完成标准：能区分并写对 01/完全/分组背包

## Week 6

| 知识域 | 训练类型 | 本周目标 |
| --- | --- | --- |
| `DP`、`综合复盘` | `专题题`、`综合题`、`复盘课` | 用 DP 进阶、贪心博弈和总复盘完成基础阶段收束 |

### 课程 26：背包 DP II 与区间 DP

- 学习目标：补齐多重背包和区间 DP
- 对应原课：075、076、077
- 知识点讲解（C++）：多重背包、混合背包、区间 DP、合并型区间 DP
- 题目来源（src Java）：`src/class075/Code01_BoundedKnapsack.java`、`src/class075/Code05_MixedKnapsack.java`、`src/class076/Code04_MinimumCostToCutAStick.java`、`src/class077/Code05_MinimumCostToMergeStones.java`
- C++ 模板：多重背包模板、区间 DP 模板
- 习题：做 2 道背包进阶题；做 2 道区间 DP
- 复盘要点：区间 DP 通常按区间长度递推
- 完成标准：能写出标准区间 DP 枚举框架

### 课程 27：树形 DP 与状压 DP

- 学习目标：恢复树上状态设计和状态压缩
- 对应原课：078、079、080、081
- 知识点讲解（C++）：树形 DP 返回信息、换根思维、状态压缩、子集枚举
- 题目来源（src Java）：`src/class078/Code06_BinaryTreeCameras.java`、`src/class078/Code05_Dancing.java`、`src/class080/Code01_CanIWin.java`、`src/class081/Code01_NumberOfWaysWearDifferentHats.java`
- C++ 模板：树形 DP 模板、状压 DP 模板、子集枚举模板
- 习题：做 2 道树形 DP；做 2 道状压 DP
- 复盘要点：树形 DP 关键在于“节点返回什么”
- 完成标准：能用返回信息或压缩状态描述解法

### 课程 28：DP 进阶方法论

- 学习目标：建立 DP 题型分类和优化意识
- 对应原课：082、083、086、087、088
- 知识点讲解（C++）：观察优化枚举、数据量猜 DP、决策恢复、专题总结
- 题目来源（src Java）：`src/class082/Code04_Stock4.java`、`src/class083/Code02_KInversePairsArray.java`、`src/class086/Code03_LIS.java`、`src/class087/Code04_MakeArrayStrictlyIncreasing.java`
- C++ 模板：决策恢复模板、DP 分类 checklist
- 习题：做 2 道优化型 DP；整理自己的 DP 分类笔记
- 复盘要点：做 DP 先归类，再套状态设计
- 完成标准：能把常见 DP 题归到固定模型里

### 课程 29：贪心与博弈

- 学习目标：恢复排序贪心、区间贪心和基础博弈结论
- 对应原课：089、090、091、092、093、094、095、096
- 知识点讲解（C++）：局部最优到全局最优、区间安排、构造型贪心、必胜态与必败态
- 题目来源（src Java）：`src/class089/Code02_TwoCityScheduling.java`、`src/class090/Code05_IPO.java`、`src/class094/Code03_MaximumAveragePassRatio.java`、`src/class095/Code01_BashGame.java`、`src/class096/Code01_BashGameSG.java`
- C++ 模板：排序贪心模板、区间调度模板、基础博弈结论模板
- 习题：做 3 道贪心题；做 2 道博弈入门题
- 复盘要点：不会证明贪心时，先尝试找反例
- 完成标准：能初步判断题目是否具备贪心结构

### 课程 30：基础总复盘

- 学习目标：完成 `必备` 阶段闭环，明确后续进阶入口
- 对应原课：019-098 总复盘
- 知识点讲解（C++）：图论/DP/数据结构/数论模板回收；高频错因整理；后续 `扩展` 学习入口
- 题目来源（src Java）：从前 29 课中各选 1 个代表题二刷
- C++ 模板：个人模板总表、错题归档模板
- 习题：整理 20 个高频模板点；完成 10 题二刷清单
- 复盘要点：复习闭环不是“看完”，而是“能独立写”
- 完成标准：形成自己的 C++ 模板库和错题清单
