import ast
import re
import yaml

from pathlib import Path

def fetch_docstrings():
    JS_FILE_PATH="./js_spec_v2.yml"
    # TODO: Make path lib configurable based on client lib
    py_file = Path("../gotrue-py/gotrue/_sync/client.py")
    raw_tree = py_file.read_text()
    tree = ast.parse(raw_tree)
    functions = [f for f in ast.walk(tree) if isinstance(f, ast.FunctionDef)]
    py_func_names = [f.name for f in functions]
    # For each function
    js_function_reference = fetch_js_function_list(JS_FILE_PATH)
    function_docs = [ast.get_docstring(f) for f in functions]
    # fetch function names
    js_func_names = [x.get('title').split(".")[-1].strip("()") for x in js_function_reference if x.get('title') is not None]
    output = {'pages':{}}
    for function in functions:
        pyfunc_as_camel = snake_to_camel_case(function.name)
        if pyfunc_as_camel in js_func_names:
            print(f"{pyfunc_as_camel}")
            output = add_yml_entry(output, function.name, pyfunc_as_camel, js_function_reference)

    with open('./py_spec_v2.yml', 'w') as pyspec:
        yaml.dump(output, pyspec)

    # return function_docs

def add_yml_entry(output, function_py_name,js_func_name, js_function_reference):
    # Top Level entry is pages
    matching_title = list(filter(lambda ref: ref.get('title_without_prefix') == js_func_name, js_function_reference))
    if len(matching_title) > 0:
        output['pages'][function_py_name] = matching_title
    return output

def fetch_js_function_list(spec_path: str):
    func_list = []
    # We used res['pages']['storage.from.createSignedUrl()'] to get an example of what ot load
    fields_to_copy = ['$ref', 'description', 'examples']
    with open(spec_path, "r") as stream:
        try:
            yml = yaml.safe_load(stream)
            top_level = yml['pages'].values()
            top_level_title = list(yml['pages'].keys())
            for index,entry in enumerate(top_level):
                func_entry = {}
                func_entry['title'] = top_level_title[index]
                # Remove the "auth." in  "auth.signUp". We also remove ()
                func_entry['title_without_prefix'] = top_level_title[index].split(".")[-1].strip("()")
                if entry.get('$ref'):
                    for field in fields_to_copy:

                        func_entry[field] = entry.get(field)
                func_list.append(func_entry)
        except yaml.YAMLError as exc:
            print(exc)
    return func_list

def is_valid_function_name(name):
    pass

def snake_to_camel_case(snake_str):
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])

if __name__ == "__main__":
    s = fetch_docstrings()
