# Unit 3 – Cryptography and Secure Execution
## Lab Writeup: Buffer Overflow in C and Python

This lab explores how unsafe memory handling in C can lead to buffer overflow vulnerabilities, and compares this against Python, where the language runtime enforces bounds checking. The exercise demonstrates why C requires careful, defensive programming and how static analysis tools like Pylint can support secure coding practices.

---

## Part I – Buffer Overflow in C

### 1. The Code (`bufoverflow.c`)

```c
#include <stdio.h>

int main(int argc, char **argv)
{
    char buf[8]; // buffer for eight characters
    printf("enter name:");
    gets(buf);   // read from stdio (sensitive function!)
    printf("%s\n", buf); // print out data stored in buf
    return 0;    // 0 as return value
}
```

### 2. Compiling and Running

```bash
gcc -o bufoverflow bufoverflow.c
./bufoverflow
```

> **Note:** Modern compilers (GCC 4.x and later) often refuse to compile code containing `gets()` without warnings, or will issue a deprecation warning such as:
> ```
> warning: implicit declaration of function 'gets' is invalid in C99
> warning: this program uses gets(), which is unsafe.
> ```
> The code may still compile and run, but the warning is itself an early indication of the vulnerability being studied.

### 3. Test 1 – Input within buffer size (8 characters or fewer)

**Input:** A short name, e.g. `Scott`

**Output:**
```
enter name:Scott
Scott
```

The program behaves exactly as expected: the name is read into `buf` and printed back out. The 8-byte buffer comfortably holds the input plus the null terminator.

### 4. Test 2 – Input exceeding buffer size (10+ characters)

**Input:** A longer string, e.g. `ScottPeatTest123`

**Output (typical on a Linux system with stack protection enabled):**
```
enter name:ScottPeatTest123
ScottPeatTest123
*** stack smashing detected ***: terminated
Aborted (core dumped)
```

On systems **without** stack protection, the result may instead be a **segmentation fault**:
```
enter name:ScottPeatTest123
Segmentation fault (core dumped)
```

In some cases, depending on the compiler, OS, and stack layout, the program may appear to "work" and print the string correctly but then crash, behave erratically, or even produce no visible error at all — this unpredictability is itself part of the danger.

### 5. What Happened, and What Does the Output Mean?

The `gets()` function reads input from `stdin` with **no bounds checking** — it has no concept of how large `buf` actually is. When the input string is longer than the 8 bytes allocated to `buf`, the extra characters are written **past the end of the buffer**, overwriting adjacent memory on the stack.

This adjacent memory typically includes:
- Padding/alignment bytes
- The **saved frame pointer**
- The **return address** of the function (where execution should resume after `main()` finishes)
- Stack canary values (if compiled with stack protection)

The messages observed mean the following:

- **`*** stack smashing detected ***: terminated`** — The compiler inserted a "canary" value (a known random value) just before the return address on the stack. When the function returns, it checks whether this canary has been altered. Because our oversized input overwrote it, the runtime detects corruption and deliberately aborts the program **before** the corrupted return address can be used. This is a *defensive mitigation* (e.g. GCC's `-fstack-protector`, enabled by default on most modern distributions).

- **`Segmentation fault (core dumped)`** — If stack protection is not active, the overwritten return address (or frame pointer) points to an invalid or inaccessible memory location. When the CPU attempts to jump to this address (or restore this frame pointer) after `main()` returns, the operating system's memory protection blocks the access, and the process is terminated with a segmentation fault.

In a real attack scenario, rather than a random crash, an attacker would carefully craft the overflow input so that the bytes overwriting the return address point to **malicious shellcode** also injected via the buffer, or to existing code (a "return-to-libc" / ROP attack), allowing arbitrary code execution with the privileges of the running program.

### 6. Root Cause and Mitigation

The fundamental flaw is the use of `gets()`, which Anthropic, GCC, and the C standard library documentation all flag as **unsafe and deprecated** (it was removed entirely from the C11 standard). Safer alternatives include:

```c
fgets(buf, sizeof(buf), stdin); // bounds-checked alternative
```

`fgets()` takes a maximum length argument and will not write beyond the supplied buffer size, preventing the overflow entirely.

---

## Part II – Buffer "Overflow" in Python

### 1. The Code (`overflow.py`)

```python
buffer = [None] * 10
for i in range(0, 11):
    buffer[i] = 7
print(buffer)
```

### 2. Running the Code

```bash
python3 overflow.py
```

### 3. The Result

```
Traceback (most recent call last):
  File "overflow.py", line 3, in <module>
    buffer[i] = 7
IndexError: list assignment index out of range
```

### 4. Explanation

The list `buffer` is created with **10 elements**, occupying valid indices `0` through `9`. However, `range(0, 11)` produces the sequence `0, 1, 2, ..., 10` — **11 values**. On the 11th iteration (`i = 10`), the code attempts `buffer[10] = 7`, which is **one position beyond the end of the list**.

Unlike the C example, Python does **not** allow this. The Python interpreter performs **bounds checking on every list access**, and immediately raises an `IndexError` exception rather than allowing the program to write into adjacent memory. The program terminates cleanly with a clear, descriptive error message, and **no memory corruption occurs**.

This is the core contrast between the two languages:

| Aspect | C (`bufoverflow.c`) | Python (`overflow.py`) |
|---|---|---|
| Bounds checking | None — programmer's responsibility | Enforced automatically by the runtime |
| Result of overflow | Memory corruption, crash, or potential exploit | Controlled exception (`IndexError`) |
| Failure mode | Silent/undefined behaviour, security risk | Explicit, traceable error |
| Fix required | Use safe functions (`fgets`), manual bounds checks | Correct the loop range (`range(0, 10)`) |

The fix for the Python code is simply to correct the off-by-one error:

```python
buffer = [None] * 10
for i in range(0, 10):
    buffer[i] = 7
print(buffer)
```

---

## Part II (continued) – Static Analysis with Pylint

### 1. Installing Pylint

```bash
pip install pylint
```

### 2. Running Pylint

From the directory containing `overflow.py`:

```bash
pylint overflow.py
```

### 3. Typical Output

```
************* Module overflow
overflow.py:1:0: C0114: Missing module docstring (missing-module-docstring)
overflow.py:1:0: C0103: Constant name "buffer" doesn't conform to UPPER_CASE naming style (invalid-name)
overflow.py:2:0: C0103: Variable name "i" doesn't conform to snake_case naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 0.00/10 (previous run: 0.00/10, +0.00)
```

*(Exact warning codes and the score may vary slightly depending on Pylint version, but the general nature of the findings is consistent.)*

### 4. Does This Tell Us How to Fix the Error?

**No — not directly.** Pylint is a **static analysis** tool: it examines the code's structure, style, and conventions *without executing it*. It is excellent at catching:

- Style and naming convention violations (PEP 8)
- Missing docstrings/comments
- Unused variables and imports
- Some categories of likely bugs (e.g. undefined variables, obvious type mismatches)

However, the `IndexError` in this exercise is a **logic error** — it only manifests when the code is *run*, because `range(0, 11)` is syntactically and stylistically valid Python. Pylint has no way of knowing that `buffer` has 10 elements and that the loop will exceed that bound; this requires runtime/dynamic analysis or careful manual review.

This highlights an important security lesson: **static analysis tools like Pylint are valuable for code quality and catching certain classes of errors early, but they are not a substitute for testing, runtime checks, and careful design.** In C, this gap is even more critical — tools such as `cppcheck`, AddressSanitizer (`-fsanitize=address`), or Valgrind are needed to catch the kind of overflow seen in Part I, since the compiler itself will not flag it as an error by default.

---

## Reflection and Discussion

This lab provided a practical demonstration of why memory safety is one of the most significant categories of vulnerability in software security:

1. **C offers performance and control at the cost of safety.** The programmer is entirely responsible for ensuring that memory accesses stay within bounds. A single careless function call (`gets()`) can lead to a crash at best, and a remote code execution vulnerability at worst — this is the underlying cause of countless real-world CVEs (e.g. historic exploits against services using unsafe string-handling functions).

2. **Python's managed runtime trades some performance for safety.** Because the interpreter enforces bounds checking, the equivalent "overflow" simply becomes a handled exception, with no risk of memory corruption.

3. **Tooling has limits.** Pylint improved code style and could catch many classes of bugs, but it could not detect this particular off-by-one logic error because it does not execute the code. This reinforces the need for a layered security approach: secure coding standards, static analysis, dynamic analysis/fuzzing, and runtime protections (e.g. stack canaries, ASLR, DEP/NX) all play complementary roles.

4. **Practical takeaway for secure development:** avoid deprecated/unsafe functions (`gets`, `strcpy`, `sprintf` without limits) in C, always validate buffer sizes and loop bounds, and use available tooling (compiler warnings, static analysers, sanitizers) as part of a defence-in-depth strategy rather than relying on any single safeguard.

---

## Repository Contents

```
Unit 3 - Cryptography and Secure Execution/
├── README.md       <- This lab writeup
├── bufoverflow.c    <- C source demonstrating an unsafe buffer (gets())
└── overflow.py      <- Python script demonstrating list bounds checking
```