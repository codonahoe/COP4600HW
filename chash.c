#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include "hashdb.h"
#include "rwlocks.h"
#include "common_threads.h"

#define MAX_COMMAND_LEN 100
#define MAX_NAME_LEN 50

// For threads
typedef struct arg
{
    char command[MAX_COMMAND_LEN];
    char param1[MAX_NAME_LEN];
    char param2[MAX_NAME_LEN];
    FILE *file;
} arg;

void parse_command(char *line, char *command, char *param1, char *param2);
void *execute_command(void *args);

int main() {

    FILE *file = fopen("commands.txt", "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening file.\n");
        return 1;
    }
    // Create output file
    FILE *output_file = fopen("output.txt", "w");   

    char line[MAX_COMMAND_LEN];
    pthread_t* thread_array;
    int threads;

    // Finds thread count on first line
    if (fgets(line, sizeof(line), file))
    {
        char command[MAX_COMMAND_LEN];
        char param1[MAX_NAME_LEN];
        char param2[MAX_NAME_LEN];
        parse_command(line, command, param1, param2);
        if (strcmp(command, "threads") == 0) {
            // Threads command
            threads = thread_count(param1);
            printf("Running %d threads\n", threads);
            fprintf(output_file, "Running %d threads\n", threads);
            // Create array of pthread_t structs
            thread_array = (pthread_t*)malloc((threads) * sizeof(pthread_t));
        }
    }

    int i = 0;
    // Read and process each command from the file
    while (fgets(line, sizeof(line), file) != NULL) {
        char command[MAX_COMMAND_LEN];
        char param1[MAX_NAME_LEN];
        char param2[MAX_NAME_LEN];
        // Parse the command and parameters
        parse_command(line, command, param1, param2);

        // For threads
        arg *arguments = (arg*)malloc(sizeof(arg));
        strcpy(arguments->command, command);
        strcpy(arguments->param1, param1);
        strcpy(arguments->param2, param2);
        arguments->file = output_file;

        // Execute the command
        Pthread_create(&thread_array[i], NULL, execute_command, (void*)arguments);
        //execute_command(command, param1, param2, output_file);
        i++;
    }

    // Join threads
    for (int i = 0; i < threads; i++)
    {
        Pthread_join(thread_array[i], NULL);
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

void *execute_command(void *args) {
    // Get parameters
    arg *arguments = (arg*)malloc(sizeof(arg));
    arguments = (arg*)args;
    char command[MAX_COMMAND_LEN];
    char param1[MAX_NAME_LEN];
    char param2[MAX_NAME_LEN];
    FILE *output_file;
    strcpy(command, arguments->command);
    strcpy(param1, arguments->param1);
    strcpy(param2, arguments->param2);
    output_file = arguments->file;
    // Handle commands
    if (strcmp(command, "insert") == 0) {
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
    return NULL;
}
