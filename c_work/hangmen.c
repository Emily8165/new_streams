#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

int get_psudo_random_number() {
	time_t seconds;

	seconds = time(NULL);
	int number = seconds % 6;
	return number;
}

void get_main_word(int number, char *myStr){
	char word[6][6] = {"About", "Alert", "Beach", "Brand", "Catch", "Crime"};
	printf("%d\n", number);
	printf("This is the word %s\nGive me a new word: ", word[number]);
	for (int i = 0; i < 6; i++) {
        myStr[i] = word[number][i];
    }
	printf("%s", myStr);
}

void red () {
  printf("\033[1;31m");
}

void green() {
	printf("\033[1;32m");
}

void yellow() {
  printf("\033[1;33m");
}

void reset () {
  printf("\033[0m");
}

char get_letter(char let[1]) {
	char letter[1];
	fgets(letter, sizeof(letter), stdin);
	printf("%s", letter);
	let = letter;
	return *let;
}

// int main1() {
// 	// Getting main word
// 	int my_num = get_psudo_random_number();
// 	char mainWord[6];
// 	get_main_word(my_num, mainWord);

// 	// initialise game:
// 	int x = 0;
// 	while (x == 0){
// 		// user inputs
// 		get_letter()

// 		char result[6] = {'_', '_', '_', '_', '_', '\0'};
// 		for (int i = 0; i < 6; i++) {
// 			if (strcmp(&mainWord[i], &letter) == 0) {
// 				result[i] = letter;
// 			}
// 		}
// 		for (int j = 0; j < 6; j++) {
// 			printf("%c", result[j]);
// 		}
// 	}
// 		return 0;
// 	}
