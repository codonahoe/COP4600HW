#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hashdb.h"
#include "rwlocks.h"

#define MAX_COMMAND_LEN 100
#define MAX_NAME_LEN 50

void parse_command(char *line, char *command, char *param1, char *param2);
void execute_command(char *command, char *param1, char *param2);

int main() {

    FILE *file = fopen("commands.txt", "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening file.\n");
        return 1;
    }

    char line[MAX_COMMAND_LEN];

    // Read and process each command from the file
    while (fgets(line, sizeof(line), file) != NULL) {
        char command[MAX_COMMAND_LEN];
        char param1[MAX_NAME_LEN];
        char param2[MAX_NAME_LEN];

        // Parse the command and parameters
        parse_command(line, command, param1, param2);

        // Execute the command
        execute_command(command, param1, param2);
    }

    // Close the file
    fclose(file);

    return 0;
}

void parse_command(char *line, char *command, char *param1, char *param2) {
    // Extract command and parameters from the input string
    sscanf(line, "%[^,],%[^,],%s", command, param1, param2);
}

void execute_command(char *command, char *param1, char *param2) {
    if (strcmp(command, "threads") == 0) {
        // Handle threads command
        // Not implemented in this basic outline
    } else if (strcmp(command, "insert") == 0) {
        // Handle insert command
        // Not implemented in this basic outline
    } else if (strcmp(command, "delete") == 0) {
        // Handle delete command
        // Not implemented in this basic outline
    } else if (strcmp(command, "search") == 0) {
        search_record(param1);
    } else if (strcmp(command, "print") == 0) {
        // Handle print command
        // Not implemented in this basic outline
    } else {
        // Invalid command
        printf("Invalid command: %s\n", command);
    }
}