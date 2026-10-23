CC ?= gcc
CFLAGS ?= -std=c11 -Wall -Wextra -O2

all: function_table target_tracker

function_table: function_table.c
	$(CC) $(CFLAGS) -o $@ $< -lm

target_tracker: target_tracker.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f function_table target_tracker

.PHONY: all clean
