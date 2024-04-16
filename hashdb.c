#include "hashdb.h"
#include "rwlocks.h"
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
// Define the size of the hash table
#define HASH_TABLE_SIZE 100
static hashRecord *hash_table[HASH_TABLE_SIZE];
static pthread_rwlock_t hash_table_lock;

/*
Concurrent Hash Table implementation: including your Jenkins function and all linked list operations
*/

/*
Reference of Jenkins function:

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
*/

uint32_t compute_hash(const char *key) {
    // Initialize hash to a non-zero value
    uint32_t hash = 5381;
    int c;

    // Iterate over each character in the key
    while ((c = *key++)) {
        // Update hash using a simple hash function (djb2)
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }
    // Return the computed hash value
    return hash;
}

hashRecord *search_record(const char *name) {
    // Compute the hash value for the name
    uint32_t hash_value = compute_hash(name);

    // Acquire the read lock
    pthread_rwlock_rdlock(&hash_table_lock);

    // Search for the record in the hash table
    hashRecord *current = hash_table[hash_value % HASH_TABLE_SIZE];
    while (current != NULL) {
        if (strcmp(current->name, name) == 0) {
            // Release the read lock and return the record
            pthread_rwlock_unlock(&hash_table_lock);
            return current;
        }
        current = current->next;
    }

    // Release the read lock and return NULL if record not found
    pthread_rwlock_unlock(&hash_table_lock);
    return NULL;
}