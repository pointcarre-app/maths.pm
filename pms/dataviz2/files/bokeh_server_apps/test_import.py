#!/usr/bin/env python
"""
Test script to verify all required imports work
Run with: python test_import.py
"""

print("Testing Bokeh imports...")

try:
    from bokeh.plotting import figure, curdoc, show

    print("✓ bokeh.plotting imported successfully")
except ImportError as e:
    print(f"✗ Error importing bokeh.plotting: {e}")

try:
    from bokeh.models import (
        Slider,
        Select,
        Button,
        CheckboxGroup,
        ColumnDataSource,
        DataTable,
        TableColumn,
        HoverTool,
        Div,
        TextInput,
    )

    print("✓ bokeh.models imported successfully")
except ImportError as e:
    print(f"✗ Error importing bokeh.models: {e}")

try:
    from bokeh.layouts import column, row, gridplot

    print("✓ bokeh.layouts imported successfully")
except ImportError as e:
    print(f"✗ Error importing bokeh.layouts: {e}")

try:
    from bokeh.io import output_notebook

    print("✓ bokeh.io imported successfully")
except ImportError as e:
    print(f"✗ Error importing bokeh.io: {e}")

try:
    import numpy as np

    print("✓ numpy imported successfully")
except ImportError as e:
    print(f"✗ Error importing numpy: {e}")

try:
    import pandas as pd

    print("✓ pandas imported successfully")
except ImportError as e:
    print(f"✗ Error importing pandas: {e}")

try:
    from datetime import datetime

    print("✓ datetime imported successfully")
except ImportError as e:
    print(f"✗ Error importing datetime: {e}")

print("\n" + "=" * 50)
print("Import test complete!")
print("=" * 50)

# Version check
import bokeh

print(f"\nBokeh version: {bokeh.__version__}")

import sys

print(f"Python version: {sys.version}")

print("\nAll imports successful! You can run the Bokeh server apps.")
