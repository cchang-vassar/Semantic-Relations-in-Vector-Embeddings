import re
from enum import Enum
from typing import Optional

import extract_arguments as argument
import get_argument_embeddings as embedding
import analyze_embedding_data as analyze
import plot_data as plot
from analyze_embedding_data import AnalysisType


# Level of processing
class ProcessingUnit(Enum):
    GLOBAL: 1
    CATEGORY: 2
    DEBATE: 3


# Run analysis on a single category
def category_run_analysis_batch(debate_topic: argument.DebateTopic, file_path: str, analysis_type: AnalysisType):
    category_files = []
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
        category_files.append({"debate_topic": debate_topic, "file_path": line})
    # category_files: list of dictionaries where each is {"debate_topic": DebateTopic, "file_path": str}
    category_arguments = []
    for debate_file in category_files:
        debate_file_topic = debate_file["debate_topic"]
        debate_file_path = debate_file["file_path"]
        # arguments: {"pro": [{"point": str, "counter": str}, ...], "con": [{"point": str, "counter": str}, ...]}
        arguments = argument.category_extract_arguments(debate_file_topic.value, debate_file_path)
        category_arguments.append(arguments)
    # grab embeddings for each debate in the category
    category_embeddings = embedding.category_embeddings_data_batch(debate_file_topic, category_arguments)
    # run analysis on category embeddings
    category_analysis = analyze.category_embeddings_analysis_batch(category_embeddings)
    # plot batch analysis
    plot.debates_embeddings_plot_batch(category_analysis)
    
    
# Run analysis on all categories at once
def global_run_analysis_batch(analysis_type: AnalysisType):
    # grab global arguments
    # key: category DebateTopic;
    # value: list of dictionaries where each is {'pro: [{'point':, 'counter':}, ...], 'con': []}
    global_arguments = argument.global_extract_arguments()
    # grab global embeddings
    global_embeddings = embedding.global_embeddings_data_batch()
    # run analysis on global embeddings
    global_embeddings_analysis = global_embeddings_analysis_batch(global_embeddings)
    # plot category batch analysis
    global_embeddings_plot_batch(categories_embeddings)
    
def run_analysis_batch(
    debate_topic: Optional[argument.DebateTopic],
    file_path: Optional[str],
    processing_unit: ProcessingUnit = ProcessingUnit.GLOBAL,
    analysis_type: AnalysisType = AnalysisType.PCA,
    ):
    if processing_unit == ProcessingUnit.GLOBAL:
        argument.global_extract_arguments()
    elif processing_unit == ProcessingUnit.CATEGORY:
        category_run_analysis_batch(analysis_type)
    elif processing_unit == ProcessingUnit.DEBATE:
        debate_run_analysis_batch(analysis_type)
    
    


    
    
    
      
    