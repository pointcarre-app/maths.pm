import ast
import inspect

from .corrector import PythonCorrector

# Get source of the module containing PythonCorrector
python_corrector_module_source = inspect.getsource(inspect.getmodule(PythonCorrector))

# Parse the source code into an AST
python_corrector_tree = ast.parse(python_corrector_module_source)


# Function to extract imports
def get_imports(tree):
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            for alias in node.names:
                imports.append(f"from {module} import {alias.name}")
    return imports


corrector_imports = get_imports(python_corrector_tree)
corrector_imports_source = "\n".join(corrector_imports).replace('"', "'")


corrector_source = inspect.getsource(PythonCorrector).replace('"', "'")
corrector_source = corrector_source.replace('"', "'")


# Now modify your PythonComposer class
class PythonComposer:
    def __init__(self):
        pass

    def compose(self, foreground_script, background_script, publics_checks, privates_checks):
        # print(publics_checks)
        # print(privates_checks)
        composed_codex = f"""# _________________foreground_script_________________
{foreground_script}

# _________________corrector_________________
{corrector_imports_source}
{corrector_source}
_pc = PythonCorrector('{background_script}')

# _________________public_checks_________________
{publics_checks}

# _________________private_checks_________________
{privates_checks}"""
        return composed_codex


# # Method 1: Using inspect module (best for getting source of functions/classes)
# import inspect


# from app.services.v1.teachers.codex.py.python_corrector import PythonCorrector


# class PythonComposer:
#     def __init__(self):
#         pass

#     def compose(self, foreground_script, background_script, publics_script, privates_script):
#         composed_codex = f"""# _________________foreground_script_________________
# {foreground_script}

# # _________________background_script_________________
# {corrector_source}
# {background_script}

# # _________________public_checks_________________
# {publics_script}

# # _________________private_checks_________________
# {privates_script}"""
#         return composed_codex
