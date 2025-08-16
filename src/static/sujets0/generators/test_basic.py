#!/usr/bin/env python3
"""
Most basic test to verify Python execution works
"""

print("Hello from Python!")
print("Basic math: 2 + 2 =", 2 + 2)


# Test if we can define functions
def greet(name):
    return f"Hello, {name}!"


print(greet("World"))

# Test if we can use lists
numbers = [1, 2, 3, 4, 5]
print("Sum of numbers:", sum(numbers))

# Test if we can use dictionaries
data = {"name": "Test", "value": 42}
print("Dictionary:", data)

print("\nExecution successful!")
