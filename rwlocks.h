/*
Reader-Writer locks struct definitions
*/
#include <semaphore.h> // Include this header for sem_t

typedef struct _rwlock_t {
    sem_t writelock;
    sem_t lock;
    int readers;
} rwlock_t;

void rwlock_init(rwlock_t *lock);