# Unit 3: Cryptography and Secure Execution — Memory Security Lab

## 📌 Overview
This lab demonstrates low-level memory mechanics, focusing on stack-based buffer overflows in memory-unsafe languages (C) and contrasting them with the runtime boundaries enforced by managed languages (Python).

---

## 💻 The Vulnerability: C Buffer Overflow

### Vulnerable Source Code (`bufoverflow.c`)
```c
#include <stdio.h> 

int main(int argc, char **argv)
{
    char buf[8];         // Allocate a fixed stack buffer for 8 characters
    printf("enter name:"); 
    gets(buf);           // Read from stdin (CRITICAL: Insecure function with no bounds checking)
    printf("%s\n", buf); // Print out data stored in buf
    return 0; 
}