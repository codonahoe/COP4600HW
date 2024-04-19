Concurrency Group 21:
Sydney Baldwin
Devon Lister
Talia Martin
Casey O'Donahoe

Code incorporated from:
https://github.com/remzi-arpacidusseau/ostep-code/tree/master/threads-sem
https://github.com/remzi-arpacidusseau/ostep-code/tree/master/include
https://github.com/remzi-arpacidusseau/ostep-code/blob/master/threads-sema/rwlock.c
https://en.wikipedia.org/wiki/Jenkins_hash_function

(Casey) ChatGPT was used early in the assignment with mostly error handling, the reasoning behind using ChatGPT for this is because it gave a quick and mostly reliable way to debug code (instead of using for example stackoverflow). Though sometimes it gave inaccurate prompts, I made sure any debugging solutions were sound and helped move our project in the right direction. Some prompts also helped set up some parts of the the main function which was rewritten later in the process as well, it gave a good skeleton structure of how we might want to proceed. The prompts are provided below, also used it to generate a makeFile and then make adjustments based upon that.



- how would i call search record in chash.c
- pthread_rwlock_t is undefined
- what would the makefile look like
- why do i need a makeFile
- how would i run and test this
- error: implicit declaration of function 'Sem_init' is invalid in C99 [-Werror,-Wimplicit-function-declaration]
    Sem_init(&lock->lock, 1); 
- error: unknown type name 'size_t'
uint32_t jenkins_one_at_a_time_hash(const uint8_t* key, size_t length);
- Undefined symbols for architecture x86_64:
  "_search_record", referenced from:
      _execute_command in chash-03bbc2.o
ld: symbol(s) not found for architecture x86_64
clang: error: linker command failed with exit code 1 (use -v to see invocation)
- error: implicit declaration of function 'get_num_lock_releases' is invalid in C99 [-Werror,-Wimplicit-function-declaration]
    printf("Number of lock releases: %d\n", get_num_lock_releases());


These prompts were just used to help debug any errors that had been confusing, as well as helping with how to call a certain function from the main file and the concept of makeFiles and how to create one.