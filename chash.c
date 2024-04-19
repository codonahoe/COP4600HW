#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hashdb.h"
#include "rwlocks.h"

#define MAX_COMMAND_LEN 100
#define MAX_NAME_LEN 50

void parse_command(char *line, char *command, char *param1, char *param2);
void execute_command(char *command, char *param1, char *param2, FILE *output_file);

int main() {

    FILE *file = fopen("commands.txt", "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening file.\n");
        return 1;
    }
    // Create output file
    FILE *output_file = fopen("output.txt", "w");   

    char line[MAX_COMMAND_LEN];

    // Read and process each command from the file
    while (fgets(line, sizeof(line), file) != NULL) {
        char command[MAX_COMMAND_LEN];
        char param1[MAX_NAME_LEN];
        char param2[MAX_NAME_LEN];

        // Parse the command and parameters
        parse_command(line, command, param1, param2);

        // Execute the command
        execute_command(command, param1, param2, output_file);
    }

    // Final print
    print_counts(output_file);
    print_all(output_file);

    // Close the file
    fclose(file);
    // Close output file
    fclose(output_file);

    return 0;
}

void parse_command(char *line, char *command, char *param1, char *param2) {
    // Extract command and parameters from the input string
    sscanf(line, "%[^,],%[^,],%s", command, param1, param2);
}

void execute_command(char *command, char *param1, char *param2, FILE *output_file) {
    if (strcmp(command, "threads") == 0) {
        // Threads command
        int threads = thread_count(param1);
        printf("Running %d threads\n", threads);
        fprintf(output_file, "Running %d threads\n", threads);
    } else if (strcmp(command, "insert") == 0) {
        // Insert command
        insert_record(param1, atoi(param2), output_file);
    } else if (strcmp(command, "delete") == 0) {
        // Delete command
        delete_record(param1, output_file);
    } else if (strcmp(command, "search") == 0) {
        // Search command
        search_record(param1, output_file);
    } else if (strcmp(command, "print") == 0) {
        // Print command
        print_all(output_file);
    } else {
        // Invalid command
        printf("Invalid command: %s\n", command);
        fprintf(output_file, "Invalid command: %s\n", command);
    }
}
