# Supa-ref-generator


This is intended to be a reference generator for the Supabase-py lib. 

It should take in the existing Supabase-js v2 spec and generate the corresponding function definitions and example usage for the Python client library. It does so by parsing the Python source into an AST and then uses the docstring associated with functions to generate the resulting yml file.
