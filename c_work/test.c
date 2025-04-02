#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char *data;
    int size = 1;
    data = malloc(size);
    printf("give data\n");
    
    while (1) {
        scanf(" %s", data);
        if (strcmp(&data[size -1], "Q")){
            break;
        }
        size += 1;
        data = realloc(data, size);
    }
    printf("%s", data);
}