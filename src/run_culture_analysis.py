import re
import extract_arguments
from get_argument_embeddings import debates_embeddings_data_batch, debates_embeddings_plot_batch
from extract_arguments import DebateTopic

def run_analysis_batch(debate_topic: DebateTopic, file_path: str):
    debates_files = [{"debate_topic": DebateTopic, "file_path": str}]
    # try to open file from path
    try:
        with open('./' + file_path + '.txt', 'r') as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path + '.txt'}")
        return None
    # convert file contents to dictionary with debate_topic and file_path for each line
    lines: [] = re.split(r'\n', file_contents)
    for line in lines:
        debates_files.append({"debate_topic": debate_topic, "file_path": line})
    # run batch analysis
    debates_embeddings = debates_embeddings_data_batch(debates_files)
    return debates_embeddings
    # debates_embeddings_plot_batch(debates_embeddings)
    
results = run_analysis_batch(DebateTopic.CULTURE, "list_of_culture_debates")