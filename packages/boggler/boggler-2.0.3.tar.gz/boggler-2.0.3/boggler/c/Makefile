CC = gcc
CFLAGS = -Wall -Werror -std=gnu17 -g3
OBJS = boggler.o

all: $(OBJS)
	$(CC) $(OBJS) -o boggler

boggler.o: boggler.c board.h tree.h
	$(CC) $(CFLAGS) -c boggler.c

clean:
	rm -f *~ *.o boggler
