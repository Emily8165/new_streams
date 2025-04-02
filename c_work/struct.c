#include <stdio.h>
#include <string.h>

struct Player {
    char name[12];
    int score;
};

int main(){

    struct Player player1, player2;
    strcpy(player1.name, "greg");
    player1.score = 4;
    strcpy(player2.name, "anna");
    player2.score = 5;

    printf("%s score: %d\n", player1.name, player1.score);
    printf("%s score: %d\n", player2.name, player2.score);

    return 0;
}