#include "hashdb.h"
#include "rwlocks.h"
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <stdio.h>
// Define the size of the hash table
#define HASH_TABLE_SIZE 100
static hashRecord *hash_table[HASH_TABLE_SIZE];
static rwlock_t hash_table_lock;

/*
Concurrent Hash Table implementation: including Jenkins function and all linked list operations
*/

uint32_t jenkins_one_at_a_time_hash(const uint8_t* key, size_t length) {
  size_t i = 0;
  uint32_t hash = 0;
  while (i != length) {
    hash += key[i++];
    hash += hash << 10;
    hash ^= hash >> 6;
  }
  hash += hash << 3;
  hash ^= hash >> 11;
  hash += hash << 15;
  return hash;
}

// Get total count of threads
int thread_count(const char *number)
{
    return atoi(number);
}

hashRecord *search_record(const char *name) {
    // Compute the hash value for the name
    uint32_t hash_value = jenkins_one_at_a_time_hash((const uint8_t *)name, strlen(name));

    // Acquire the read lock
    rwlock_init(&hash_table_lock);
    rwlock_acquire_readlock(&hash_table_lock);
    printf("Aquiring Read Lock\n");

    // Search for the record in the hash table
    hashRecord *current = hash_table[hash_value % HASH_TABLE_SIZE];
    while (current != NULL) {
        if (strcmp(current->name, name) == 0) {
            // Release the read lock and return the record
            rwlock_release_readlock(&hash_table_lock);
            return current;
        }
        current = current->next;
    }

    // Release the read lock and return NULL if record not found
    rwlock_release_readlock(&hash_table_lock);
    printf("Releasing Read Lock\n");
    return NULL;
}

void insert_record(const char *name, int salary) {
    // Compute the hash value for the name
    uint32_t hash_value = jenkins_one_at_a_time_hash((const uint8_t *)name, strlen(name));

    // Acquire the write lock
    rwlock_init(&hash_table_lock);
    rwlock_acquire_writelock(&hash_table_lock);

    // Create a new record
    hashRecord *new_record = (hashRecord *)malloc(sizeof(hashRecord));
    if (new_record == NULL) {
        rwlock_release_writelock(&hash_table_lock);
        return;
    }
    new_record->hash = hash_value;
    strncpy(new_record->name, name, 50);
    new_record->salary = salary;
    new_record->next = NULL;

    // Insert the record into the hash table
    int index = hash_value % HASH_TABLE_SIZE;
    if (hash_table[index] == NULL) {
        hash_table[index] = new_record;
    } else {
        //Update existing record
        hashRecord *current = hash_table[index];
        //check if name exists
        while (current != NULL) {
            if (strcmp(current->name, name) == 0) {
                //Exists so update the salary
                current->salary = salary;
                break;
            }
            //else name not found & we need to append to end of list to avoid collision (chaining)
            if (current->next == NULL) {
                // Name not found, append the new record
                current->next = new_record;
                break;
            }
            current = current->next;
        }
    }

    // Release the write lock
    rwlock_release_writelock(&hash_table_lock);
}

// Print a single record
void print_element(hashRecord *element)
{
    // Print hash value, name, and salary
    printf("%d,", element->hash);
    printf("%s,", element->name);
    printf("%d\n", element->salary);
}

// Print the current list
void print_all(hashRecord *head)
{
    hashRecord *current = head;
    // Use single record print for each record
    while (current != NULL)
    {
        print_element(current);
        current = current->next;
    }
}
