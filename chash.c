#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hashdb.h"
#include "rwlocks.h"

#define MAX_COMMAND_LEN 100
#define MAX_NAME_LEN 50

void parse_command(char *command, char *param1, char *param2);
void execute_command(char *command, char *param1, char *param2);

int main() {
    // Initialize the concurrent hash table and locks
    init_hash_table();
    init_rwlock();

    // Hardcoded array of commands
    char *commands[] = {
        "threads,11,0",
        "insert,Richard Garriot,40000",
        "insert,Sid Meier,50000",
        "insert,Shigeru Miyamoto,51000",
        "insert,Hideo Kojima,45000",
        "insert,Gabe Newell,49000",
        "insert,Roberta Williams,45900",
        "insert,Carol Shaw,41000",
        "print,0,0",
        "search,Shigeru Miyamoto,0",
        "delete,Sid Meier,0",
        "print,0,0"
    };

    // Process each command in the array
    for (int i = 0; i < sizeof(commands) / sizeof(commands[0]); i++) {
        char command[MAX_COMMAND_LEN];
        char param1[MAX_NAME_LEN];
        char param2[MAX_NAME_LEN];

        // Copy the current command to process
        strcpy(command, commands[i]);

        // Parse the command and parameters
        parse_command(command, param1, param2);

        // Execute the command
        execute_command(command, param1, param2);
    }

    // Print summary information to console
    printf("Number of lock acquisitions: %d\n", get_num_lock_acquisitions());
    printf("Number of lock releases: %d\n", get_num_lock_releases());

    // Print final table contents to console
    printf("Final Table:\n");
    print_hash_table();

    // Clean up resources
    destroy_hash_table();
    destroy_rwlock();

    return 0;
}

void parse_command(char *command, char *param1, char *param2) {
    // Extract command and parameters from the input string
    sscanf(command, "%[^,],%[^,],%s", param1, param2);
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
        // Handle search command
        // Not implemented in this basic outline
    } else if (strcmp(command, "print") == 0) {
        // Handle print command
        // Not implemented in this basic outline
    } else {
        // Invalid command
        printf("Invalid command: %s\n", command);
    }
}