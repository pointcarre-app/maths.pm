import ast
import html


class PythonParser:
    def __init__(self):
        pass

    def split_codex_str(self, code_str: str):
        """Splits a file content based on sections marked with # _________________ and ending with _________________
        Returns a dictionary with section names as keys and their content as values
        """
        # Initialize variables
        current_section = None
        current_content = []
        sections = {
            "foreground_script": "",
            "background_script": "",
            "private_checks": "",
            "public_checks": "",
        }

        # print("SPLITTING CODE STR", type(code_str))
        # if type(code_str) is not str:
        #     from pprint import pprint

        #     pprint(code_str)
        #     raise Exception("GOTCHA")

        # Process each line
        for line in code_str.split("\n"):
            # Check if line starts a new section
            if line.startswith("# _________________") and line.endswith("_________________"):
                # If we were already in a section, save it
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()
                    current_content = []

                # Extract new section name
                current_section = (
                    line.replace("# _________________", "").replace("_________________", "").strip()
                )
                if current_section not in [
                    "foreground_script",
                    "background_script",
                    "public_checks",
                    "private_checks",
                    "corrector",
                ]:
                    raise ValueError(f"{current_section=}")
            elif current_section:
                current_content.append(line)

        # Don't forget to save the last section
        if current_section and current_content:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    def get_imports(self, code_str):
        # Parse the code string into an AST
        tree = ast.parse(code_str)

        # Lists to store different types of imports
        imports_std = []
        from_imports = []

        # Walk through the AST nodes
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports_std.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    from_imports.append(f"from {module} import {alias.name}")

        return imports_std, from_imports

    def parse(self, code_str: str):
        # print("PARSING CODE STR", type(code_str))
        # TODO sel: when reading script after file.read, should user html.escape
        # TODO sel: should have a mode using inspect to read the code
        sections = self.split_codex_str(code_str)
        asts = {}
        asts["foreground_script"] = ast.parse(html.unescape(sections["foreground_script"]))
        asts["background_script"] = ast.parse(html.unescape(sections["background_script"]))
        asts["private_checks"] = ast.parse(html.unescape(sections["private_checks"]))
        asts["public_checks"] = ast.parse(html.unescape(sections["public_checks"]))
        return sections, asts
