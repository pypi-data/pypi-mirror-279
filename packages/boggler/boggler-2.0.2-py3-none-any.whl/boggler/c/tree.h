#ifndef WORD_TREE
#define WORD_TREE

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "board.h"

struct WordNode {
    bool is_word;
    struct BoardCell *cell;
    struct WordNode *parent;
    uint8_t child_cnt;
    struct WordNode *children[];
};

struct WordTree {
    char *alphabet;
    struct WordNode *root;
};

void *init_wordnode(struct WordNode *n, bool is_word, struct BoardCell *cell,
    struct WordNode *parent, struct WordNode *children[], uint8_t child_cnt) {
    n->is_word = is_word;
    n->cell = cell;
    n->parent = parent;
    if (children != NULL) {
        for (uint8_t i = 0; i < child_cnt; i++) {
            n->children[i] = children[i];
        }
    }
    n->child_cnt = child_cnt;

    return n;
}
void *print_wordnode(struct WordNode *n) {
    if (n == NULL) {
        return NULL;
    }
    printf("%3s | (%d,%d) | %3d\n", n->cell->letters, n->cell->row, n->cell->col, n->child_cnt);
    return n;
}

void *print_wordnode_path(struct WordNode *n) {
    if (n == NULL) {
        return NULL;
    }
    struct WordNode *node = n;

    // Print letters from leaf to root
    do {
        printf("%s < ", node->cell->letters);
        node = node->parent;
    } while(node != NULL);
    puts("ROOT");
    return node;
}

struct WordNode *add_child_node(struct WordNode **parent, struct BoardCell *cell, bool is_word) {
    *parent = realloc(*parent, sizeof(struct WordNode) + sizeof(struct WordNode) * ((*parent)->child_cnt + 1));
    (*parent)->children[(*parent)->child_cnt] = malloc(sizeof(struct WordNode));
    init_wordnode((*parent)->children[(*parent)->child_cnt], is_word, cell, *parent, NULL, 0);
    (*parent)->child_cnt++;
    return (*parent)->children[(*parent)->child_cnt];
}

void free_wordnode_children(struct WordNode *n) {
    // TODO: recursively free wordnode children
    for (uint8_t i = 0; i < n->child_cnt; i++) {
        free(n->children[i]);
    }
}

void *insert_word(struct WordTree *tree, char *word) {
    // TODO: Traverse tree from tree->root and add nodes needed to complete `word`
    return NULL;
}


int search(struct WordTree *tree, char *word) {
    // TODO: Traverse `tree` node-by-node and return an array of Board paths for `word`
    return 0;
}

#endif /* WORD_TREE */
