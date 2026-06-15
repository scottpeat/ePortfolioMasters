# Unit 4 – Exploring Programming Language Concepts

This entry covers two core language concepts explored in Unit 4: **recursion** (via the Towers of Hanoi problem) and **regular expressions** (via UK postcode validation). Both exercises were completed in a Jupyter Notebook environment using Python.

---

## Table of Contents

- [1. Recursion: Towers of Hanoi](#1-recursion-towers-of-hanoi)
  - [1.1 Implementation](#11-implementation)
  - [1.2 Sample Output](#12-sample-output)
  - [1.3 Theoretical Maximum Number of Disks](#13-theoretical-maximum-number-of-disks)
  - [1.4 What Limits the Number of Iterations? Security Implications](#14-what-limits-the-number-of-iterations-security-implications)
- [2. Regex: UK Postcode Validation](#2-regex-uk-postcode-validation)
  - [2.1 Implementation](#21-implementation)
  - [2.2 Test Results](#22-test-results)
  - [2.3 Avoiding an Evil Regex Attack](#23-avoiding-an-evil-regex-attack)
- [3. Reflections on Weidman: Evil Regex and Regex Security](#3-reflections-on-weidman-evil-regex-and-regex-security)
  - [3.1 What is an Evil Regex?](#31-what-is-an-evil-regex)
  - [3.2 Common Problems with Regex and How to Mitigate Them](#32-common-problems-with-regex-and-how-to-mitigate-them)
  - [3.3 How and Why Regex Can Be Used as Part of a Security Solution](#33-how-and-why-regex-can-be-used-as-part-of-a-security-solution)
- [References](#references)

---

## 1. Recursion: Towers of Hanoi

The Towers of Hanoi problem is a classic demonstration of recursion. The objective is to move a stack of *n* disks from a source peg to a target peg, using a third peg as an auxiliary, subject to two rules:

1. Only one disk may be moved at a time.
2. A larger disk may never be placed on top of a smaller disk.

Following the explanation and walkthrough provided by Cormen and Balkcom (no date), the recursive solution can be summarised as follows for moving `n` disks from `source` to `target` using `auxiliary`:

1. Move `n - 1` disks from `source` to `auxiliary`.
2. Move the remaining (largest) disk from `source` to `target`.
3. Move the `n - 1` disks from `auxiliary` to `target`.

### 1.1 Implementation

The program below asks the user for the number of disks, executes the moves recursively, displays each move with a simple `*`-based visualisation of the towers, and finally reports the total number of moves performed.

```python
"""
Towers of Hanoi - Recursive Implementation
Based on the explanation and approach described by Cormen and Balkcom (no date).
"""

move_count = 0

def hanoi(n, source, target, auxiliary, towers):
    global move_count
    if n == 0:
        return
    # Move n-1 disks from source to auxiliary
    hanoi(n - 1, source, auxiliary, target, towers)
    # Move the nth (largest remaining) disk from source to target
    disk = towers[source].pop()
    towers[target].append(disk)
    move_count += 1
    print(f"Move {move_count}: Disk {disk} from {source} -> {target}")
    print_towers(towers)
    # Move the n-1 disks from auxiliary to target
    hanoi(n - 1, auxiliary, target, source, towers)


def print_towers(towers):
    for peg in ['A', 'B', 'C']:
        disks = towers[peg]
        representation = ' '.join('*' * d for d in disks) if disks else '-'
        print(f"  {peg}: {representation}")
    print()


def main():
    while True:
        try:
            n = int(input("Enter the number of disks: "))
            if n <= 0:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    # Disks are represented as integers 1 (smallest) to n (largest).
    # Tower A starts with all disks, largest at the bottom.
    towers = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}

    print("\nInitial configuration:")
    print_towers(towers)

    hanoi(n, 'A', 'C', 'B', towers)

    print(f"Total moves executed: {move_count}")
    print(f"Theoretical minimum moves (2^n - 1): {2**n - 1}")


if __name__ == "__main__":
    main()
```

Each disk is represented by a row of asterisks (`*`), where the number of asterisks corresponds to the disk's size — larger disks display as longer rows. This gives an immediate, readable visual of the puzzle state after every move.

### 1.2 Sample Output

Running the program with `n = 5` produces output such as:

```
Enter the number of disks: 5

Initial configuration:
  A: ***** **** *** ** *
  B: -
  C: -

Move 1: Disk 1 from A -> C
  A: ***** **** *** **
  B: -
  C: *

Move 2: Disk 2 from A -> B
  A: ***** **** ***
  B: **
  C: *

Move 3: Disk 1 from C -> B
  A: ***** **** ***
  B: ** *
  C: -

... (additional moves omitted for brevity) ...

Total moves executed: 31
Theoretical minimum moves (2^n - 1): 31
```

This confirms the well-known result that the minimum number of moves required for `n` disks is `2^n - 1`, and the program's move counter matches this formula exactly.

### 1.3 Theoretical Maximum Number of Disks

In theory, the algorithm itself places **no upper bound** on `n` — recursion is a general technique and the mathematics of the problem works for any positive integer. In practice, however, the program will fail well before any "theoretical" limit imposed by the problem itself, because of constraints in the **execution environment**:

- **Python's recursion limit.** By default, Python imposes a maximum recursion depth of **1,000** (`sys.getrecursionlimit()`). Since `hanoi()` recurses to a depth of `n`, a value of `n` somewhere around **995–997** (allowing for the small number of stack frames already used by `main()` and the interpreter) will trigger a `RecursionError: maximum recursion depth exceeded`.
- **The exponential growth of moves.** Even *before* hitting the recursion limit, the number of moves required (`2^n - 1`) becomes computationally infeasible. For example:
  - `n = 20` → 1,048,575 moves
  - `n = 30` → over 1 billion moves
  - `n = 64` (the classic "legend of the temple" version of the puzzle) → over 18 quintillion moves

  Long before `n` reaches the recursion-depth limit of ~1,000, the program would take longer than the lifetime of the universe to actually complete the moves, even though the *recursive call stack itself* would not yet be exhausted at smaller values of `n`.

So, in a strict sense, the **recursion depth limit (~995–997 disks)** is the point at which the program would raise an error and stop outright. But the **practical, usable maximum** is far lower (realistically under 25–30 disks) due to the exponential time complexity of the problem, even though no error would technically be thrown at those values.

### 1.4 What Limits the Number of Iterations? Security Implications

Two distinct factors limit how many recursive calls (and therefore "iterations") can occur:

1. **The call stack and recursion limit.** Every recursive call adds a new frame to the call stack, consuming memory. Python enforces a configurable ceiling (`sys.setrecursionlimit()`, default 1,000) specifically to prevent a runaway recursive function from crashing the interpreter by exhausting the underlying C stack. Without this safeguard, deep or infinite recursion would eventually cause a **stack overflow** at the operating system level.
2. **Combinatorial/exponential growth of the problem itself.** Independent of the stack, the *amount of work* the recursive function generates (here, `2^n - 1` moves) grows exponentially with the input size, making the program practically unusable long before any hard system limit is reached.

**Implications for application and system security:**

- **Denial of Service (DoS) via stack exhaustion.** If an application accepts user input that controls the depth of a recursive function (directly or indirectly — for example, recursively parsing nested JSON, XML, or file-system paths), an attacker can supply deliberately deep or malicious input to force excessive recursion. This can crash the process with a stack overflow, or, in languages without Python's protective recursion limit (such as C), corrupt memory and potentially allow arbitrary code execution.
- **Resource exhaustion / algorithmic complexity attacks.** Even where stack depth isn't the limiting factor, an attacker who understands that an operation grows exponentially (or even just polynomially) with input size can submit a small, innocuous-looking input that causes the server to consume excessive CPU or memory — a form of DoS sometimes called an "algorithmic complexity attack."
- **The need for input validation and bounds-checking.** This exercise demonstrates why production code should never trust user-supplied values to control recursion depth, loop counts, or memory allocation without validation. Sensible upper bounds (and, where appropriate, converting recursive solutions to iterative ones with explicit stacks) help ensure that legitimate use cases are served while malicious or accidental extreme inputs are rejected gracefully rather than crashing the system.

---

## 2. Regex: UK Postcode Validation

The UK postcode format follows a defined structure consisting of an **outward code** (area and district, e.g. `M1`, `CR2`, `EC1A`) and an **inward code** (sector and unit, e.g. `1AA`, `6XH`), separated by a space. The structural rules — including which letters can and cannot appear in specific positions — are set out by idealpostcodes (2020), following the official Royal Mail / GOV.UK specification.

### 2.1 Implementation

```python
"""
UK Postcode Validation using Regular Expressions
Pattern based on the official UK postcode specification
(as summarised by idealpostcodes, 2020).
"""

import re

# UK postcode regex:
#   Outward code: 1-2 letters, then 1-2 digits, optionally followed
#                 by a single letter  (e.g. M1, M60, CR2, DN55, W1A, EC1A)
#   Inward code:  a single digit followed by two letters, where the
#                 final two letters EXCLUDE C, I, K, M, O, V
#                 (these letters are never used in the final position
#                 to avoid confusion with similar-looking characters
#                 and digits, e.g. 0/O, 1/I)
UK_POSTCODE_REGEX = re.compile(
    r"^[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][ABD-HJLNP-UW-Z]{2}$",
    re.IGNORECASE
)


def is_valid_postcode(postcode):
    """Return True if the postcode matches the UK postcode pattern."""
    return bool(UK_POSTCODE_REGEX.match(postcode.strip()))


if __name__ == "__main__":
    test_postcodes = [
        "M1 1AA",
        "M60 1NW",
        "CR2 6XH",
        "DN55 1PT",
        "W1A 1HQ",
        "EC1A 1BB",
        "ST7 9HV",   # Given as an invalid example in the exercise
        "12345",     # Clearly invalid
        "AAAA 1AA",  # Too many letters in the outward code
    ]

    for pc in test_postcodes:
        result = "VALID" if is_valid_postcode(pc) else "INVALID"
        print(f"{pc:10} -> {result}")
```

### 2.2 Test Results

```
M1 1AA     -> VALID
M60 1NW    -> VALID
CR2 6XH    -> VALID
DN55 1PT   -> VALID
W1A 1HQ    -> VALID
EC1A 1BB   -> VALID
ST7 9HV    -> INVALID
12345      -> INVALID
AAAA 1AA   -> INVALID
```

All six provided valid examples (`M1 1AA`, `M60 1NW`, `CR2 6XH`, `DN55 1PT`, `W1A 1HQ`, `EC1A 1BB`) pass validation, confirming the regex correctly handles the different outward-code formats (`A9`, `A99`, `AA9`, `AA99`, `A9A`, `AA9A`).

**`ST7 9HV` is correctly flagged as invalid.** Although its overall *shape* looks plausible (two letters, a digit, a space, a digit, two letters), the final letter `V` is one of the letters (`C`, `I`, `K`, `M`, `O`, `V`) that the Royal Mail specification never uses in the final two positions of a postcode, precisely because letters like `V` and `O` can be visually confused with digits (`0`) or other letters in handwriting and certain fonts. The regex's character class `[ABD-HJLNP-UW-Z]` explicitly excludes these letters, so `ST7 9HV` fails to match — demonstrating that the regex is enforcing a *real* postal rule, not just a loose pattern shape.

> **Note:** Regex can only validate that a string is *formatted correctly* as a postcode. It cannot confirm that the postcode actually *exists* or is currently in use — that would require checking against the Royal Mail Postcode Address File (PAF) or a postcode lookup API.

### 2.3 Avoiding an Evil Regex Attack

An "evil" regex is one that is vulnerable to **catastrophic backtracking** (see Section 3.1), typically caused by *nested or overlapping quantifiers* applied to patterns that can match the same input in multiple ways (e.g. `(a+)+$`, `(a|aa)+$`, `([a-zA-Z]+)*$`).

The postcode regex above was deliberately written to avoid this risk:

- **No nested quantifiers.** Every quantifier (`{1,2}`, `?`, `{2}`) is applied directly to a simple character class, and none of these quantified groups are themselves wrapped in another quantifier. There is no construct of the form `(X+)+` or `(X*)*` anywhere in the pattern.
- **Fixed-length, bounded repetition.** All repeated elements have small, explicit bounds (`{1,2}`, `{2}`, or a single optional character `?`). The total input length the regex can meaningfully match is small and bounded — postcodes are at most 8 characters — so even in the worst case the engine has very little to backtrack over.
- **Unambiguous character classes.** Each position in the pattern is restricted to a specific, non-overlapping character class (letters vs. digits vs. a restricted letter set), so there is only ever **one way** for a given input string to match (or fail to match) the pattern. Ambiguity — where the same substring could be consumed by multiple parts of the pattern — is the root cause of exponential backtracking, and this pattern has none.
- **Anchored matching.** The pattern uses `^` and `$` to anchor the match to the whole string, preventing the engine from attempting many partial matches at different starting positions within a larger string.
- **Input length limits as a defence-in-depth measure.** In a production system, it is good practice to also enforce a maximum input length (e.g. reject any string longer than 8–10 characters) *before* passing it to the regex engine. This ensures that even if a pattern were unexpectedly inefficient, the worst-case input size — and therefore the worst-case processing time — remains bounded.

---

## 3. Reflections on Weidman: Evil Regex and Regex Security

### 3.1 What is an Evil Regex?

An "evil regex" is a regular expression whose structure makes it vulnerable to **catastrophic backtracking** — a situation where, for certain crafted inputs, the regex engine's matching algorithm takes an amount of time that grows **exponentially** with the length of the input, rather than linearly.

This typically occurs when a pattern contains **nested quantifiers operating over overlapping character sets** — for example, a group that itself contains a repeated element, where that group is also repeated, such as `(a+)+`, `(a*)*`, or `([a-zA-Z]+)*`. When such a pattern is tested against an input that *almost* matches but ultimately fails (e.g. a long run of valid characters followed by one invalid character), a backtracking-based regex engine must try an enormous number of different ways of dividing the input among the repeated groups before it can conclude the match fails.

Because the number of possible ways to partition the string grows exponentially with its length, an attacker can submit a relatively short, carefully chosen input string and cause the regex engine to consume CPU resources for an extremely long time — effectively a **Denial of Service (DoS)** attack, often referred to as **ReDoS (Regular expression Denial of Service)**. Weidman highlights this as a serious and often overlooked vulnerability, since regex patterns are frequently used in input validation and are an easy attack surface for an attacker to probe with automated tools.

### 3.2 Common Problems with Regex and How to Mitigate Them

Several recurring problems arise when regex is used in real applications:

1. **Catastrophic backtracking / ReDoS (as above).**
   - *Mitigation:* Avoid nested or ambiguous quantifiers. Prefer patterns where each part of the input can only be matched in one way (as in the postcode example above). Use tools (e.g. static analysers, or online tools that detect catastrophic backtracking patterns) to test regexes before deployment. Where supported, use regex engines that guarantee linear-time matching (e.g. Google's RE2), or impose a timeout on regex execution so a runaway match can be aborted safely.

2. **False sense of security from "validation".** A regex that checks *format* is often mistaken for full input validation. A string can be perfectly well-formed according to a regex (e.g. a syntactically valid email address or postcode) while still being malicious — for example, containing SQL injection payloads that happen to be permitted by a loose character class, or referencing a non-existent account.
   - *Mitigation:* Treat regex as one layer of defence, not the whole solution. Combine format validation with proper output encoding, parameterised queries, and (where relevant) lookups against authoritative data sources (e.g. a postcode database) to confirm the value is not just well-formed but also legitimate.

3. **Overly permissive or overly restrictive patterns.** Regexes that are too loose may allow malicious or malformed data through; regexes that are too strict may reject valid input (a common complaint with email and name validation, which can exclude legitimate international characters, plus-addressing, etc.).
   - *Mitigation:* Base patterns on an authoritative specification (as was done here using the official UK postcode rules) rather than guesswork, and test extensively against both valid and invalid real-world examples, including edge cases.

4. **Readability and maintainability.** Complex regexes are notoriously difficult to read, debug, and modify safely. A small, well-intentioned edit can silently introduce a catastrophic backtracking vulnerability or a logic error.
   - *Mitigation:* Write regexes incrementally, comment them clearly (as in the Python examples above), break very complex patterns into smaller named sub-patterns, and maintain a test suite of known-good and known-bad inputs that is run whenever the pattern changes.

5. **Encoding and Unicode issues.** Regexes designed with only ASCII in mind may behave unexpectedly (or insecurely) when presented with Unicode input, homoglyphs, or different encodings — which can sometimes be used to bypass validation (e.g. in security filters).
   - *Mitigation:* Be explicit about the character sets and encodings a pattern is expected to handle, normalise input (e.g. to a consistent Unicode normalisation form) before matching, and test with non-ASCII input where relevant.

### 3.3 How and Why Regex Could Be Used as Part of a Security Solution

Despite the risks above, regex remains a valuable and widely used security tool when applied carefully:

- **Input validation and sanitisation.** Regex is commonly used as a first-line filter to ensure user-supplied data conforms to an expected format (postcodes, email addresses, usernames, file paths, etc.) before it is processed further. Rejecting malformed input early reduces the attack surface for downstream components.
- **Web Application Firewalls (WAFs) and Intrusion Detection/Prevention Systems (IDS/IPS).** Many WAF and IDS products use regex-based signatures to detect known attack patterns in HTTP requests — for example, patterns characteristic of SQL injection (`' OR 1=1`), cross-site scripting (`<script>`), or directory traversal (`../../`). Regex allows these systems to flag or block suspicious traffic in real time.
- **Log analysis and threat hunting.** Security analysts routinely use regex to search through large volumes of log data for indicators of compromise — for example, identifying patterns of failed login attempts, unusual user-agent strings, or specific malware signatures within network traffic logs.
- **Data Loss Prevention (DLP).** Regex patterns are used to detect sensitive data formats (e.g. credit card numbers, National Insurance numbers, or — as in this exercise — postcodes as part of personally identifiable information) within outgoing emails or files, enabling organisations to flag or block potential data leaks.

**Why** regex is well suited to these roles is that it provides a *concise, declarative, and portable* way to describe complex string patterns, can be evaluated very quickly for well-designed (non-evil) patterns, and is supported natively across almost every programming language, web server, and security tool — making it a practical "common language" for describing both legitimate and malicious input patterns.

However, as discussed above, regex used in a security context must itself be designed defensively: a poorly written detection or validation regex can become the very vulnerability (via ReDoS) that the security control was meant to prevent, which is precisely the tension Weidman draws attention to.

---

## References

- Cormen, T. and Balkcom, D. (no date) *Recursion: the Towers of Hanoi*. [Link as provided in module reading list].
- idealpostcodes (2020) *UK Postcode Format*. [Link as provided in module reading list].
- Jaiswal, S. (2020) *Python Regular Expressions Tutorial*. [Link as provided in module lecturecast].
- Weidman, G. (no date) *Evil Regex / Regular Expression Denial of Service (ReDoS)*. [Link as provided in module reading list].

*(Full citation details and direct links are taken from the module reading list as provided by the tutor; please update these entries with the exact URLs/dates from the reading list before final submission.)*
