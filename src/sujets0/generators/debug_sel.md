


## Generic notes : 

- We generate 100 questions per generator. 
    - If high number of errors, like even 100: probably adjustement in teachers cause they used to work with Doppel
    - If low number of errors, like 10: probably adjustement in generator cause some specific values break stuff (like when a percentage becomes 100% -> Integer...)
        - We'lll adjust those laters


## gen_sujet1_auto_01_question.py

### Diag 

- Same errors, but not always
- AttributeError: 'Integer' object has no attribute 'as_percent'

### Fix from generator
- `x = gen.random_integer(1, 20)` --> `x = gen.random_integer(1, 19)`





## gen_sujet1_auto_06_question.py

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



