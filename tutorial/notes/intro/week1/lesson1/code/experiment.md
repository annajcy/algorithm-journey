# Experiment C++ 译写

> [返回课程 01 正文](../content.md)

- 程序性质：课程实验程序
- 说明：本页直接保存并展示课程使用的 C++ 代码

## 代码

```cpp
// Lesson 1 code translation
// Source class: src/class002/Experiment.java
// Problem source: none, course experiment program

#include <algorithm>
#include <chrono>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>
using namespace std;

struct Experiment {
    inline static mt19937 rng(
        static_cast<unsigned>(chrono::steady_clock::now().time_since_epoch().count())
    );

    static void experiment(int n, int t) {
        vector<double> wealth(n, 100.0);
        vector<bool> hasMoney(n, false);
        uniform_int_distribution<int> dist(0, n - 1);

        for (int i = 0; i < t; ++i) {
            fill(hasMoney.begin(), hasMoney.end(), false);
            for (int j = 0; j < n; ++j) {
                if (wealth[j] > 0) {
                    hasMoney[j] = true;
                }
            }
            for (int j = 0; j < n; ++j) {
                if (hasMoney[j]) {
                    int other = j;
                    do {
                        other = dist(rng);
                    } while (other == j);
                    wealth[j]--;
                    wealth[other]++;
                }
            }
        }

        sort(wealth.begin(), wealth.end());
        cout << "列出每个人的财富(贫穷到富有) : " << '\n';
        for (int i = 0; i < n; ++i) {
            cout << static_cast<int>(wealth[i]) << ' ';
            if (i % 10 == 9) {
                cout << '\n';
            }
        }
        cout << '\n';
        cout << "这个社会的基尼系数为 : " << calculateGini(wealth) << '\n';
    }

    static double calculateGini(const vector<double>& wealth) {
        double sumOfAbsoluteDifferences = 0;
        double sumOfWealth = 0;
        int n = static_cast<int>(wealth.size());
        for (int i = 0; i < n; ++i) {
            sumOfWealth += wealth[i];
            for (int j = 0; j < n; ++j) {
                sumOfAbsoluteDifferences += abs(wealth[i] - wealth[j]);
            }
        }
        return sumOfAbsoluteDifferences / (2 * n * sumOfWealth);
    }
};

int main() {
    cout << "一个社会的基尼系数是一个在0~1之间的小数" << '\n';
    cout << "基尼系数为0代表所有人的财富完全一样" << '\n';
    cout << "基尼系数为1代表有1个人掌握了全社会的财富" << '\n';
    cout << "基尼系数越小，代表社会财富分布越均衡；越大则代表财富分布越不均衡" << '\n';
    cout << "在2022年，世界各国的平均基尼系数为0.44" << '\n';
    cout << "目前普遍认为，当基尼系数到达 0.5 时" << '\n';
    cout << "就意味着社会贫富差距非常大，分布非常不均匀" << '\n';
    cout << "社会可能会因此陷入危机，比如大量的犯罪或者经历社会动荡" << '\n';
    cout << "测试开始" << '\n';
    int n = 100;
    int t = 1000000;
    cout << "人数 : " << n << '\n';
    cout << "轮数 : " << t << '\n';
    Experiment::experiment(n, t);
    cout << "测试结束" << '\n';
    return 0;
}
```
