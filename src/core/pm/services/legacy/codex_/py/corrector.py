from io import StringIO
from pprint import pprint
import sys
import typing
import unittest

# Get the currently focused/active element


# from app.services.v1.teachers.composers.python_composer import PythonComposer


# def init_python_corrector():
#     return PythonCorrector()


class PythonCorrector:
    def __init__(self, background_script):
        self.background_script = background_script
        self.last_error: str | None = None
        self.testcase = unittest.TestCase()
        self.check_counter = 0
        self.correction = {}
        # TODO: move this in the teacher class
        # Create a StringIO object to capture output
        self.original_stdout = sys.stdout
        # self.stdout = StringIO()
        # sys.stdout = self.stdout
        self.stdout = sys.stdout

        # if pyodide
        # todo : write surcouche pour data get

        print(sys.platform)

        #     print(codex_id)
        #     # load the data-background-script with js
        #     self.background_script = ""
        #     # js.globals.data_background_script

        #     self.background_script = document.activeElement.id

    def __del__(self):
        sys.stdout = sys.__stdout__

    @staticmethod
    def gracefully_check(check_method):
        def wrapper(self, *args, **kwargs):
            try:
                check_method(self, *args, **kwargs)
                success, msg = 1, ""
            except AssertionError as e:
                success, msg = 0, str(e)

            self.check_counter += 1
            self.correction[self.check_counter] = (success, msg)
            return success, msg

        return wrapper

    def check_coincide(self, x: typing.Any) -> None:
        namespace = {}
        exec(self.background_script, namespace)
        # TODO : SAME SETUP FOR ALL BECAUSE OF AUTOFORMAT
        x_name = f"{x=}".split("=")[0]
        self.check_equal(x, namespace[x_name])

    @gracefully_check
    def check_equal(self, x: typing.Any, y: typing.Any) -> None:
        # First check if types match
        self.testcase.assertIsInstance(x, type(y))
        # Booleans
        if isinstance(x, bool):
            self.testcase.assertEqual(x, y)
        # Strings
        if isinstance(x, str):
            self.testcase.assertEqual(x, y)
        # Numbers
        elif isinstance(x, int):
            self.testcase.assertEqual(x, y)
        elif isinstance(x, float):
            self.testcase.assertAlmostEqual(x, y)
        # Sequences
        elif isinstance(x, list):
            self.testcase.assertListEqual(x, y)
        elif isinstance(x, tuple):
            self.testcase.assertTupleEqual(x, y)
        elif isinstance(x, set):
            self.testcase.assertSetEqual(x, y)
        # Dictionaries
        elif isinstance(x, dict):
            self.testcase.assertDictEqual(x, y)
        # Handle None
        elif x is None:
            self.testcase.assertIsNone(y)
        # Default case
        else:
            # raise NotImplementedError(f"PythonCorrector cannot compare {type(x)=}")
            self.testcase.assertEqual(x, y)

    @gracefully_check
    def check_equals_on_grid(self, f, args, values):
        for x, y in zip(args, values, strict=False):
            self.testcase.assertEqual(f(x), y)

    @gracefully_check
    def check_module_is_imported(self, module_name, teacher):
        # TODO mad: handle from_imports
        self.testcase.assertIn(module_name, teacher.story["user_input"]["imports"]["imports"])

    def check_stdout_equals(self, x):
        # NOTE mad: no need for the `gracefully_check` decorator as the `check_equal` method is used
        stdout = self.stdout.getvalue()
        stdout = stdout.strip().replace("\n", "")
        x = x.strip().replace("\n", "")
        self.check_equal(stdout, x)

    def check_nb_lines(self): ...

    # TODO: mad
    # check if nb lines consistent with sections
    # check if nb lines ==

    def correct(self) -> bool:
        ...
        # TODO: ideally the checks would be performed there
        # answer_nature = answer["nature"].split("_")
        # return self.correction


#################
# DRAFT
#################

# class LoopCounter(ast.NodeVisitor):
#     def __init__(self):
#         self.count = 0

#     def visit_For(self, node):
#         self.count += 1
#         self.generic_visit(node)


#     # def contains_for_statement(self, code_ast: ast.Module) -> bool:
#     #     counter = LoopCounter()
#     #     counter.visit(code_ast)
#     #     return counter.count > 0
