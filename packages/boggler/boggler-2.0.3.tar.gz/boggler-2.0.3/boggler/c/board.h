#ifndef BOGGLER_UTILS
#define BOGGLER_UTILS

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

/* Board is structured like so when referencing cells
 *      x ->
 *    +---+---+---+---+
 *  y |0,0|1,0|2,0|3,0| -+
 *  | |---------------|  |
 *  v |0,1|1,1|2,1|3,1|  |
 *    |---------------|  | height
 *    |0,2|1,2|2,2|3,2|  |
 *    |---------------|  |
 *    |0,3|1,3|2,3|3,3| -+
 *    +---+---+---+---+
 *     |             |
 *     +-------------+
 *          width
 *
 *    Vec2 = (x, y) = (col, row)
 */

struct BoardCell {
    char *letters;
    uint8_t row;
    uint8_t col;
    struct BoardCell **adjacent_cells;
    uint8_t adjacent_cnt;
};

typedef struct Vec2 {
    uint8_t row;
    uint8_t col;
} Vec2;

typedef struct Board {
    /* BoardCells are indexed from top-to-bottom, left-to-right
     * For instance a 3x3 board would have cells ordered like this
     * +---+---+---+
     * | 0 | 1 | 2 |
     * |---+---+---|
     * | 3 | 4 | 5 |
     * |---+---+---|
     * | 6 | 7 | 8 |
     * +---+---+---+
     */
    uint8_t height;
    unsigned short width;
    struct BoardCell **cells;
} Board;

struct BoardCell *create_board_cell(char *letters, uint8_t row, uint8_t col) {
    /* BoardCells are created with 8 adjacent cells since that is the minimum required
     * for centrally placed (not on sides or corners) cells on a board.
     */
    struct BoardCell *cell = malloc(sizeof(struct BoardCell));
    cell->letters = letters;
    cell->row = row;
    cell->col = col;

    return cell;
}

struct BoardCell *get_cell_at(Board *board, Vec2 pos) {
    return board->cells[pos.row * pos.col + pos.col];
}

int print_boardcell(struct BoardCell *c) {
    printf("%3s | (%d,%d)\n", c->letters, c->row, c->col);
    return 0;
}

int print_board(Board *board) {
    uint8_t row_len = (board->width * 4 + 1) * sizeof(char) + 1;
    char *row_delim = malloc(row_len);
    snprintf(row_delim, 2, "%c", '+');
    for (uint8_t i = 0; i < board->width; i++) {
        strcat(row_delim, "----");
    }
    row_delim[strlen(row_delim)-1] = '+';

    for (uint8_t row = 0; row < board->height; row++) {
        printf("%s\n", row_delim);
        for (uint8_t col = 0; col < board->width; col++) {
            printf("|%2s ", board->cells[(row * board->width) + col]->letters);
        }
        puts("|");
    }
    printf("%s\n", row_delim);

    free(row_delim);

    return 0;
}

void free_board(Board *b) {
    if (b != NULL) {
        for (uint8_t i = 0; i < b->width * b->height; i++) {
            free(b->cells[i]);
            b->cells[i] = NULL;
        }
        free(b->cells);
        free(b);
    }
}
//Vec2[] get_adjacent_indexes(uint8_t board_size, Vec2 pos) {
//    // Calculate total possible number of adjacent cells
//    uint16_t = total_adj_cell_cnt = ((board-size-2) * (board-size-2) * 8) + ((board-size-2) * 4 * 5) + (4 * 3);
//
//    Vec2[] indexes = malloc(8 * sizeof(Vec2));
//    uint16_t i = 0;
//    if (pos.row > 0) {
//        indexes[i].append((row-1, col)) // up
//        if col > 0:
//            indexes.append((row-1, col-1)) // up-left
//        if col < self.width - 1:
//            indexes.append((row-1, col+1)) // up-right
//    }
//    if row < self.height - 1:
//        indexes.append((row+1, col)) // down
//        if col > 0:
//            indexes.append((row+1, col-1)) // down-left
//        if col < self.width - 1:
//            indexes.append((row+1, col+1)) // down-right
//    if col > 0:
//        indexes.append((row, col-1)) // left
//    if col < self.width - 1:
//        indexes.append((row, col+1)) // right
//
//    if (i != 8) {
//        indexes = realloc(i * sizeof(Vec2));
//    }
//    return indexes
//}

#endif
