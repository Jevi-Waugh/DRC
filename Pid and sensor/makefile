CC=gcc
OBJ=droid.o main.o
CFLAGS=-Wall
EXEC=droid

$(EXEC): $(OBJ)
	$(CC) $(OBJ) -o $(EXEC)

droid.o: droid.c droid.h
	$(CC) $(CFLAGS) -c droid.c

main.o: main.c droid.h
	$(CC) $(CFLAGS) -c main.c

clean:
	rm -i $(EXEC) $(OBJ)

runval :
	valgrind ./$(EXEC) $(PARAMS)

