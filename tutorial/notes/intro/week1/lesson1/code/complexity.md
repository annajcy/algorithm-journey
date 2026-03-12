# Complexity C++ 译写

> [返回课程 01 正文](../content.md)

- 程序性质：课程演示程序
- 说明：本页直接保存并展示课程使用的 C++ 代码

## 代码

```cpp
// Lesson 1 code translation
// Source class: src/class007/Complexity.java
// Problem source: none, complexity demonstration program

#include <chrono>
#include <iostream>
#include <random>
#include <vector>
using namespace std;

struct Complexity {
    static void bubbleSort(vector<int>& arr) {
        if (arr.size() < 2) {
            return;
        }
        int n = static_cast<int>(arr.size());
        int end = n - 1;
        int i = 0;
        while (end > 0) {
            if (arr[i] > arr[i + 1]) {
                swap(arr, i, i + 1);
            }
            if (i < end - 1) {
                ++i;
            } else {
                --end;
                i = 0;
            }
        }
    }

    static void swap(vector<int>& arr, int i, int j) {
        int tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
};

int main() {
    mt19937 rng(static_cast<unsigned>(
        chrono::steady_clock::now().time_since_epoch().count()
    ));

    int n = 10;
    int v = 4;
    vector<int> arr1(n);
    uniform_int_distribution<int> dist(0, v - 1);
    arr1[0] = dist(rng);
    for (int i = 1; i < n; ++i) {
        do {
            arr1[i] = dist(rng);
        } while (arr1[i] == arr1[i - 1]);
    }
    for (int num : arr1) {
        cout << num << ' ';
    }
    cout << '\n';
    cout << "=========" << '\n';

    // C++ 中的动态数组通常用 vector
    // 初始容量和扩容因子可能因实现而异，但均摊复杂度依然可以认为是 O(1)
    vector<int> arr2;
    arr2.push_back(5); // 0
    arr2.push_back(4); // 1
    arr2.push_back(9); // 2
    arr2[1] = 6;
    cout << arr2[1] << '\n';
    cout << "=========" << '\n';

    vector<int> arr = {64, 31, 78, 0, 5, 7, 103};
    Complexity::bubbleSort(arr);
    for (int num : arr) {
        cout << num << ' ';
    }
    cout << '\n';
    cout << "=========" << '\n';

    int N = 200000;
    cout << "测试开始" << '\n';
    auto start = chrono::steady_clock::now();
    for (int i = 1; i <= N; ++i) {
        for (int j = i; j <= N; j += i) {
            // 这两个嵌套 for 循环的流程，时间复杂度为 O(N * logN)
            // 1/1 + 1/2 + 1/3 + ... + 1/n 是调和级数，增长量级为 O(logN)
        }
    }
    auto end = chrono::steady_clock::now();
    cout << "测试结束，运行时间 : "
         << chrono::duration_cast<chrono::milliseconds>(end - start).count()
         << " 毫秒" << '\n';

    cout << "测试开始" << '\n';
    start = chrono::steady_clock::now();
    for (int i = 1; i <= N; ++i) {
        for (int j = i; j <= N; ++j) {
            // 这两个嵌套 for 循环的流程，时间复杂度为 O(N^2)
        }
    }
    end = chrono::steady_clock::now();
    cout << "测试结束，运行时间 : "
         << chrono::duration_cast<chrono::milliseconds>(end - start).count()
         << " 毫秒" << '\n';

    return 0;
}
```
