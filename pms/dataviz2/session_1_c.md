# The Zen of Python: Philosophy and Principles
[TOC]

Programming philosophy, design principles, and guiding values
{: .pm-subtitle}

<!-- <hr class="my-5 border-base-200"> -->


## Is this only an Easter Egg ?

Run this to see the Zen of Python:
```yaml
f_type: "codex_"
height_in_px: 20
inline: |
    import this
```


> It's not an Easter Egg, it's a list of principles that guide Python's design and coding practices. As we deal with very high level abstraction when building data visualisation tools, this list is a good guide to write Pythonic code.

## Code Examples

### 0️⃣A first example in practice
```yaml
f_type: "codex_"
height_in_px: 280
inline: |
    # Not Pythonic - verbose, implicit, hard to read
    data = [1, 2, 3, None, 5, "6"]
    result = []
    for i in range(len(data)):
        try:
            if data[i] and type(data[i]) == int and data[i] > 2:
                result.append(data[i] * 2)
        except:
            pass

    # Pythonic - clear, concise, explicit
    data = [1, 2, 3, None, 5, "6"]
    result = [num * 2 for num in data if isinstance(num, int) and num > 2]
```
The Pythonic version is more readable, avoids silent errors, and uses a list comprehension for clarity and brevity.



### 1️⃣ Beautiful is better than ugly
```yaml
f_type: "codex_"
height_in_px: 240
inline: |
    # Not Pythonic - unclear names, dense
    x = [1, 2, 3, 4, 5]
    y = []
    for i in x: 
        y.append(i**2) if i%2==0 else None
    print("y =", y)

    # Pythonic - clear names, readable
    numbers = [1, 2, 3, 4, 5]
    squared_evens = [num ** 2 for num in numbers if num % 2 == 0]
    print("squared_evens =", squared_evens)
```

### 2️⃣ Explicit is better than implicit
```yaml
f_type: "codex_"
height_in_px: 230
inline: |
    # Not Pythonic - magic numbers, hidden logic
    def calculate_price(x):
        return x * 1.15 if x > 100 else x * 1.05

    # Pythonic - explicit constants, clear intent
    TAX_RATE_HIGH = 1.15
    TAX_RATE_LOW = 1.05

    def calculate_price(amount):
        return amount * TAX_RATE_HIGH if amount > 100 else amount * TAX_RATE_LOW
```

### 3️⃣ Simple is better than complex
```yaml
f_type: "codex_"
height_in_px: 220
inline: |
    # Not Pythonic - overcomplicated logic
    def is_valid_string(s):
        if s != None:
            if len(s) > 0:
                return True if s.strip() != "" else False
        return False

    # Pythonic - straightforward, uses built-ins
    def is_valid_string(text):
        return bool(text and text.strip())
```

### 4️⃣ Flat is better than nested
```yaml
f_type: "codex_"
height_in_px: 280
inline: |
    # Not Pythonic - deeply nested
    def process_user(user):
        if user:
            if user.active:
                if user.age > 18:
                    return user.name
        return None

    # Pythonic - flat with early returns
    def process_user(user):
        if not user or not user.active or user.age <= 18:
            return None
        return user.name
```

### 5️⃣ Errors should never pass silently
```yaml
f_type: "codex_"
height_in_px: 370
inline: |
    # Not Pythonic - silent error handling
    def read_file(path):
        try:
            with open(path) as f:
                return f.read()
        except:
            return None

    # Pythonic - specific exception, logging
    import logging

    def read_file(path):
        try:
            with open(path) as file:
                return file.read()
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            return None
```

### 6️⃣ There should be one obvious way to do it
```yaml
f_type: "codex_"
height_in_px: 220
inline: |
    # Not Pythonic - multiple ways, confusing
    def sum_list(lst):
        total = 0
        for i in range(len(lst)):
            total += lst[i]
        return total

    # Pythonic - clear, uses built-in sum
    def sum_list(numbers):
        return sum(numbers)
```

## About the Zen of Python
### 📝 Historical Context
- **Author**: Tim Peters
- **Status**: Active (PEP 20)
- **Created**: August 19, 2004
- **Purpose**:
    - Codify Python's design philosophy
    - Guide developers in writing Pythonic code
- **Access**: Run `import this` in a Python interpreter

### ✅ Prerequisites
- Basic programming knowledge
- (Optional) Familiarity with Python syntax

### 🛠️ Core Philosophy
- Focus on simplicity, readability, and clarity
- Key areas: aesthetics, explicitness, error handling, design clarity

### ⚛️ Secondary learning Outcomes
- Write Pythonic code
- Recognize and avoid anti-patterns
- Create maintainable, clear code

##  The 19 Principles Explained
The Zen of Python, outlined in PEP 20, consists of 19 aphorisms that guide Python’s design and coding practices. Below is an explanation of each principle with its practical implications:

1. **Beautiful is better than ugly**  
   Write code that is visually appealing and easy to read. Use consistent formatting, meaningful variable names, and follow PEP 8 style guidelines to ensure code is aesthetically pleasing.

2. **Explicit is better than implicit**  
   Code should clearly express its intent. Avoid hidden behaviors, magic numbers, or ambiguous constructs like `import *`. Use explicit declarations for clarity.

3. **Simple is better than complex**  
   Choose the simplest solution that solves the problem. Prefer built-in functions and standard library tools over custom, complex implementations.

4. **Complex is better than complicated**  
   If complexity is unavoidable, ensure it’s well-structured and logical rather than convoluted or overly intricate.

5. **Flat is better than nested**  
   Avoid deep nesting in code (e.g., multiple nested loops or conditionals). Use early returns or guard clauses to simplify control flow.

6. **Sparse is better than dense**  
   Spread out code for readability. Avoid cramming multiple operations into a single line; use whitespace and break complex logic into steps.

7. **Readability counts**  
   Code is read more often than written. Prioritize clear, descriptive variable names and add comments for complex logic to aid understanding.

8. **Special cases aren't special enough to break the rules**  
   Follow Python’s conventions consistently, even for edge cases, to maintain uniformity across codebases.

9. **Although practicality beats purity**  
   While adhering to principles is ideal, real-world constraints may require pragmatic solutions. Balance idealism with practical needs.

10. **Errors should never pass silently**  
    Avoid bare `except:` clauses that hide errors. Handle specific exceptions and log issues to ensure problems are visible and traceable.

11. **Unless explicitly silenced**  
    If you intentionally ignore an error, make it clear with specific exception handling and document the reasoning.

12. **In the face of ambiguity, refuse the temptation to guess**  
    Avoid assumptions in unclear situations. Write code that explicitly handles all cases or fails gracefully.

13. **There should be one-- and preferably only one --obvious way to do it**  
    Python favors a single, clear approach to tasks, reducing confusion and promoting consistency across codebases.

14. **Although that way may not be obvious at first unless you're Dutch**  
    A humorous nod to Guido van Rossum (Python’s creator, who is Dutch). Some Pythonic solutions may require experience to recognize.

15. **Now is better than never**  
    It’s better to implement a working solution now than to delay indefinitely for perfection.

16. **Although never is often better than *right* now**  
    Avoid rushing into poor solutions. Take time to ensure the implementation is reasonable and maintainable.

17. **If the implementation is hard to explain, it's a bad idea**  
    Code that’s difficult to explain likely has design flaws. Aim for solutions that are intuitive and straightforward.

18. **If the implementation is easy to explain, it may be a good idea**  
    Simple, clear implementations are often indicators of good design and should be favored.

19. **Namespaces are one honking great idea -- let's do more of those!**  
    Use namespaces (e.g., modules, classes) to organize code logically, avoiding naming conflicts and improving modularity.

20. **The real Easter Egg**
    The 20th principle is intentionally unwritten, reflecting "explicit is better than implicit." More info  [here, at math.python.org](https://mail.python.org/pipermail/python-list/1999-June/001951.html).




