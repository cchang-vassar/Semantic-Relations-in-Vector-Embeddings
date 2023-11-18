import re
from enum import Enum


# Enum for argument type
class ArgumentType(Enum):
    PRO = 1
    CON = 2


# Enum for debate topic
class DebateTopic(Enum):
    def __str__(self):
        return str(self.value)
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
    
    
# Extract arguments from .txt file
def extract_arguments(
    debate_topic: str,
    file_path: str,
    start_re: str = "# PRO",
    end_re: str = "# LITERATURE",
    pro_start_re: str = "# PRO\w+-POINT|# CON\w+-COUNTER",
    con_start_re: str = "# CON\w+-POINT|# PRO\w+-COUNTER"
    ):
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
        "pro": [],
        "con": []
    }
    current_argument: str = ""
    current_argument_type: ArgumentType = ArgumentType.PRO
    start: bool = False

    for line in lines:
        # skip to start line
        if (not start):
            if re.match(r'\s*' + start_re, line):
                start = True
                if (start_re == "# PRO"):
                    current_argument_type = ArgumentType.PRO
                elif (start_re == "# CON"):
                    current_argument_type = ArgumentType.CON
                continue
            continue

        # special case when we reach # LITERATURE we append the last argument and return
        if re.match(r'\s*' + end_re, line):
            arguments["pro"].append(current_argument.strip())
            arguments_write_to_file(debate_topic, file_path, arguments)
            return arguments

        # skip citations
        if re.match(r'\s*\[', line):
            continue

        # start a new entry into arguments["pro"] or arguments["con"] array if we see a # PRO... or # CON...
        if re.match(r'\s*' + pro_start_re, line):
            if (current_argument_type == ArgumentType.PRO):
                arguments["pro"].append(current_argument)
            elif (current_argument_type == ArgumentType.CON):
                arguments["con"].append(current_argument)
            current_argument_type = ArgumentType.PRO
            current_argument = ""
            continue
        elif re.match(r'\s*' + con_start_re, line):
            if (current_argument_type == ArgumentType.PRO):
                arguments["pro"].append(current_argument)
            elif (current_argument_type == ArgumentType.CON):
                arguments["con"].append(current_argument)
            current_argument_type = ArgumentType.CON
            current_argument = ""
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
    for line in extracted_arguments["pro"]:
        file.write(line + "\n")
    file.write("# CON arguments:\n")
    for line in extracted_arguments["con"]:
        file.write(line + "\n")
    file.close()
