#include <stdio.h>
#include <unistd.h>
#include "helpers/helperString.h"
#include "helpers/helperInput.h"

int main()
{
    char name[100];
    int age;

    printf("Enter your name: ");
    helperString(name, 100);

    printf("Enter your age: ");
    age = helperInt();

    printf("Your name is %s and your age is %d.\n", name, age);

    for(int x = 1; x <= age; x++) {
        printf("%d\n", x);
        sleep(1);
    }

    return 0;
}