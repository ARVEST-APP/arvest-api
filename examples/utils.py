import os
import json

def read_txt(path : str) -> str:
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() == ".txt":
            with open(path, 'r') as f:
                return f.read()
        else:
            print(f"{path} is not a text file.")
            return None
    else:
        print(f"{path} doesn't exist.")
        return None
    
def read_login(path: str):
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() == ".txt":
            with open(path, 'r') as file:
                lines = file.readlines()
            lines = [line.strip() for line in lines]

            return lines[0], lines[1]
        else:
            print(f"{path} is not a text file.")
            return None, None
    else:
        print(f"{path} doesn't exist.")
        return None, None
    
def write_json(path : str, content : dict, indent : int = 4) -> None:
    """
    Write to json. Will create folder if doesn't exist.
    """
    if os.path.splitext(path)[1] == ".json":
        check_dir_exists(path)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii = False, indent = indent)
    else:
        print(f"{path} needs to be a json file.")

def check_dir_exists(filepath):
    """Check if folder exists, if not, create it."""
    if os.path.isdir(os.path.dirname(filepath)) == False:
        os.makedirs(os.path.dirname(filepath))