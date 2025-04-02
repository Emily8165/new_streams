#include <stdio.h>
#include <stdlib.h>


// Goals for this area: 
// Learn Basic Syntax and Compilation

// Variables, data types, and operators
// Control structures (if, switch, loops)
// Functions and scope
// Practice: Write a basic calculator program.


// CALCULATOR
// Must:
//      Be able to do basic maths, +, /, -, *
//      Be able to take user input 
// Cans:
//      Do muliple operators one after the other
//      
// Won'ts:
//      Do complex operators outside of +, /, *, -
//      Have a memory of previous operators once the program has been terminated. 
//      size of numbers is less then 32 bit -2,147,483,648 to 2,147,483,647 (232)




int get_number() {
    // returns the int value by the user
    int num;
    printf("give me a number: ");
    scanf("%d", &num);
    return num;
}

char get_operator() {
    // returns the str operator value given by the user
    char operator;
    printf("give me an operator: ");
    scanf(" %c", &operator);
    return operator;
}

void calculator() {
    // initalise variables:
    // match variables to corrisponding functions
    int result = 0;
    int num1 = get_number();
    int num2 = get_number();
    char operator = get_operator();
    // match operator to operation
    switch (operator) {
        case '+':
            result = num1 + num2;
            break;
        case '-':
            result = num1 - num2;
            break;
        case '*':
            result = num1 * num2;
            break;
        case '/':
            result = num1 / num2;
            break;
    }
    printf("answer: %d\n", result);
}

char* is_pass_or_fail(int score){
    if (score > 50){
        printf("pass");
    } else {
        printf("fail");
    }
}

int main() {
    // inialises while loop to continuously ask for operators:
    // while(1) {
    //     printf("\nHi, I am a calulator, give me sums to solve: \n");
    //     calculator();
    // }
    is_pass_or_fail();
    return 0; 
}