import os

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