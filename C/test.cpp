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

void inputInts(int a[], int n) {
    for (int i = 0; i < n; i++) {
        for (; ; ) {
            printf("a[%d] | (a[i] > 0) ? ", i); scanf("%d", &a[i]);
            if (a[i] > 0) {break;}
        }
    }
}

void printInts(int a[], int n) {
    for (int i = 0; i < n; i++) {printf("%d ", a[i]);}
}

void writeFile(int a[], int n) {
    FILE *f = fopen("test.txt", "w");
    fprintf(f, "%d\n", n);
    for (int i = 0; i < n; i++) {fprintf(f, "%d ", a[i]);}
    fclose(f);
}

void readfile(int a[], int n) {
    FILE *f = fopen("test.txt", "r");
    fscanf(f, "%d", &n);
    for (int i = 0; i < n; i++) {fscanf(f, "%d", &a[i]);}
    fclose(f);
}

typedef struct item {
    float scale;
    char name[10];
} it;

void input1Item(it &y) {
    printf("scale? "); scanf("%f", &y.scale); fflush(stdin);
    printf("name? "); gets(y.name); fflush(stdin);
}
void print1Item(it y) {
    printf("scale: %f\n", y.scale);
    puts(y.name);
}

void inputItems(it a[], int n) {
    printf("Input items:\n");
    for (int i = 0; i < n; i++) {
        printf("a[%d]:\n", i);
        input1Item(a[i]);
    }
}

void printItems(it a[], int n) {
    printf("List of items:\n");
    for (int i = 0; i < n; i++) {
        printf("a[%d]:\n", i);
        print1Item(a[i]);
    }
}

int main()  {
    int a[MAX], b[MAX];
    it c[MAX];
    int n = inputn('n', 5, MAX); inputInts(a, n);
    writeFile(a, n); readfile(b, n);
    printf("\nDay so thuc la: "); printInts(b, n); printf("\n");
    n = inputn('n', 5, MAX); inputItems(c, n); printItems(c, n);
    return 0;
}