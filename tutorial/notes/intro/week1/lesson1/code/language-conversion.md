# Language Conversion C++ 译写

> [返回课程 01 正文](../content.md)

- 题目出处：`LeetCode 912. Sort an Array`
- 说明：本页直接保存并展示课程使用的 C++ 代码

## 代码

```cpp
// Lesson 1 code translation
// Source class: src/class001/LanguageConversion.java
// Problem source: LeetCode 912. Sort an Array

#include <algorithm>
#include <chrono>
#include <random>
#include <vector>
using namespace std;

struct LanguageConversion {
    static constexpr int MAXN = 50001;
    inline static vector<int> help = vector<int>(MAXN);
    inline static int first = 0;
    inline static int last = 0;
    inline static mt19937 rng(
        static_cast<unsigned>(chrono::steady_clock::now().time_since_epoch().count())
    );

    static vector<int> sortArray(vector<int>& nums) {
        if (nums.size() > 1) {
            mergeSort(nums);
        }
        return nums;
    }

    // 以下是归并排序
    static void mergeSort(vector<int>& arr) {
        int n = static_cast<int>(arr.size());
        for (int l, m, r, step = 1; step < n; step <<= 1) {
            l = 0;
            while (l < n) {
                m = l + step - 1;
                if (m + 1 >= n) {
                    break;
                }
                r = min(l + (step << 1) - 1, n - 1);
                merge(arr, l, m, r);
                l = r + 1;
            }
        }
    }

    static void merge(vector<int>& nums, int l, int m, int r) {
        int p1 = l;
        int p2 = m + 1;
        int i = l;
        while (p1 <= m && p2 <= r) {
            help[i++] = nums[p1] <= nums[p2] ? nums[p1++] : nums[p2++];
        }
        while (p1 <= m) {
            help[i++] = nums[p1++];
        }
        while (p2 <= r) {
            help[i++] = nums[p2++];
        }
        for (i = l; i <= r; ++i) {
            nums[i] = help[i];
        }
    }

    // 以下是随机快速排序
    static void quickSort(vector<int>& arr) {
        sort(arr, 0, static_cast<int>(arr.size()) - 1);
    }

    static void sort(vector<int>& arr, int l, int r) {
        if (l >= r) {
            return;
        }
        uniform_int_distribution<int> dist(l, r);
        int x = arr[dist(rng)];
        partition(arr, l, r, x);
        int left = first;
        int right = last;
        sort(arr, l, left - 1);
        sort(arr, right + 1, r);
    }

    static void partition(vector<int>& nums, int l, int r, int x) {
        first = l;
        last = r;
        int i = l;
        while (i <= last) {
            if (nums[i] == x) {
                ++i;
            } else if (nums[i] < x) {
                swap(nums, first++, i++);
            } else {
                swap(nums, i, last--);
            }
        }
    }

    static void swap(vector<int>& arr, int i, int j) {
        int tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }

    // 以下是堆排序
    static void heapSort(vector<int>& nums) {
        int n = static_cast<int>(nums.size());
        for (int i = n - 1; i >= 0; --i) {
            heapify(nums, i, n);
        }
        while (n > 1) {
            swap(nums, 0, --n);
            heapify(nums, 0, n);
        }
    }

    // 这个方法虽然堆排序用不上，但是堆结构里是重要方法，所以这里保留
    // 后面的课会讲
    static void heapInsert(vector<int>& nums, int i) {
        while (nums[i] > nums[(i - 1) / 2]) {
            swap(nums, i, (i - 1) / 2);
            i = (i - 1) / 2;
        }
    }

    static void heapify(vector<int>& nums, int i, int s) {
        int l = i * 2 + 1;
        while (l < s) {
            int best = l + 1 < s && nums[l + 1] > nums[l] ? l + 1 : l;
            best = nums[best] > nums[i] ? best : i;
            if (best == i) {
                break;
            }
            swap(nums, best, i);
            i = best;
            l = i * 2 + 1;
        }
    }
};
```
