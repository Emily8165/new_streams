#include <stdio.h>
#include <string.h>
#include <stdlib.h>
// Write a C program that:

// Asks the user how many integers they want to store.
// Dynamically allocates memory for that many integers using malloc().
// Allows the user to input values into the allocated array.
// Asks the user if they want to add more integers.
// If yes, use realloc() to increase the size and allow more input.
// If no, print all stored values and free the allocated memory.

int main() {
    int *arr;
    int boolean;
    int size, new_size, i;
    printf("How many integers do you want to store?: ");
    scanf("%d", &size);
    arr = (int * )malloc(size * sizeof(int));
    if (arr == NULL){
       printf("memory allocation failed, please restart program\n");
       return 1; 
    }
    for (i = 0; i < size; i++){
        printf("give me an int (ints remaining: %d)", size - i);
        scanf("%d", &arr[i]);
    }
    printf("I have assigned space for %d integers, do you want me to store any more?: ", size);
    scanf("%d", &new_size);
    int final_size = new_size + size;
    arr = (int *)realloc(arr, final_size);
    if (arr == NULL){
        printf("memory allocation failed, please restart program\n");
        return 1; 
    }
    for (i = 0; i < new_size; i++){
        printf("give me an int (ints remaining: %d)", new_size - i);
        scanf("%d", &arr[size + i]);
    }
    printf("Here is your array: ");
    for (i = 0; i < final_size; i++){
        printf("%d", arr[i]);
    }
    free(arr);
    return 0;
}