#ifndef HASHDB_H
#define HASHDB_H

#include <stdint.h> // Include this header for uint32_t
#include <stdlib.h>

typedef struct hash_struct
{
    uint32_t hash;       // 32-bit unsigned integer for the hash value made by running the name text thru Jenkins function
    char name[51];       // Arbitrary string up to 50 characters long
    uint32_t salary;     // 32-bit unsigned integer to represent an annual salary
    struct hash_struct *next; // pointer to the next node in the list
} hashRecord;

int thread_count(const char *number);
hashRecord *search_record(const char *name);
uint32_t jenkins_one_at_a_time_hash(const uint8_t* key, size_t length);
void print_element(hashRecord *element);
void print_all(hashRecord *head);
#endif /* HASHDB_H */
