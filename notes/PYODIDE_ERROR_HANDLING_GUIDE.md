# Pyodide Python Error Handling Guide

## Problem Statement
When executing Python code through Pyodide in the browser, errors are often opaque and only show generic messages like "Python Execution Error" in the console, making debugging difficult.

## Solutions for Better Error Visibility

### Solution 1: Enhanced JavaScript Error Logging
**Location**: `files/sujets0/sujets0_question_generator_v1.js` around line 310-338

```javascript
// Enhanced error handling in executePythonCode function
const result = await manager.executeAsync(filename, pythonCode);
const success = !result.error && (result.exit_code === 0 || result.missive);

if (!success) {
  // Add detailed error logging
  console.error("=== PYTHON ERROR DETAILS ===");
  console.error("Error:", result.error);
  console.error("Exit Code:", result.exit_code);
  console.error("STDOUT:", result.stdout);
  console.error("STDERR:", result.stderr);
  
  // Python traceback is usually in stderr
  if (result.stderr) {
    console.error("Python Traceback:\n", result.stderr);
  }
  
  return {
    success: false,
    error: result.error || "Execution failed",
    stdout: result.stdout,
    stderr: result.stderr,
    pythonTraceback: result.stderr  // Add for easier access
  };
}
```

### Solution 2: Python-Side Error Wrapper
Add comprehensive error handling in your Python generators:

```python
import traceback
import sys

try:
    # Your existing code
    components = generate_components(None)
    answer = solve(**components)
    question = render_question(**components)
    
    # Create missive
    missive({...})
    
except Exception as e:
    # Print full traceback to stderr for visibility
    traceback.print_exc(file=sys.stderr)
    
    # Also print simplified error info
    print(f"ERROR: {str(e)}", file=sys.stderr)
    print(f"ERROR TYPE: {type(e).__name__}", file=sys.stderr)
    print(f"ERROR LOCATION: Line {sys.exc_info()[2].tb_lineno}", file=sys.stderr)
    
    # Optional: Send error as missive for structured handling
    missive({
        "error": True,
        "error_type": type(e).__name__,
        "error_message": str(e),
        "traceback": traceback.format_exc()
    })
    
    # Re-raise to maintain error state
    raise
```

### Solution 3: Debug Mode with Verbose Output
Add a debug wrapper in JavaScript that automatically wraps Python code:

```javascript
// Add debug flag
const DEBUG_PYTHON = true;

if (DEBUG_PYTHON) {
  // Wrap entire Python code in error handler
  pythonCode = `
import sys
import traceback

def debug_wrapper():
    try:
${pythonCode.split('\n').map(line => '        ' + line).join('\n')}
    except Exception as e:
        print("=== PYTHON EXCEPTION ===", file=sys.stderr)
        print(f"Error Type: {type(e).__name__}", file=sys.stderr)
        print(f"Error Message: {str(e)}", file=sys.stderr)
        print("=== FULL TRACEBACK ===", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("=== END EXCEPTION ===", file=sys.stderr)
        raise

debug_wrapper()
`;
}
```

### Solution 4: Pyodide-Specific Exception Extraction
Access Python exceptions directly through Pyodide API:

```javascript
// After executeAsync fails
if (!success && window.pyodide) {
  try {
    // Get the last Python exception details
    const pyErr = window.pyodide.runPython(`
import sys
import traceback

# Get last exception if available
if hasattr(sys, 'last_value'):
    exc_info = {
        'type': sys.last_type.__name__,
        'value': str(sys.last_value),
        'traceback': ''.join(traceback.format_exception(
            sys.last_type, sys.last_value, sys.last_traceback
        ))
    }
else:
    exc_info = {'error': 'No Python exception available'}

exc_info
    `);
    console.error("Python Exception Details:", pyErr);
  } catch (e) {
    console.error("Could not extract Python error:", e);
  }
}
```

### Solution 5: Structured Error Reporting
Modify the Python generator template to always include error handling:

```python
# Template for all generators
def safe_execute():
    try:
        # Generator code here
        components = generate_components(None, seed)
        answer = solve(**components)
        question = render_question(**components)
        
        # Success missive
        missive({
            "success": True,
            "data": {...}
        })
        
    except KeyError as e:
        missive({
            "success": False,
            "error_type": "KeyError",
            "error_message": f"Missing key: {e}",
            "hint": "Check that all required parameters are being passed"
        })
    except TypeError as e:
        missive({
            "success": False,
            "error_type": "TypeError", 
            "error_message": str(e),
            "hint": "Check function signatures and parameter names"
        })
    except Exception as e:
        import traceback
        missive({
            "success": False,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        })

safe_execute()
```

### Solution 6: Browser Console Enhancement
Add a global error handler for better visibility:

```javascript
// Add to your main JavaScript file
window.addEventListener('error', (event) => {
  if (event.error && event.error.toString().includes('Python')) {
    console.group('🐍 Python Error Detected');
    console.error('Message:', event.message);
    console.error('Source:', event.filename);
    console.error('Line:', event.lineno);
    console.error('Column:', event.colno);
    console.error('Error Object:', event.error);
    console.groupEnd();
  }
});
```

## Implementation Priority

1. **Immediate**: Fix Solution 1 (JavaScript error logging) - easiest to implement
2. **High**: Add Solution 2 (Python try-catch wrapper) to problematic generators
3. **Medium**: Implement Solution 3 (Debug mode) for development
4. **Low**: Add Solutions 4-6 for comprehensive error handling

## Testing Error Handling

To test if error handling is working:

1. **Intentional KeyError**:
```python
components = {"k": 1, "factor": 2}
print(components["missing_key"])  # Will trigger KeyError
```

2. **Intentional TypeError**:
```python
def func(a, b):
    return a + b
func(1)  # Missing required argument
```

3. **Check Console Output**:
- Should see detailed Python traceback
- Should see line numbers
- Should see variable states if possible

## Common Pyodide Error Patterns

### Pattern 1: Parameter Mismatch
**Error**: `TypeError: render_question() got an unexpected keyword argument 'k'`
**Cause**: Function signature doesn't match passed parameters
**Fix**: Ensure function parameters match what's being unpacked

### Pattern 2: Missing Import
**Error**: `NameError: name 'random' is not defined`
**Cause**: Module not imported or not available in Pyodide
**Fix**: Add import or check Pyodide package availability

### Pattern 3: Attribute Error
**Error**: `AttributeError: 'NoneType' object has no attribute 'latex'`
**Cause**: Function returned None instead of expected object
**Fix**: Add null checks and default returns

## Specific Fix for spe_sujet2_auto_06_question.py

### Current Issues
1. **Parameter Mismatch**: `render_question` expects `prefix_joules_to_multiply_by_power` and `power`
2. **Component Keys**: `generate_components` returns `k` and `factor`
3. **Missive Access**: Trying to access non-existent keys in lines 118-121

### Required Fixes

**Option 1: Update render_question to match new structure**
```python
def render_question(*, k, factor):
    """Render question with k and factor parameters"""
    # Extract parts from k if it's in form x * 10^n
    # k is Mul(l=Integer, r=Pow(base=10, exp=n))
    
    statement = f"Un appareil a besoin d'une énergie de ${k.latex()}$ Joules (J) pour se mettre en route. À combien de kiloWatt-heure (kWh) cela correspond-il? On donne $1kWh={factor.latex()}J$."
    
    return {
        "statement": statement,
    }
```

**Option 2: Fix the components in missive**
```python
missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-6]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "k": components["k"].latex(),
            "factor": components["factor"].latex(),
        },
    }
)
```

## Debugging Workflow

1. **Enable verbose logging** in JavaScript
2. **Add try-catch** in Python code
3. **Check browser console** for full error details
4. **Look for stderr output** which contains tracebacks
5. **Fix parameter mismatches** based on error messages
6. **Test with seed variations** to ensure robustness

## References
- [Pyodide Error Handling Docs](https://pyodide.org/en/stable/usage/api/python-api.html#error-handling)
- [JavaScript Error Event](https://developer.mozilla.org/en-US/docs/Web/API/Window/error_event)
- [Python traceback module](https://docs.python.org/3/library/traceback.html)
