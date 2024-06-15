#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "board.h"
#include "tree.h"

int main(int argc, char **argv) {
    const uint8_t BOARD_SIZE = 4;
    char *letters[] = {
        "u", "n", "r", "e",
        "qu","n", "i", "l",
        "i", "s", "h", "a",
        "s", "e", "l", "b"
    };
    char **cell_letters = malloc(BOARD_SIZE * sizeof(struct BoardCell*));

    struct BoardCell **cells = malloc(sizeof(struct BoardCell*) * BOARD_SIZE * BOARD_SIZE);
    for (uint8_t i = 0; i < BOARD_SIZE * BOARD_SIZE; i++) {
        cells[i] = create_board_cell(letters[i], (int)(i / BOARD_SIZE), i % BOARD_SIZE);
        print_boardcell(cells[i]);
    }

    Board board = { .height = 4, .width = 4, .cells = cells };
    print_board(&board);
    free(cell_letters);

    struct WordNode *root = malloc(sizeof(struct WordNode) + sizeof(struct WordNode*));
    init_wordnode(root, false, cells[0], NULL, NULL, 0);
    add_child_node(&root, cells[5], false);
    add_child_node(&root, cells[4], false);
    print_wordnode(root);
    print_wordnode_path(root->children[0]);

    free_wordnode_children(root);
    free(root);
    for (uint8_t i = 0; i < BOARD_SIZE * BOARD_SIZE; i++) {
        free(cells[i]);
    }
    free(cells);
}
