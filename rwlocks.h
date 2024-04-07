/*
Reader-Writer locks struct definitions
*/
typedef struct _rwlock_t {
    sem_t writelock;
    sem_t lock;
    int readers;
} rwlock_t;