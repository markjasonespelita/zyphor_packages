#include <stdio.h>
#include <unistd.h>

void helperCommand(char *_command, char *_arguments, int size) {
    char *args[] = {_command, _arguments, NULL};
    execv(_command, args);
}