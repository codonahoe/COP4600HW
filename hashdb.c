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
    printf("ACQUIRING READ LOCK\n");
    acquisition_count++;

    // Search for the record in the hash table
    hashRecord *current = hash_table[hash_value % HASH_TABLE_SIZE];
    while (current != NULL) {
        if (strcmp(current->name, name) == 0) {
            // Release the read lock and return the record
            rwlock_release_readlock(&hash_table_lock);
            printf("RELEASING READ LOCK\n");
            release_count++;
            return current;
        }
        current = current->next;
    }

    // Release the read lock and return NULL if record not found
    rwlock_release_readlock(&hash_table_lock);
    printf("RELEASING READ LOCK\n");
    release_count++;
    return NULL;
}

void insert_record(const char *name, int salary) {
    uint32_t hash_value = jenkins_one_at_a_time_hash((const uint8_t *)name, strlen(name));

    rwlock_init(&hash_table_lock);
    rwlock_acquire_writelock(&hash_table_lock);
    printf("ACQUIRING WRITE LOCK\n");
    acquisition_count++;

    // Search for the record in the hash table
    hashRecord *existing_record = search_record(name);
    if (existing_record != NULL) { // Record with the same name already exists, update its salary
        existing_record->salary = salary;
        rwlock_release_writelock(&hash_table_lock);
        printf("RELEASING WRITE LOCK\n");
        release_count++;
        return;
    }

    // Else we must create a new record
    hashRecord *new_record = (hashRecord *)malloc(sizeof(hashRecord));
    if (new_record == NULL) { ///cant allocate memory
        rwlock_release_writelock(&hash_table_lock);
        printf("RELEASING WRITE LOCK\n");
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
    rwlock_release_writelock(&hash_table_lock);
    printf("RELEASING WRITE LOCK\n");
    release_count++;
}

void delete_record(const char *name) {
    rwlock_init(&hash_table_lock);
    rwlock_acquire_writelock(&hash_table_lock);
    printf("ACQUIRING WRITE LOCK\n");
    acquisition_count++;
    // Search for the record to delete
    hashRecord *record_to_delete = search_record(name);
    if (record_to_delete == NULL) { // Record not found, release the write lock and return
        rwlock_release_writelock(&hash_table_lock);
        printf("RELEASING WRITE LOCK\n");
        release_count++;
        return;
    }

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
    rwlock_release_writelock(&hash_table_lock);
    printf("RELEASING WRITE LOCK\n");
    release_count++;
}

// Print a single record
void print_element(hashRecord element)
{
    // Print hash value, name, and salary
    printf("%u,", element.hash);
    printf("%s,", element.name);
    printf("%d\n", element.salary);
}

// Print current records in sorted order
void print_all()
{
    rwlock_acquire_readlock(&hash_table_lock);
    printf("ACQUIRING READ LOCK\n");
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
        print_element(sort[i]);
    }
    rwlock_release_readlock(&hash_table_lock);
    printf("RELEASING READ LOCK\n");
    release_count++;
}

// Print counts for lock acquire/release
void print_counts()
{
    printf("Number of lock acquisitions: %d\n", acquisition_count);
    printf("Number of lock releases: %d\n", release_count);
}