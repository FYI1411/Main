#include <stdio.h>
#include <string.h>
#define MAX 100

int inputn(char tenN, int min, int max) {
    int n;
    for (; ; ) {
        printf("%d < %c < %d? ", min, tenN, max); scanf("%d", &n);
        if (min <= n <= max) {break;}
    }
    return n;
}

// tim kiem tuyen tinh / linear search
int tktt(int a[], int n, int x) {
    for (int i = 0; i < 7; i++) {
        if (a[i] == n) {return i;}
    } return -1;
}

// tim kiem nhi phan /binary search
int tknp(int a[], int n, int x) {
int left = 0;
int right = n - 1;
int mid = (right - left) / 2;
for (; ; ) {
    if (x < a[mid]) {
        right = mid - 1;
    } else { left = mid - 1;}
    mid = (right - left) / 2;
    if (left > right) {return mid;}
} return -1;
}

int main()  {
    int a[7] = {1, 2, 6, 26, 28, 37, 40};
    printf("%d", tknp(a, 7, -7));
    return 0;
}