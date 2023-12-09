import re
from enum import Enum

# Enum for debate topic
class Category(Enum):
    CULTURE = "culture"
    DIGITAL_FREEDOMS = "digital-freedoms"
    ECONOMY = "economy"
    EDUCATION = "education"
    ENVIRONMENT = "environment"
    FREE_SPEECH_DEBATE = "free-speech-debate"
    HEALTH = "health"
    INTERNATIONAL = "international"
    LAW = "law"
    PHILOSOPHY = "philosophy"
    POLITICS = "politics"
    RELIGION = "religion"
    SCIENCE = "science"
    SOCIETY = "society"
    SPORT = "sport" 
    
    
# Enum for argument type
class ArgumentType(Enum):
    PRO = "pro"
    CON = "con"
    
    
# Extract arguments from category file: debate_topic.txt -> full.txt
def debate_extract_arguments(
    category: Category,
    file_path: str,
    start_re: str = "# PRO",
    end_re: str = "# LITERATURE",
    pro_point_re: str = "# PRO\w+-POINT",
    pro_counter_re: str = "# PRO\w+-COUNTER",
    con_point_re: str = "# CON\w+-POINT",
    con_counter_re: str = "# CON\w+-COUNTER"
    ) -> {}:
    # try to open file from path
    try:
        with open('../' + 'arguana-counterargs-corpus/' + '02-extracted-arguments/' + 'training/' +
                  category.value + '/' + file_path + '/' + 'full.txt', 'r') as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path + '.txt'}")
        return None
    # parse file contents
    lines: [] = re.split(r'\n', file_contents)
    # holds the extracted arguments for the debate topic
    debate_arguments = {}
    # holds the argument pairs data for the debate topic
    arguments = {
        'pro': [],
        'con': []
    }
    # Start looping through lines
    current_argument: str = ""
    start: bool = False
    current_argument_type = ArgumentType.PRO
    cur_pair = {}

    for line in lines:
        # skip to start line
        if (not start):
            if re.match(r'\s*' + start_re, line):
                start = True
                continue
            continue
        
        # special case when we reach # LITERATURE we append the last argument and return
        if re.match(r'\s*' + end_re, line):
            if len(cur_pair):
                cur_pair['counter'] = current_argument
            else:
                cur_pair["point"] = current_argument
            arguments['con'].append(cur_pair)
            arguments_write_to_file(category.value, file_path, arguments)
            debate_arguments[file_path] = arguments
            return debate_arguments

        # skip citations
        if re.match(r'\s*\[', line):
            continue

        # case where we meet a pro counter -> finish a pro point
        if re.match(r'\s*' + pro_counter_re, line):
            cur_pair['point'] = current_argument
            current_argument = ""
            continue
        # case where we meet a pro point -> finish a pro counter
        elif re.match(r'\s*' + pro_point_re, line):
            cur_pair['counter'] = current_argument
            arguments["pro"].append(cur_pair)
            current_argument = ""
            cur_pair = {}
            continue
        # case where we meet a con counter -> finish a con point
        elif re.match(r'\s*' + con_counter_re, line):
            cur_pair['point'] = current_argument
            current_argument = ""
            continue
        # case where we meet a con point -> finish a con counter
        elif re.match(r'\s*' + con_point_re, line):
            cur_pair['counter'] = current_argument
            if current_argument_type == ArgumentType.PRO:
                arguments["pro"].append(cur_pair)
                current_argument_type = ArgumentType.CON
            else:
                arguments["con"].append(cur_pair)
            current_argument = ""
            cur_pair = {}
            continue
        
        # remove in-text citations
        line = re.sub(r'\[\w+\]', '', line)
        line = re.sub(r'\s\s+', '', line)
        current_argument += line.strip()
    # this should never actually be reached
    arguments_write_to_file(category.value, file_path, arguments)
    debate_arguments[file_path] = arguments
    return debate_arguments
    
        
# Extract all debates from a category: list_of_<category>_debates.txt -> <debate_topic>.txt
def category_extract_arguments(category: Category) -> {}:
    # convert category.value to path syntax
    category_path = category.value.replace('_', '-')
    # try to open file from path
    try:
        with open('./' + 'file_paths/' + 'list_of_/' + category_path + '_debates.txt', 'r') as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"File not found: {'list_of_/' + category_path + '_debates.txt'}")
        return None
    # parse file contents
    debates: [] = re.split(r'\n', file_contents)
    # grab arguments for each debate in the category
    category_arguments = {}
    for debate in debates:
        # add topic and arguments to category_arguments
        category_arguments.update(debate_extract_arguments(category, debate))
    return {category.value: category_arguments}
    
    
# Extract all debates across all categories: all_categories.txt -> list_of_<category>_debates.txt
def global_extract_arguments() -> {}:
   # open global file from path
    with open('./file_paths/all_categories.txt', 'r') as global_file:
        global_file_contents = global_file.read()
    # parse file contents
    category_pattern = re.compile(r'list_of_(\w+)_debates')
    lines: [] = re.split(r'\n', global_file_contents)
    category_paths = [line for line in lines if category_pattern.search(line)]
    category_names = [category_pattern.search(category).group(1).upper() for category in category_paths]
    # key: category: Category.value
    # value: dictionary of dictionaries where key = topic and value is {'pro: [{'point':, 'counter':}, ...], 'con': []}
    global_arguments = {} 
    # add valid topics as keys to extracted_categories
    for category_path, category_name in enumerate(zip(category_paths, category_names)):
        try:
            category = Category[category_name]
            global_arguments.update(category_extract_arguments(category))
        except KeyError:
            print(f"Category: {category_name}, Category not found in Category enum and is removed.")
            category_paths.remove(category_path)
            category_names.remove(category_name)
    return global_arguments


# Write extracted arguments to file
def _arguments_write_to_file(debate_topic: str, file_path: str, arguments: dict):
    file = open('../' + 'data_dump/' + 'arguments_dump/'
                + debate_topic + '/' + file_path + '.txt', "w")
    file.write("# PRO arguments:\n")
    for pair in arguments["pro"]:
        file.write('point: ' + pair['point'] + "\n")
        file.write('counter: ' + pair['counter'] + "\n")
    file.write("# CON arguments:\n")
    for pair in arguments["pro"]:
        file.write('point: ' + pair["point"] + "\n")
        file.write('counter: ' + pair["counter"] + "\n")
    file.close()