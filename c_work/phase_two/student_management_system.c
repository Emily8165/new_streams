#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int numberOfStudents = 0;
int MAX_STUDENTS = 100;

typedef struct Student {
    char name[50];
    int age;
    int year;
    float score;
    char grade;
    int id;
} Student;

char calculateGrade(int score) {
    if (score < 0 || score > 101){
        printf("Invalid!");
        return 1;
    }
    else if (score >= 80){
        return 'A';
    } else if (score >= 70){
        return 'B';
    } else if (score >= 60) {
        return 'C';
    } else if (score >= 50) {
        return 'D';
    } else if (score >= 40) {
        return 'E';
    } else {
        return 'F';
    }
}

int calculateYear(int age) {
    if (age < 4 || age > 18){
        printf("Invalid!");
        return 1;
    }
    return age - 5;
}

void createStudent() {
    Student *student = &student[numberOfStudents];
    student->id = numberOfStudents + 1;
    printf("give me the student's name: ");
    scanf("%s", student->name);
    printf("give me the student's age: ");
    scanf("%d", &student->age);
    student->year = calculateYear(student->age);
    printf("give me the students score: ");
    scanf("%f", &student->score);
    student->grade = calculateGrade(student->score);
    student->id = numberOfStudents;
    printf("%d | %s | %c | %f | %c\n", student->id, student->name, student->grade, student->score, student->grade);
    numberOfStudents++;
}

void viewStudents(Student *student) {
    printf("Name | Age | Year | Score | Grade | Id \n");
    for (int i = 0; i < numberOfStudents; i++){
        if (student[i].id > 0){
            printf("%s | %d | %d | %f | %c | %d\n", student[i].name, student[i].age, student[i].year, student[i].score, student[i].grade, student[i].id);
        }
    }
}

void searchStudents(Student *student, int id) {
    printf("Name | Age | Year | Score | Grade | Id \n");
    if (id < 0 || id > numberOfStudents){
        printf("%s | %d | %d | %f | %c | %d\n", student[id].name, student[id].age, student[id].year, student[id].score, student[id].grade, student[id].id);
    } else {
        printf("I cannot find that student\n");
    }
}

void updateStudent(Student *student) {
    int id;
    char option;
    printf("which student do you want to update?: \n");
    viewStudents(student);
    scanf("%d", &id);
    printf("%s | %d | %d | %f | %c | %d\n", student[id].name, student[id].age, student[id].year, student[id].score, student[id].grade, student[id].id);
    printf("What do you want to update from %d\n", student[id].id);
    printf("A. Name, B. Age, C. Score\n");
    scanf(" %c", &option);
    switch (option){
        case 'A':
            printf("Give me the new name: \n");
            scanf("%s", student[id].name);
            break;
        case 'B':
            printf("Give me the new age: \n");
            scanf("%d", &student[id].age);
            student[id].year = calculateYear(student[id].age);
            break;
        case 'C':
            printf("Give me the new score: \n");
            scanf("%f", &student[id].score);
            student[id].grade = calculateGrade(student[id].score);
            break;
    }
    printf("update!\n");
    searchStudents(student, id);
}

void deleteStudent(Student *student) {
    int id;
    printf("which student do you want to delete?: ");
    viewStudents(student);
    scanf("%d", &id);
    student[id].id = -1;
    for (int i = id -1; i < numberOfStudents - id; i++){
        student[i].id = student[i].id -1;
    }
    numberOfStudents--;
}

int main() {
    // initalise main loop with x, id is used for searching student ids, student is initalised here:
    int x = 1;
    int id;
    Student *student = (Student *)malloc(MAX_STUDENTS * sizeof(Student));
    while (x == 1) {
        // options used to direct user activities. 
        char options;
        printf("Welcome to the student database, what would you like to do?: \n");
        printf("A. Create a student\n");
        printf("B. View all students\n");
        printf("C. Update student information\n");
        printf("D. Delete a student\n");
        printf("E. Search for a student by their ID\n");
        scanf(" %c", &options);

        switch (options)
        {
        case 'A':
            createStudent();
            break;
        case 'B':
            viewStudents(student);
            break;
        case 'C':
            updateStudent(student);
            break;
        case 'D':
            deleteStudent(student);
            break;
        case 'E':
            printf("Which student are you looking for?: ");
            viewStudents(student);
            scanf("%d", &id);
            searchStudents(student, id);
            break;
        case 'F':
            x = 0;
            free(student);
            break;
        default:
            printf("That is not a valid input");
            break;
        }
    }
    printf("Thank you please come again");
    return 0;
}