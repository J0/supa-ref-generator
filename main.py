import ast
import re
from pathlib import Path

def fetch_docstrings():
    JS_FILE_PATH="./js_v2_spec.yml"
    # TODO: Make path lib configurable based on client lib
    py_file = Path("../gotrue-py/gotrue/_sync/client.py")
    raw_tree = py_file.read_text()
    tree = ast.parse(raw_tree)
    functions = [f for f in ast.walk(tree) if isinstance(f, ast.FunctionDef)]
    # For each function
    js_function_reference = fetch_js_function_list(JS_FILE_PATH)
    function_docs = [ast.get_docstring(f) for f in functions]
    res = []
    for function in functions:
        if snake_to_camel_case(function) in js_function_reference:
            yml_entry = create_yml_entry(function)
            res.append(yml_entry)

    # Write res to yml file

    return function_docs

def create_yml_entry():
    pass

def fetch_js_function_list(spec):
    # Get the spec
    pass

def is_valid_function_name(name):
    pass

def snake_to_camel_case(name):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    name = pattern.sub('_', name).lower()
    return name

if __name__ == "__main__":
    s = fetch_docstrings()
