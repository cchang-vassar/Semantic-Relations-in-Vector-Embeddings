import re
from enum import Enum
from typing import Optional

import extract_arguments as argument
import get_embeddings as embedding
import analyze_embedding_data as analyze
import plot_data as plot
from analyze_embedding_data import AnalysisType

# Enum for debate categories
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


# Level of processing
class ProcessingUnit(Enum):
    GLOBAL: 1
    CATEGORY: 2
    DEBATE: 3


# Run analysis on a single category
def category_run_analysis_batch(category: Category, analysis_type: AnalysisType):
    # grab arguments for all debates in the category -> {}
    category_arguments = argument.category_extract_arguments(category)
    # grab embeddings for all debates in the category -> pd.DataFrame
    category_embeddings_df = embedding.category_get_embeddings_df(category, category_arguments)
    # run analysis on category embeddings
    category_analysis = analyze.category_analyze_embeddings(category, analysis_type, category_embeddings_df)
    # plot batch analysis
    plot.debates_embeddings_plot_batch(category_analysis)
    return category_arguments
    
    
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
    



    
    
    
      
    