import os

def read_project_code(directory):
    """
    Reads all Python files in the given directory and returns a dictionary 
    with filenames as keys and file contents as values.
    """
    code_files = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):  # Read only Python files
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    code_files[file] = f.read()
    
    return code_files
