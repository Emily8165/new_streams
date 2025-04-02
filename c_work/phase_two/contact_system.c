#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int numberOfContacts = 0;
int MAX_CONTACTS = 100;

typedef struct Contact {
    int id;
    char name[50];
    char phone[15];
    char email[50];
} Contact;

int phoneValidation(char number[15]) {
    char valid_numbers[10] = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'};
    for (int i = 0; i < sizeof(number); i++) {
        for (int j = 0; j < sizeof(valid_numbers); j++){
            if (strcmp(valid_numbers[j], number[i]) == 0) {
                break;
            }
            if (strcmp(j, '0') == 0 && (strcmp(number[i], valid_numbers[j]) != 0)){
                return 1;
            }
        }
    }
    return 0;
}
int emailValidation(char email[50]){
    char expectedEndput[10] = "@gmail.com";
    int length = strlen(email);
    int start = length - 10;
    if (start < 0){
        return 1;
    }
    for (int i = start; i < length; i++){
        if (strcmp(email[i], expectedEndput[i]) != 0){
            return 1;
        }
    }
    return 0;
};

void addContact(Contact contacts[]) {
    contacts[numberOfContacts].id=numberOfContacts;
    
    // get phone:
    while (getchar() != '\n');
    printf("Give me a phone number: ");
    fgets(contacts->name, sizeof(contacts->name), stdin);
    contacts->name[strcspn(contacts->name, "\n")] = 0; 

    // get name
    char name[50];
    printf("Give me thier name: ");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = 0; 
    strcpy(contacts->name, name);

    // get number
    char number[15];
    printf("Give me their email: ");
    fgets(number, sizeof(number), stdin);
    if (phoneValidation(number) == 1){
        return 1;
    } else {
        strcpy(contacts->phone, number);
    }
    contacts->email[strcspn(contacts->email, "\n")] = 0; 

    printf("ID | NAME | PHONE | EMAIL\n");
    printf("%d | %s | %s | %s\n", contacts->id, contacts->name, contacts->phone, contacts->email);
    numberOfContacts++;
}
void viewContacts(Contact contacts[]){
    for (int i = 0; i < numberOfContacts; i++){
        printf("ID | NAME | PHONE | EMAIL\n");
        printf("%d | %s | %s | %s\n", contacts[i].id, contacts[i].name, contacts[i].phone, contacts[i].email);
    }
}
char findColum(char query[]){
    // if ascii codes say that the query is a number:
    if ((int)query[0] >= 48 || (int)query[0] <= 57){
        printf("%d", (int)query[0]);
        return 'A'; // Phone number
    }
    for (int i = 1; i < strlen(query); i++){
        // if ascii codes say the query contains characturers that are not normal letters e.g @ or .
        if ((int)query[i] < 97 || (int)query[i] > 122) {
            return 'B'; // Email
        }
    }
    // if not number and not email 
    return 'C'; // Name
}
void searchContact(Contact contacts[], char query[]){
    for (int i = 0; i < numberOfContacts; i++) {
        if (strcmp(contacts[i].phone, query) == 0){
            printf("ID | NAME | PHONE | EMAIL\n");
            printf("%d | %s | %s | %s\n", contacts[i].id, contacts[i].name, contacts[i].phone, contacts[i].email);
        } else if (strcmp(contacts[i].name, query) == 0){
            printf("ID | NAME | PHONE | EMAIL\n");
            printf("%d | %s | %s | %s\n", contacts[i].id, contacts[i].name, contacts[i].phone, contacts[i].email);
        } else if (strcmp(contacts[i].email, query) == 0){
            printf("ID | NAME | PHONE | EMAIL\n");
            printf("%d | %s | %s | %s\n", contacts[i].id, contacts[i].name, contacts[i].phone, contacts[i].email);
        }
    }
}
void updateContact(Contact contacts[], char id){
    printf("Which field do you want to update for: \n");
    printf("A: NAME \nB: PHONE \nC: EMAIL\n");
    char field_option;
    scanf(" %c", &field_option);
    switch (field_option){
        case 'A':
            printf("Give me a new name: \n");
            while (getchar() != '\n');
            fgets(contacts[id].name, sizeof(contacts[id].name), stdin);
            contacts[id].name[strcspn(contacts[id].name, "\n")] = 0; 
            break;
        case 'B':
            printf("Give me a new phone: \n");
            while (getchar() != '\n');
            fgets(contacts[id].phone, sizeof(contacts[id].phone), stdin);
            contacts[id].phone[strcspn(contacts[id].phone, "\n")] = 0; 
            break;
        case 'C':
            printf("Give me a new email: \n");
            while (getchar() != '\n');
            fgets(contacts[id].email, sizeof(contacts[id].email), stdin);
            contacts[id].email[strcspn(contacts[id].email, "\n")] = 0; 
            printf("%s\n", contacts[id].email);
            break;
    }
}
void deleteContact(Contact contacts[], int id){
    contacts[id] = contacts[id-1];
}



int main() {
    int x = 1;
    Contact *contact = (Contact *)malloc(MAX_CONTACTS * sizeof(contact));
    int id;
    char *query;
    char option;
    while(x == 1) {
        
        printf("Welcome to the Contact Manager!\nA. Add a new contact\nB. View all contacts\nC. Search for a contact\nD. Update a contact\nE. Delete a contact\nF. Exit\n");
        option = getchar();

        switch(option) {
            case 'A':
                addContact(contact);
                break;
            case 'B':
                viewContacts(contact);
                break;
            case 'C':
                printf("Give me a query: ");
                while (getchar() != '\n');
                fgets(query, sizeof(query), stdin);
                query[strcspn(query, "\n")] = 0; 
                searchContact(contact, query);
                break;
            case 'D':
                printf("Give me an id: ");
                scanf(" %d", &id);
                updateContact(contact, id);
                break;
            case 'E':
                printf("Give me an id: ");
                scanf(" %d", &id);
                deleteContact(contact, id);
                break;
            case 'F':
                printf("thanks for using me!");
                free(contact);
                x = 0;
                break;
        }
    }
    return 0;
}