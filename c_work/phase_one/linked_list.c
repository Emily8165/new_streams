#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
};

struct Node *head(){
    struct Node * newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = 2;
    newNode->next = (struct Node*)malloc(sizeof(struct Node));
    return newNode;
}

struct Node *insert(int position, int data){
    struct Node * newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = (struct Node*)malloc(sizeof(struct Node));
    return newNode;
}

struct Node *append(int position) {
    struct Node * newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = position += 1;
    newNode->next = NULL;
    return newNode;
}

int main() {
    struct Node *n1 = head();
    head()->next = append(head()->data);
    struct Node *temp = n1;
    for (int i = 0; i < 2; i++) {
        printf("Node: %d\n", temp->data);
        temp = temp->next;
    }
    return 0;
}