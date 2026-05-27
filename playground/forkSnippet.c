#include <stdio.h>
#include <unistd.h>

int main() {

    printf("Process... %d\n", getpid());

    fork();

    printf("Process... %d\n", getpid());

    return 0;
}