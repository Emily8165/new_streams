#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int NUM_OF_NODES;

typedef struct Node {
    struct Node *prev;
    int id;
    char *name;
    struct Node *next;
} Node;


Node *createNodes(int numOfNodes) {
    if (numOfNodes <= 0) return NULL;

    // create innital memory space for the nodes. 
    Node *nodes = malloc(numOfNodes * sizeof(Node));


    if (nodes == NULL) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    // create head
    nodes[0].prev = NULL;
    nodes[0].id = 0;
    nodes[0].next = &nodes[1];
    // add body / tail
    for (int i = 1; i <= numOfNodes; i++){
            
        nodes[i].prev = &nodes[i - 1];
        nodes[i].id = i;
        if (i == numOfNodes){
        nodes[numOfNodes].next = NULL;
        } else {
        nodes[i].next = &nodes[i + 1];
        }
    }
    
    // returns the address where the nodes are kept.
    return nodes;
}

Node *view(Node *nodes){
    for (int i = 0; i < NUM_OF_NODES + 1; i++){
        if (nodes[i].prev == NULL){
            printf("Head: N, ID: %d, Content: %s, Tail: %d\n", nodes[i].id, nodes[i].name, nodes[i].next->id);
            continue;
        } else if (nodes[i].next == NULL){
            printf("Head: %d, ID: %d, Content: %s, Tail: N\n", nodes[i].prev->id, nodes[i].id, nodes[i].name);
            break;;
        }
        printf("Head: %d, ID: %d, Content: %s, Tail: %d\n", nodes[i].prev->id, nodes[i].id, nodes[i].name, nodes[i].next->id);
    }
    return nodes;
}

Node *insert(Node *nodes) {
    int position;
    printf("where do you want the new node to be located?: \n");
    scanf(" %d", &position);
    NUM_OF_NODES++;
    // create new node
    Node *newNode=(Node *)realloc(nodes, sizeof(Node) * NUM_OF_NODES);
    if (newNode == NULL) {
        printf("Memory allocation failed!\n");
        return nodes;  // Return the old pointer (though it's risky)
    }
    // assign values to new node
    
    newNode[position].prev = &nodes[position-1];
    newNode[position].id = position;
    newNode[position].next = &nodes[position+1];

    while (newNode[position].next != NULL) {
        nodes[position].prev = &newNode[position];
        nodes[position].id += 1;
        nodes[position].next = &newNode[position +1];
        newNode = nodes[position].next;
    }
    return newNode;
}

Node *append(Node *nodes) {
    NUM_OF_NODES++;
    // create new node
    Node *newNode=(Node *)realloc(nodes, sizeof(Node) * NUM_OF_NODES);
    if (newNode == NULL) {
        printf("Memory allocation failed!\n");
        return nodes;  // Return the old pointer (though it's risky)
    }
    // assign values to new node
    
    newNode[NUM_OF_NODES].prev = &nodes[NUM_OF_NODES-1];
    newNode[NUM_OF_NODES].id = NUM_OF_NODES;
    newNode[NUM_OF_NODES].next = NULL;

    // point previous last node to new node 
    nodes[NUM_OF_NODES-1].next = &newNode[NUM_OF_NODES];
    return newNode;
}

Node *pop(Node *nodes) {
    Node *toDelete = &nodes[NUM_OF_NODES];
    toDelete->prev->next = NULL;
    toDelete->prev = NULL;
    free(toDelete);
    NUM_OF_NODES--;
    nodes = realloc(nodes, NUM_OF_NODES * sizeof(nodes));
    return nodes;
}

Node *delete(Node *nodes) {
    int position;
    printf("Which object do you want to delete?: ");
    scanf(" %d", &position);

    Node *toDelete = &nodes[position];

    if (toDelete->prev != NULL){
        toDelete->prev->next = toDelete->next;
    }
    if (toDelete->next != NULL){
        toDelete->next->prev = toDelete->prev;
    }
    free(toDelete);

    for (int i = position; i < NUM_OF_NODES; i++) {
        nodes[i] = nodes[i + 1];
    }

    NUM_OF_NODES--;

    nodes = realloc(nodes, NUM_OF_NODES * sizeof(nodes));
    return nodes;
}

int main(){
    // create nodes:
    printf("how many nodes do you want?:\n");
    scanf(" %d", &NUM_OF_NODES);
    Node *temp = createNodes(NUM_OF_NODES);
    int upDown;
    while (1){
        printf("AT NODE: %d\n", temp->id);
        printf("0 = DOWN\n1 = UP\n2 = APPEND\n3 = POP\n4 = VIEW\n5 = INSERT\n6 = DELETE\n7 = FREE\n");
        scanf(" %d", &upDown);
        switch(upDown){
            case 0:
                if (temp->next == NULL){
                    printf("already at the tail!\n");
                } else {
                    temp = temp->next;
                }
                break;
            case 1: 
                if (temp->prev == NULL){
                    printf("Already at head!\n");
                } else {
                    temp = temp->prev;
                }
                break;
            case 2: 
                append(temp);
                break;
            case 3:
                pop(temp);
                break;
            case 4: 
                view(temp);
                break;
            case 5: 
                insert(temp);
                break;
            case 6:
                delete(temp);
                break;
            case 7:
                free(temp);
                return 0;
            }
    }
    return 0;
}