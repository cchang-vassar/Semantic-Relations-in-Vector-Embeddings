import re

def check_unique_file_paths(file_path: str) -> bool:
    try:
        with open('./' + file_path + '.txt', 'r') as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path + '.txt'}")
        return None

    lines: [] = re.split(r'\n', file_contents)
    
    length = 0
    unique = set()

    for line in lines:
        length += 1
        unique.add(line)
    
    return len(unique)

results = check_unique_file_paths("list_of_all_debates")
print(results)