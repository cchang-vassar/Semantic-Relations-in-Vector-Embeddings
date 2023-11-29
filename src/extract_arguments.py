import re
from enum import Enum


# Enum for debate topic
class DebateTopic(Enum):
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
    
class ArgumentType(Enum):
    PRO = "pro"
    CON = "con"
    
    
# Extract arguments from .txt file
def extract_arguments(
    debate_topic: str,
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
                  debate_topic + '/' + file_path + '/' + 'full.txt', 'r') as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path + '.txt'}")
        return None

    lines: [] = re.split(r'\n', file_contents)
    arguments = {
        'pro': [],
        'con': []
    }
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
            # arguments_write_to_file(debate_topic, file_path, arguments)
            return arguments

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


# Write extracted arguments to file
def arguments_write_to_file(debate_topic: str, file_path: str, extracted_arguments: dict):
    file = open('../' + 'data_dump/' + 'arguments_dump/'
                + debate_topic + '/' + file_path + '.txt', "w")
    file.write("# PRO arguments:\n")
    for pair in extracted_arguments["pro"]:
        file.write('point: ' + pair['point'] + "\n")
        file.write('counter: ' + pair['counter'] + "\n")
    file.write("# CON arguments:\n")
    for pair in extracted_arguments["con"]:
        file.write('point: ' + pair["point"] + "\n")
        file.write('counter: ' + pair["counter"] + "\n")
    file.close()