#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


int SIZE;
typedef struct Cell
{
    int x, y;
    char *state;
    struct Cell *north, *south, *east, *west;
} Cell;

int getStart(int limit) {
    time_t seconds;
    seconds = time(NULL);
    int result = seconds % limit;
    return result;
}

Cell *generateMase() {
    int totalSize = SIZE * SIZE;
    Cell *cells = (Cell *)malloc(totalSize * sizeof(Cell)); 
    if (cells == NULL) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    int bod = totalSize - (SIZE * 4);
    int *edges = (int *)malloc((SIZE * 4) * sizeof(int));
    int *body = (int *)malloc(bod * sizeof(int));
    int b = 0;
    int e = 0;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++){
            int cell = i + j * SIZE;
            cells[cell].x = i;
            cells[cell].y = j;
            // southern edge
            if (j == 0){
                cells[cell].south = NULL;
                cells[cell].state = "# ";
                edges[e] = cell;
                e++;
                continue;
            }
            // eastern edge
            if (i == 0){
                cells[cell].east = NULL;
                cells[cell].state = "# ";
                edges[e] = cell;
                e++;
                continue;
            }
            // western edge
            if (i == SIZE-1) {
                cells[cell].west = NULL;
                cells[cell].state = "# ";
                edges[e] = cell;
                e++;
                continue;
            }
            // north edge
            if (j == SIZE - 1) {
                cells[cell].north = NULL;
                cells[cell].state = "# ";
                edges[e] = cell;
                e++;
                continue;
            }
            cells[cell].north = cells[cell -10].north;
            cells[cell].west = cells[cell -1].west;
            cells[cell].east = cells[cell + 1].east;
            cells[cell].south = cells[cell +10].south;
            cells[cell].state = ". ";
            body[b] = cell;
            b++;
        }
    }

    // add start and end
    int s = getStart(e);
    srand(time(NULL));
    int end = rand() % e;
    // make sure they are not in the corner
    while (s == 0 || s == SIZE || s == (SIZE * SIZE) - SIZE + 1 || s == SIZE * SIZE)
        {
            s = getStart(e); 
        }
    while (e == 0 || e == SIZE || e == (SIZE * SIZE) - SIZE +1 || e == SIZE * SIZE)
        {
            end = rand() % e; 
        }
    cells[edges[s]].state = "S ";
    cells[edges[end]].state = "E ";

    // add walls
    int o = 0;
    while (o < SIZE * 2){
        int r = rand() % b;
        cells[body[r]].state = "# ";

        // make sure wall is not infront of start or end
        if (strcmp(cells[body[r]].state, "S ") == 0 || strcmp(cells[body[r]].state, "E ") == 0){
            if (cells[body[r]].north == NULL){
                cells[body[r]].north->south->state = ". ";
                continue;
            } else if (cells[body[r]].south == NULL) {
                cells[body[r]].south->north->state = ". ";
                continue;
            } else if (cells[body[r]].east == NULL) {
                cells[body[r]].east->west->state = ". ";
                continue;
            } else if (cells[body[r]].west == NULL) {
                cells[body[r]].west->east->state = ". ";
                continue;
            }
        }
        o++;
    }
    return cells;
}

int main() {
    printf("How big do you want the maze to be?: ");
    scanf(" %d", &SIZE);
    Cell *maze = generateMase();
    for (int i = 0; i < (SIZE * SIZE); i++) {
        if (i % SIZE == 0){
            printf("\n");
        }
        printf("%s", maze[i].state);
    }
    free(maze);
    return 0;
}