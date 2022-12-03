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
    # For each function
    js_function_reference = fetch_js_function_list(JS_FILE_PATH)
    function_docs = [ast.get_docstring(f) for f in functions]
    res = []
    # for function in functions:
    #     if snake_to_camel_case(function) in js_function_reference:
    #         yml_entry = create_yml_entry(function)
    #         res.append(yml_entry)

    # Write res to yml file
    import pdb;pdb.set_trace()
    with open('./py_spec_v2.yml', 'w') as pyspec:
        yaml.dump(spec_dict, pyspec)

    return function_docs

def create_yml_entry():
    # If it has a ref, we grad the title, examples and name.
    # To determine the name we split by "." and take the last entry
    pass

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
                if entry.get('$ref'):
                    for field in fields_to_copy:

                        func_entry[field] = entry.get(field)
                func_list.append(func_entry)
        except yaml.YAMLError as exc:
            print(exc)
    return func_list

def is_valid_function_name(name):
    pass

def snake_to_camel_case(name):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    name = pattern.sub('_', name).lower()
    return name

if __name__ == "__main__":
    s = fetch_docstrings()
