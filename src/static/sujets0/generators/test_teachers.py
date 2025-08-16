#!/usr/bin/env python3
"""
Test that teachers module is loaded and working
"""

print("Testing teachers module...")

try:
    import teachers

    print("✅ teachers module imported successfully")
    print("Available in teachers:", dir(teachers))
except ImportError as e:
    print(f"❌ Failed to import teachers: {e}")
    exit(1)

try:
    import teachers.generator as tg

    print("✅ teachers.generator imported successfully")
except ImportError as e:
    print(f"❌ Failed to import teachers.generator: {e}")
    exit(1)

try:
    import teachers.maths as tm

    print("✅ teachers.maths imported successfully")
except ImportError as e:
    print(f"❌ Failed to import teachers.maths: {e}")
    exit(1)

try:
    from teachers.defaults import SEED

    print(f"✅ teachers.defaults imported successfully, SEED={SEED}")
except ImportError as e:
    print(f"❌ Failed to import teachers.defaults: {e}")
    exit(1)

# Test creating a generator
try:
    gen = tg.MathsGenerator(0)
    n = gen.random_integer(2, 5)
    print(f"✅ MathsGenerator created, random integer: {n}")
except Exception as e:
    print(f"❌ Failed to create MathsGenerator: {e}")
    exit(1)

# Test creating math objects
try:
    x = tm.Integer(n=42)
    print(f"✅ Created Integer: {x}")
except Exception as e:
    print(f"❌ Failed to create Integer: {e}")
    exit(1)

print("\n🎉 All teachers module tests passed!")
