#!/usr/bin/env python3
"""
Simple test generator that doesn't require external imports
"""

import json
import random


def generate_question():
    """Generate a simple math question"""
    a = random.randint(1, 10)
    b = random.randint(1, 10)

    question = {"statement": f"What is {a} + {b}?", "answer": a + b, "a": a, "b": b}

    return question


def main():
    # Generate a question
    question_data = generate_question()

    # Print as JSON for the missive
    print(
        json.dumps(
            {
                "question": question_data["statement"],
                "answer": str(question_data["answer"]),
                "simplified_answer": str(question_data["answer"]),
                "components": {"a": question_data["a"], "b": question_data["b"]},
            }
        )
    )

    return 0


if __name__ == "__main__":
    exit_code = main()
    print(f"\nExecution completed with exit code: {exit_code}")
