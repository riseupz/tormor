import os

# Current directory path
MYDIR = os.path.dirname(os.path.abspath(__file__))

def get_schema_path():
    for root, dirs, files in os.walk(os.ge):
        if "schema" in root.lower():
            return root
    return None

def find_schema_paths():
    return None