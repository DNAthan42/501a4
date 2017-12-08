#include <stdio.h>
void convolve(float x[], int N, float h[], int M, float y[], int P);

void convolve(float x[], int N, float h[], int M, float y[], int P){

    int n,m;
    //y is cleared in calling code always (via python instantiation)

    for (n = 0; n < N; n++){
        if (n % 1000 == 0) {
            printf("n: %d\n", n);
        }
        for (m = 0; m < M; m++){
            y[n+m] += x[n] * h[n];
        }
    }
}