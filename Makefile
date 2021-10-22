CC=gcc
LIBS=-loqs -lcrypto
CFLAGS=-Wall -Wextra -O3 -Iliboqs/build/include -Lliboqs/build/lib
SOURCES=$(wildcard src/*.c)
OBJECTS=$(patsubst %.c, %.o, $(SOURCES))
EXECUTABLE=gcwr-ake
OUTPUT=build

all: build ake

build:
	mkdir -p $(OUTPUT)

clean:
	rm -rf $(EXECUTABLE) $(OUTPUT)
	find . -name "*~" -exec rm {} \;
	find . -name "*.o" -exec rm {} \;

ake: src/gcwr-ake.c
	$(CC) $(CFLAGS) src/gcwr-ake.c -o $(OUTPUT)/gcwr-ake $(LIBS)
