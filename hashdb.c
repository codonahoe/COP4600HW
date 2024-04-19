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
// Keeps track of locks and releases
int acquisition_count = 0;
int release_count = 0;

/*
Concurrent Hash Table implementation: including Jenkins function and all linked list operations
*/
//Jenkins function
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
    // Initialize rwlock here since threads is always first line
    rwlock_init(&hash_table_lock);
    return atoi(number);
}

// Search command
hashRecord *search_record(const char *name, FILE *output_file) {
    // Compute the hash value for the name
    uint32_t hash_value = jenkins_one_at_a_time_hash((const uint8_t *)name, strlen(name));
    printf("SEARCH,%s\n", name);
    fprintf(output_file, "SEARCH,%s\n", name);

    // Acquire the read lock
    rwlock_acquire_readlock(&hash_table_lock);
    /*printf("READ LOCK ACQUIRED\n");
    fprintf(output_file, "READ LOCK ACQUIRED\n");*/
    acquisition_count++;

    // Search for the record in the hash table
    hashRecord *current = hash_table[hash_value % HASH_TABLE_SIZE];
    while (current != NULL) {
        if (strcmp(current->name, name) == 0) {
            // Release the read lock and return the record
            printf("READ LOCK RELEASED\n");
            fprintf(output_file, "READ LOCK RELEASED\n");
            rwlock_release_readlock(&hash_table_lock);
            printf("%lu,%s,%u\n", (unsigned long)current->hash, current->name, current->salary);
            fprintf(output_file, "%lu,%s,%u\n", (unsigned long)current->hash, current->name, current->salary);
            release_count++;
            return current;
        }
        current = current->next;
    }

    // Release the read lock and return NULL if record not found
    printf("READ LOCK RELEASED\n");
    fprintf(output_file, "READ LOCK RELEASED\n");
    rwlock_release_readlock(&hash_table_lock);
    release_count++;
    return NULL;
}

// Insert command
void insert_record(const char *name, int salary, FILE *output_file) {
    uint32_t hash_value = jenkins_one_at_a_time_hash((const uint8_t *)name, strlen(name));
    printf("INSERT,%lu,%s,%d\n", (unsigned long)hash_value, name, salary);
    fprintf(output_file, "INSERT,%lu,%s,%d\n", (unsigned long)hash_value, name, salary);

    rwlock_acquire_writelock(&hash_table_lock);
    printf("WRITE LOCK ACQUIRED\n");
    fprintf(output_file, "WRITE LOCK ACQUIRED\n");
    acquisition_count++;

    // Create record
    hashRecord *new_record = (hashRecord *)malloc(sizeof(hashRecord));
    if (new_record == NULL) { ///cant allocate memory
        printf("WRITE LOCK RELEASED\n");
        fprintf(output_file, "WRITE LOCK RELEASED\n");
        rwlock_release_writelock(&hash_table_lock);
        release_count++;
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
        // Append to end of list to avoid collision (chaining)
        hashRecord *current = hash_table[index];
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = new_record;
    }
    printf("WRITE LOCK RELEASED\n");
    fprintf(output_file, "WRITE LOCK RELEASED\n");
    rwlock_release_writelock(&hash_table_lock);
    release_count++;
}

// Delete command
void delete_record(const char *name, FILE *output_file) {
    printf("DELETE,%s\n", name);
    fprintf(output_file, "DELETE,%s\n", name);
    // Print statement here, not inside search function, to match example output
    printf("READ LOCK ACQUIRED\n");
    fprintf(output_file, "READ LOCK ACQUIRED\n");
    // Search for the record to delete
    hashRecord *record_to_delete = search_record(name, output_file);
    if (record_to_delete == NULL) { // Record not found
        return;
    }

    rwlock_acquire_writelock(&hash_table_lock);
    printf("WRITE LOCK ACQUIRED\n");
    fprintf(output_file, "WRITE LOCK ACQUIRED\n");
    acquisition_count++;
    uint32_t hash_value = record_to_delete->hash;
    int index = hash_value % HASH_TABLE_SIZE;

    // Search again to find the previous record in the list
    hashRecord *current = hash_table[index];
    hashRecord *prev = NULL;
    while (current != NULL && current != record_to_delete) {
        prev = current;
        current = current->next;
    }

    // Remove the record from the list
    if (prev == NULL) { // The record to delete is the first in the list
        hash_table[index] = record_to_delete->next;
    } else {
        prev->next = record_to_delete->next;
    }
    free(record_to_delete);
    printf("WRITE LOCK RELEASED\n");
    fprintf(output_file, "WRITE LOCK RELEASED\n");
    rwlock_release_writelock(&hash_table_lock);
    release_count++;
}

// Print a single record
void print_element(hashRecord element, FILE *output_file)
{
    // Print hash value, name, and salary
    printf("%u,", element.hash);
    fprintf(output_file, "%u,", element.hash);
    printf("%s,", element.name);
    fprintf(output_file, "%s,", element.name);
    printf("%d\n", element.salary);
    fprintf(output_file, "%d\n", element.salary);
}

// Print current records in sorted order
void print_all(FILE *output_file)
{
    rwlock_acquire_readlock(&hash_table_lock);
    printf("READ LOCK ACQUIRED\n");
    fprintf(output_file, "READ LOCK ACQUIRED\n");
    acquisition_count++;
    hashRecord sort[HASH_TABLE_SIZE];
    int index = 0;
    // Grab elements of hash table that aren't null
    for (int i = 0; i < HASH_TABLE_SIZE; i++)
    {
        if (hash_table[i])
        {
            sort[index].hash = hash_table[i]->hash;
            strcpy(sort[index].name, hash_table[i]->name);
            sort[index].salary = hash_table[i]->salary;
            sort[index].next = hash_table[i]->next;
            index++;
        }
    }
    int k;
    // Sort relevant indexes by hash
    for (int i = 0; i < index; i++)
    {
        for (int i = 0; i < index-1; i++)
        {
            k = i;
            for (int j = i+1; j < index; j++)
            {
                if (sort[j].hash < sort[k].hash)
                {
                    k = j;
                }
            }
            if (k != i)
            {
                hashRecord temp;
                // temp = a
                temp.hash = sort[k].hash;
                strcpy(temp.name, sort[k].name);
                temp.salary = sort[k].salary;
                temp.next = sort[k].next;
                // a = b
                sort[k].hash = sort[i].hash;
                strcpy(sort[k].name, sort[i].name);
                sort[k].salary = sort[i].salary;
                sort[k].next = sort[i].next;
                // b = temp
                sort[i].hash = temp.hash;
                strcpy(sort[i].name, temp.name);
                sort[i].salary = temp.salary;
                sort[i].next = temp.next;
            }
        }
    }
    // Print resulting array
    for (int i = 0; i < index; i++)
    {
        print_element(sort[i], output_file);
    }
    printf("READ LOCK RELEASED\n");
    fprintf(output_file, "READ LOCK RELEASED\n");
    rwlock_release_readlock(&hash_table_lock);
    release_count++;
}

// Print counts for lock acquire/release
void print_counts(FILE *output_file)
{
    printf("Number of lock acquisitions: %d\n", acquisition_count);
    fprintf(output_file, "Number of lock acquisitions: %d\n", acquisition_count);
    printf("Number of lock releases: %d\n", release_count);
    fprintf(output_file, "Number of lock releases: %d\n", release_count);
}