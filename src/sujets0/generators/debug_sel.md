# Debug in lexicographic order the errors in the generators



## Generic notes : 

- We generate 100 questions per generator. 
    - If high number of errors, like even 100: probably adjustement in teachers cause they used to work with Doppel
    - If low number of errors, like 10: probably adjustement in generator cause some specific values break stuff (like when a percentage becomes 100% -> Integer...)
        - We'lll adjust those laters

**BUT SOMETIMES it's different**


## Stucture:

```markdown
## Filename

### Diag

- Error message

### Fix from generator / Fix from teachers

- Details (tagged version / changelog / updates in generators)


```





## `gen_sujet1_auto_01_question.py`

### Diag 

- Same errors, but not always
- AttributeError: 'Integer' object has no attribute 'as_percent'

### Fix from generator itself
- `x = gen.random_integer(1, 20)` --> `x = gen.random_integer(1, 19)`




## `gen_sujet1_auto_06_question.py`

### Diag


```bash
Erreur de génération
1 validation error for Integer n Input should be a valid integer, got a number with a fractional part [type=int_from_float, input_value=0.0001, input_type=float] For further information visit https://errors.pydantic.dev/2.11/v/int_from_float
Type: ValidationError
Traceback complet
Traceback (most recent call last):
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 114, in generate_question
    module = load_generator_module(generator_file)
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 46, in load_generator_module
    spec.loader.exec_module(module)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "", line 1026, in exec_module
  File "", line 488, in _call_with_frames_removed
  File "/Users/selim/madles/pca-mathspm/src/sujets0/generators/gen_sujet1_auto_06_question.py", line 64, in 
    components = generate_components(None)
  File "/Users/selim/madles/pca-mathspm/src/sujets0/generators/gen_sujet1_auto_06_question.py", line 21, in generate_components
    b = b.simplified().as_decimal
        ~~~~~~~~~~~~^^
  File "/Users/selim/madles/pca-teachers/src/teachers/maths.py", line 753, in simplified
    return Integer(n=n1**n2)
  File "/Users/selim/madles/pca-mathspm/env/lib/python3.13/site-packages/pydantic/main.py", line 253, in __init__
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
pydantic_core._pydantic_core.ValidationError: 1 validation error for Integer
n
  Input should be a valid integer, got a number with a fractional part [type=int_from_float, input_value=0.0001, input_type=float]
    For further information visit https://errors.pydantic.dev/2.11/v/int_from_float
```



### Fix from teachers 

- In maths.py, we have now : 


```python
    @field_validator("base", mode="before")
    @classmethod
    def format_base(cls, value: int | MathsObject) -> MathsObject:
        if isinstance(value, int):
            return Integer(n=value)
        elif isinstance(value, MathsObject):
            return value
        else:
            raise NotImplementedError(f"Unsupported base type: {type(value)}")

    @field_validator("exp", mode="before")
    @classmethod
    def format_exp(cls, value: int | MathsObject) -> MathsObject:
        if isinstance(value, int):
            return Integer(n=value)
        elif isinstance(value, MathsObject):
            return value
        else:
            raise NotImplementedError(f"Unsupported exp type: {type(value)}")

```



## `gen_sujet1_auto_11_question.py`


### Diag

- Interaction in between specific `tm.maths` objects not dealt with



```bash
Simplification of Mul of <class 'teachers.maths.Integer'> and <class...
```


```bash
Traceback complet:
Traceback (most recent call last):
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 114, in generate_question
    module = load_generator_module(generator_file)
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 46, in load_generator_module
    spec.loader.exec_module(module)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/selim/madles/pca-mathspm/src/sujets0/generators/gen_sujet1_auto_11_question.py", line 72, in <module>
    "simplified_latex": answer["maths_object"].simplified().latex(),
                        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/Users/selim/madles/pca-teachers/src/teachers/maths.py", line 796, in simplified
    return l ** Integer(n=2) + (Integer(n=2) * l * r).simplified() + r ** Integer(n=2)
                               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/Users/selim/madles/pca-teachers/src/teachers/maths.py", line 523, in simplified
    l, r = self.l.simplified(), self.r.simplified()
           ~~~~~~~~~~~~~~~~~^^
  File "/Users/selim/madles/pca-teachers/src/teachers/maths.py", line 573, in simplified
    raise NotImplementedError(
        f"Simplification of Mul of {type(l)} and {type(r)}\n{l=}\n{r=}"
    )
NotImplementedError: Simplification of Mul of <class 'teachers.maths.Integer'> and <class 'teachers.maths.Mul'>
l=Integer(n=2)
r=Mul(l=Integer(n=3), r=Symbol(s='x'))

```


### Fix from teachers

- Interaction in between specific `tm.maths` not implement 
- And tested in `teachers/tests/test_mul_simplification.py`

```markdown
## [0.0.8] - 2025-01-16

### Fixed
- **Critical Mul Simplification Bug**: Fixed NotImplementedError when simplifying nested multiplication operations
  - `Mul.simplified()` now correctly handles `Integer * Mul(Integer, Symbol)` combinations in both orders
  - Added support for `Mul(Integer, Symbol) * Integer` combinations  
  - Added distributive property handling for nested Mul objects
  - Resolved the original bug where polynomial expansions like `(ax + b)^2` would fail during simplification
  - Added zero multiplication simplification (`0 * anything = 0`)
```




## `gen_sujet2_auto_02_question.py``



### Diag 

- Sometimes the value returned by `simplified()` is an `Integer` object, not a `Fraction` object
- And `Integer` object has (had) no attribute `as_decimal`

```bash
Erreur de génération
'Integer' object has no attribute 'as_decimal'
Type: AttributeError
```


```bash
Traceback complet
Traceback (most recent call last):
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 114, in generate_question
    module = load_generator_module(generator_file)
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 46, in load_generator_module
    spec.loader.exec_module(module)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "", line 1026, in exec_module
  File "", line 488, in _call_with_frames_removed
  File "/Users/selim/madles/pca-mathspm/src/sujets0/generators/gen_sujet2_auto_02_question.py", line 61, in 
    question = render_question(**components)
  File "/Users/selim/madles/pca-mathspm/src/sujets0/generators/gen_sujet2_auto_02_question.py", line 50, in render_question
    p1 = (p * n1).simplified().as_decimal
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/selim/madles/pca-mathspm/env/lib/python3.13/site-packages/pydantic/main.py", line 991, in __getattr__
    raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}')
AttributeError: 'Integer' object has no attribute 'as_decimal'
```




### Fix from teachers

```markdown
## [0.0.9] - 2025-01-16

### Fixed
- **Critical as_decimal Property Bug**: Fixed AttributeError when accessing as_decimal property on Integer objects
  - `Integer.as_decimal` property now returns a properly formatted `Decimal` object
  - Resolved the original bug where expressions like `(p * n1).simplified().as_decimal` would fail with "Integer object has no attribute 'as_decimal'"
  - Fixed in 27% of generator scenarios that were failing with this error

### Enhanced
- **Clean Decimal LaTeX Output**: Improved `Decimal.latex()` method for cleaner mathematical notation
  - Whole numbers now render without decimal points: `5.0` → `"5"` instead of `"5.0"`
  - Changed decimal separator from comma to period: `3,14` → `"3.14"` for international compatibility
  - Eliminates unwanted decimal formatting in educational content
````





## `gen_sujet2_auto_03_question.py`


### Diag


**Teachers error**

```bash
Erreur de génération
'Integer' object has no attribute 'as_percent'
Type: AttributeError
```

**Traceback**


```bash
Traceback (most recent call last):
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 114, in generate_question
    module = load_generator_module(generator_file)
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 46, in load_generator_module
    spec.loader.exec_module(module)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "", line 1026, in exec_module
  File "", line 488, in _call_with_frames_removed
  File "/Users/selim/madles/pca-mathspm/src/sujets0/generators/gen_sujet2_auto_03_question.py", line 60, in 
    answer = solve(**components)
  File "/Users/selim/madles/pca-mathspm/src/sujets0/generators/gen_sujet2_auto_03_question.py", line 30, in solve
    maths_object = (n-tm.Integer(n=1)).simplified().as_percent
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/selim/madles/pca-mathspm/env/lib/python3.13/site-packages/pydantic/main.py", line 991, in __getattr__
    raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}')
AttributeError: 'Integer' object has no attribute 'as_percent'
```


### Fix from teachers


```markdown
## [0.0.10] - 2025-01-16

### Fixed
- **Critical as_percent Property Bug**: Fixed AttributeError when accessing as_percent property on Integer objects
  - `Integer.as_percent` property now returns a properly formatted `Integer` object (multiply by 100)
  - Resolved the bug where expressions like `(n-tm.Integer(n=1)).simplified().as_percent` would fail with "Integer object has no attribute 'as_percent'"
  - Consistent with existing `Fraction.as_percent` behavior
  - Critical fix for generator scripts that were failing in production

```




## `gen_sujet2_auto_06_question.py`


### Diag

*Only one error for:Seed: 63 | Échec ✗*

```bash
Erreur de génération
1 validation error for Fraction q Value error, Denominator cannot be zero [type=value_error, input_value=Integer(n=0), input_type=Integer] For further information visit https://errors.pydantic.dev/2.11/v/value_error
Type: ValidationError
```


```bash
Traceback complet
Traceback (most recent call last):
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 114, in generate_question
    module = load_generator_module(generator_file)
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 46, in load_generator_module
    spec.loader.exec_module(module)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "", line 1026, in exec_module
  File "", line 488, in _call_with_frames_removed
  File "/Users/selim/madles/pca-mathspm/src/sujets0/generators/gen_sujet2_auto_06_question.py", line 67, in 
    "simplified_latex": answer["maths_object"].simplified().latex(),
                        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/Users/selim/madles/pca-teachers/src/teachers/maths.py", line 701, in simplified
    return Fraction(p=p, q=q)
  File "/Users/selim/madles/pca-mathspm/env/lib/python3.13/site-packages/pydantic/main.py", line 253, in __init__
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
pydantic_core._pydantic_core.ValidationError: 1 validation error for Fraction
q
  Value error, Denominator cannot be zero [type=value_error, input_value=Integer(n=0), input_type=Integer]
    For further information visit https://errors.pydantic.dev/2.11/v/value_error
```


### Fix from generator itself

- Ensure x1 ≠ x2 in the generator: modified generate_components function to guarantee that x1 and x2 are different
    - while strategy is safe: 


```python

def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-8]
    >>> generate_components(None, 0)
    {'x1': Integer(n=-2), 'y1': Integer(n=7), 'x2': Integer(n=94), 'y2': Integer(n=-90)}
    """

    gen = tg.MathsGenerator(seed)

    x1 = gen.random_integer(-100, 100)
    x2 = gen.random_integer(-100, 100)


    # 🧂 Ensure x2 ≠ x1 added this to avoid division by zero in solve
    while x2.n == x1.n:
        x2 = gen.random_integer(-100, 100)

    y1 = gen.random_integer(-100, 100)
    y2 = gen.random_integer(-100, 100)

    return {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
    }
```



## `gen_sujet3_auto_05_question.py`



### Diag


```bash
Erreur de génération
Simplification of Mul of and l=Decimal(p=23, q=25) r=Function(name=V)(Symbol(s='n'))
Type: NotImplementedError
Traceback complet
```


### Fix from teachers



```markdown

## [0.0.12] - 2025-01-16

### Enhanced
- **Mul.simplified() Extensions**: Added comprehensive Pi multiplication cases
  - `Integer * Pi` and `Pi * Integer` combinations
  - `Decimal * Pi` and `Pi * Decimal` combinations  
  - `Fraction * Pi` and `Pi * Fraction` combinations
  - `Pi * Pow` combinations for expressions like π * r²
  - Proper coefficient ordering maintains mathematical notation standards

```



## `gen_sujet2_auto_09_question.py`


### Diag


```bash
Erreur de génération
module 'teachers.maths' has no attribute 'Pi'
Type: AttributeError
```

```bash
Traceback (most recent call last):
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 114, in generate_question
    module = load_generator_module(generator_file)
  File "/Users/selim/madles/pca-mathspm/src/build_questions.py", line 46, in load_generator_module
    spec.loader.exec_module(module)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "", line 1026, in exec_module
  File "", line 488, in _call_with_frames_removed
  File "/Users/selim/madles/pca-mathspm/src/sujets0/generators/gen_sujet2_auto_09_question.py", line 55, in 
    components = generate_components(None)
  File "/Users/selim/madles/pca-mathspm/src/sujets0/generators/gen_sujet2_auto_09_question.py", line 18, in generate_components
    r=tm.Fraction(p=1, q=3) * tm.Pi() * r**tm.Integer(n=2) * h,
                              ^^^^^
AttributeError: module 'teachers.maths' has no attribute 'Pi'
```


### Fix from teachers


```markdown
## [0.0.12] - 2025-01-16

### Added
- **Pi (π) Mathematical Constant**: New `Pi` class for geometric calculations and mathematical formulas
  - Full SymPy integration with `sp.pi` for exact symbolic computation
  - Proper LaTeX rendering (`\\pi`) with coefficient-first notation (2π, (1/3)π, 0.5π)
  - Numerical evaluation matching `math.pi` for calculations
  - Complete multiplication support with Integer, Decimal, and Fraction coefficients
  - Addition operations with other mathematical objects
  - Perfect for geometric formulas: circle area (πr²), circumference (2πr), volumes ((4/3)πr³)

```