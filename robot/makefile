C := gcc
CFLAGS := -Wall -pedantic -std=gnu99 -g

TARGETS := start control ultra_sonic

.PHONY: all clean

all: $(TARGETS)

clean:
	rm -f $(TARGETS) *.o

$(TAGETS): %: %.o
	$(CC) $(CFLAGS)   -o $@ $^
