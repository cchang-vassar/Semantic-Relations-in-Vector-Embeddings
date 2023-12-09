from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import StandardScaler
import pandas as pd
import numpy as np

import os
from enum import Enum
from typing import Optional

from extract_arguments import Category


class AnalysisType(Enum):
    TSNE = "tsne"
    PCA = "pca"


"""Debate level"""
# TSNE argument embeddings from a debate
def debate_tsne_embeddings(arguments_embeddings_df: pd.DataFrame):
    numeric_columns = arguments_embeddings_df.select_dtypes(include=[np.number]).columns
    non_numeric_columns = arguments_embeddings_df.select_dtypes(exclude=[np.number]).columns
    arguments_embeddings_data = arguments_embeddings_df[numeric_columns].values
    tsne = TSNE(n_components=2, perplexity=len(arguments_embeddings_data) // 2, random_state=42, init='random', learning_rate=200)
    arguments_tsne = tsne.fit_transform(arguments_embeddings_data)
    arguments_tsne_plot_data = (
        pd.DataFrame(arguments_tsne, columns=['x','y'])
        .join(arguments_embeddings_df[non_numeric_columns])
    )
    return arguments_tsne_plot_data

# PCA argument embeddings from a debate
def debate_pca_embeddings(arguments_embeddings_df: pd.DataFrame):
    numeric_columns = arguments_embeddings_df.select_dtypes(include=[np.number]).columns
    non_numeric_columns = arguments_embeddings_df.select_dtypes(exclude=[np.number]).columns
    arguments_embeddings_data = arguments_embeddings_df[numeric_columns].values
    scaler = StandardScaler()
    embedding_vectors_scaled = scaler.fit_transform(arguments_embeddings_data)
    num_components = 2
    pca = PCA(n_components=num_components)
    arguments_pca = pca.fit_transform(embedding_vectors_scaled)
    arguments_pca_plot_data = (
        pd.DataFrame(arguments_pca, columns=['x','y'])
        .join(arguments_embeddings_df[non_numeric_columns])
    )
    return arguments_pca_plot_data

# Write analysis results to csv file'
def _analysis_write_to_file(
    analysis_type: AnalysisType,
    category: Optional[Category],
    topic: Optional[str],
    arguments_plot_data: pd.DataFrame
    ):
    if topic and category:
        topic_path = topic.replace('-', '_')
        output_folder = f'../data_dump/{analysis_type.value}_dump/{category.value}/'
        output_file_path = f'{output_folder}{topic_path}_{analysis_type.value}.csv'
    elif category:
        output_folder = f'../data_dump/{analysis_type.value}_dump/'
        output_file_path = f'{output_folder}{category.value}_{analysis_type.value}.csv'
    else:
        output_folder = f'../data_dump/{analysis_type.value}_dump/'
        output_file_path = f'{output_folder}global_{analysis_type.value}.csv'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    arguments_plot_data.to_csv(output_file_path, index=False)
    
    
"""Category level"""
def category_analyze_embeddings(category: Category, analysis_type: AnalysisType, category_embeddings_df: pd.DataFrame):
    if analysis_type == AnalysisType.TSNE:
        category_embeddings_analysis = debate_tsne_embeddings(category_embeddings_df)
    elif analysis_type == AnalysisType.PCA:
        category_embeddings_analysis = debate_pca_embeddings(category_embeddings_df)
    _analysis_write_to_file(analysis_type, category, category_embeddings_analysis)
    return category_embeddings_analysis