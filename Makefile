# Compiler
CC = gcc

# Compiler flags
CFLAGS = -Wall -Wextra -std=c99

# Linker flags
LDFLAGS = -lpthread

# Source files
SRCS = chash.c hashdb.c rwlocks.c

# Object files
OBJS = $(SRCS:.c=.o)

# Executable name
TARGET = chash

# Default target
all: $(TARGET)

# Compile source files to object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Link object files to create executable
$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) $(LDFLAGS)

# Clean up
clean:
	rm -f $(OBJS) $(TARGET)
