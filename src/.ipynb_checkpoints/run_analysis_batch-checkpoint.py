import re
from enum import Enum
from typing import Optional

import extract_arguments as argument
import get_embeddings as embedding
import analyze_embedding_data as analyze
import plot_data as plot

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
    
# Enum for analysis types
class AnalysisType(Enum):
    TSNE = "tsne"
    PCA = "pca"


# Run analysis on a single category
def category_run_analysis_batch(category: Category, analysis_type: AnalysisType):
    # grab arguments for all debates in the category -> {}
    category_arguments = argument.category_extract_arguments(category)
    # grab embeddings for all debates in the category -> pd.DataFrame
    category_embeddings_df = embedding.category_get_embeddings_df(category, category_arguments)
    # run analysis on category embeddings
    category_analysis = analyze.category_analyze_embeddings(category, analysis_type, category_embeddings_df)
    # plot category analysis
    plot.category_plot(analysis_type, category_analysis, False)
    
    
# Run analysis on all categories at once
def global_run_analysis_batch(analysis_type: AnalysisType):
    # grab global arguments
    # key: category DebateTopic;
    # value: list of dictionaries where each is {'pro: [{'point':, 'counter':}, ...], 'con': []}
    global_arguments = argument.global_extract_arguments()
    # grab global embeddings
    global_embeddings = embedding.global_get_embeddings_df(global_arguments)
    # run analysis on global embeddings
    global_embeddings_analysis = analyze.global_analyze_embeddings(analysis_type, global_embeddings)
    # plot global analysis
    plot.global_plot(analysis_type, global_embeddings_analysis, False)

    
category_run_analysis_batch(Category.CULTURE, AnalysisType.PCA)
    
      
    