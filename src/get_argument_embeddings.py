from ctypes import Union
from enum import Enum
from typing import Optional
from openai import OpenAI
import os
import API_KEY
os.environ["OPENAI_API_KEY"] = API_KEY.api_key()
client = OpenAI()
client.models.list()

import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import StandardScaler
import numpy as np
from ast import literal_eval
import matplotlib.pyplot as plt
import extract_arguments
from extract_arguments import DebateTopic
from plotnine import ggplot, geom_point, geom_text, aes, theme_void


    



def get_arguments_embeddings(arguments: {}) -> {}:
    pro_arguments = arguments['pro']
    con_arguments = arguments["con"]
    arguments_embeddings = {"pro_arguments_embeddings": [], "con_arguments_embeddings": []}
    # Loop through all pro arguments and create embeddings
    for argument in pro_arguments:
        cur_pair = {}
        point_argument_embedding = client.embeddings.create(input=argument['point'], model="text-embedding-ada-002")
        counter_argument_embedding = client.embeddings.create(input=argument['counter'], model="text-embedding-ada-002")
        cur_pair['point_embedding'] = point_argument_embedding.data[0].embedding
        cur_pair['counter_embedding'] = counter_argument_embedding.data[0].embedding
        arguments_embeddings["pro_arguments_embeddings"].append(cur_pair)
    # Loop through all con arguments and create embeddings
    for argument in con_arguments:
        cur_pair = {}
        point_argument_embedding = client.embeddings.create(input=argument['point'], model="text-embedding-ada-002")
        counter_argument_embedding = client.embeddings.create(input=argument['counter'], model="text-embedding-ada-002")
        cur_pair['point_embedding'] = point_argument_embedding.data[0].embedding
        cur_pair['counter_embedding'] = counter_argument_embedding.data[0].embedding
        arguments_embeddings["con_arguments_embeddings"].append(cur_pair)
    return arguments_embeddings


# Convert the embeddings to lists
def embeddings_df(arguments_embedding: {}, debate_topic: Optional[DebateTopic], debate_title: Optional[str]):
    reshaped_arguments_embeddings = pd.DataFrame()
    # loop through all argument pairs in the # PRO section
    for i, pro_embedding in enumerate(arguments_embedding["pro_arguments_embeddings"]):
        reshaped_point_embedding = pd.DataFrame(np.array(pro_embedding['point_embedding']).reshape(1, -1))
        reshaped_point_embedding['number'] = i
        reshaped_point_embedding['type'] = 'point'
        reshaped_arguments_embeddings = pd.concat([reshaped_arguments_embeddings, reshaped_point_embedding], axis=0)
        reshaped_arguments_embeddings = reshaped_arguments_embeddings.reset_index(drop=True)
        reshaped_arguments_embeddings.loc[reshaped_arguments_embeddings.index[-1], 'stance'] = 'PRO'
        
        reshaped_counter_embedding = pd.DataFrame(np.array(pro_embedding['counter_embedding']).reshape(1, -1))
        reshaped_counter_embedding['number'] = i
        reshaped_counter_embedding['type'] = 'counter'
        reshaped_arguments_embeddings = pd.concat([reshaped_arguments_embeddings, reshaped_counter_embedding], axis=0)
        reshaped_arguments_embeddings = reshaped_arguments_embeddings.reset_index(drop=True)
        reshaped_arguments_embeddings.loc[reshaped_arguments_embeddings.index[-1], 'stance'] = 'CON'
    
    offset = len(arguments_embedding["pro_arguments_embeddings"])
    # loop through all argument pairs in the # COUNTER section
    for j, con_embedding in enumerate(arguments_embedding["con_arguments_embeddings"]):
        reshaped_point_embedding = pd.DataFrame(np.array(con_embedding['point_embedding']).reshape(1, -1))
        reshaped_point_embedding['number'] = chr(j + offset)
        reshaped_point_embedding['type'] = 'point'
        reshaped_arguments_embeddings = pd.concat([reshaped_arguments_embeddings, reshaped_point_embedding], axis=0)
        reshaped_arguments_embeddings = reshaped_arguments_embeddings.reset_index(drop=True)
        reshaped_arguments_embeddings.loc[reshaped_arguments_embeddings.index[-1], 'stance'] = 'CON'
        
        reshaped_counter_embedding = pd.DataFrame(np.array(con_embedding['counter_embedding']).reshape(1, -1))
        reshaped_counter_embedding['number'] = chr(j + offset)
        reshaped_counter_embedding['type'] = 'counter'
        reshaped_arguments_embeddings = pd.concat([reshaped_arguments_embeddings, reshaped_counter_embedding], axis=0)
        reshaped_arguments_embeddings = reshaped_arguments_embeddings.reset_index(drop=True)
        reshaped_arguments_embeddings.loc[reshaped_arguments_embeddings.index[-1], 'stance'] = 'PRO'
    if debate_topic:
        reshaped_arguments_embeddings['debate_topic'] = debate_topic.value
    if debate_title:
        reshaped_arguments_embeddings['debate_title'] = debate_title
    return reshaped_arguments_embeddings.dropna()


# Write extracted embeddings to csv file
def embeddings_write_to_file(debate_topic: DebateTopic, file_path: str, reshaped_arguments_embeddings: pd.DataFrame):
    reshaped_arguments_embeddings.to_csv('../' + 'data_dump/' + 'embeddings_dump/' +
                                         debate_topic.value + '/' + file_path + '_embeddings.csv',
                                         index=False)



"""Batch processing"""
# Batch process debates in a category
def category_embeddings_data_batch(debate_file_topic: DebateTopic, category_debates_arguments: [], analysis_type: AnalysisType) -> pd.DataFrame:
    debates_data_set = pd.DataFrame()
    # loop through all debates in the category
    for arguments in category_debates_arguments:
        if arguments:
            arguments_embeddings = get_arguments_embeddings(arguments)
            arguments_df = embeddings_df(arguments_embeddings, debate_file_topic, debate_file_path)
            if analysis_type == AnalysisType.TSNE:
                arguments_data = arguments_embeddings_tsne(arguments_df)
            elif analysis_type == AnalysisType.PCA:
                arguments_data = arguments_embeddings_pca(arguments_df)
            arguments_data['file_path'] = debate_file_path
            if analysis_type == AnalysisType.TSNE:
                pca_write_to_file(debate_file_topic, debate_file_path, arguments_data)
            elif analysis_type == AnalysisType.PCA:
                tsne_write_to_file(debate_file_topic, debate_file_path, arguments_data)
            debates_data_set = pd.concat([debates_data_set, arguments_data], axis=0)
    return debates_data_set


# Batch process debates to get data across all categories at once
def global_embeddings_data_batch(categories_files: []) -> pd.DataFrame:
    all_categories = pd.DataFrame()
    for category in categories_files.keys():
        category_file_topic = category.value
        if arguments:
            arguments_embeddings = get_arguments_embeddings(arguments, )
            arguments_df = embeddings_df(arguments_embeddings)
            all_debates = pd.concat([all_debates, arguments_df], axis=0)
    arguments_tsne = arguments_embeddings_tsne(arguments_df)
    arguments_tsne['file_path'] = category_file_path
    tsne_write_to_file(category_file_topic, category_file_path, arguments_tsne)
    debates_tsne_set = pd.concat([debates_tsne_set, arguments_tsne], axis=0)
    
    
# Wrapper for data batch processing based on processing unit
def embeddings_data_batch(files: [], unit: ProcessingUnit) -> pd.DataFrame:
        if unit == ProcessingUnit.Debate:
            # TODO
            return
        elif unit == ProcessingUnit.Category:
            return category_embeddings_data_batch(files)
        elif unit == ProcessingUnit.Global:
            return global_embeddings_data_batch(files)
        
# Batch process debates to plot data
def debates_embeddings_plot_batch(debates_tsne_set: pd.DataFrame):
    colors = {'PRO': 'red', 'CON': 'blue'}
    unique_file_paths = pd.unique(debates_tsne_set['file_path'])
    num_cols = 5
    num_rows = len(unique_file_paths) // num_cols + (len(unique_file_paths) % num_cols > 0)
    fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(16, 2 * num_rows))
    
    for i, file_path in enumerate(unique_file_paths):
        row = i // num_cols
        col = i % num_cols
        subset = debates_tsne_set[debates_tsne_set['file_path'] == file_path]
        scatter = axs[row, col].scatter(subset['x'], subset['y'], c=subset['stance'].map(colors), s=20)
        axs[row, col].set_title(f'File Path: \n{file_path}', wrap=True)
        axs[row, col].set_xlabel('x')
        axs[row, col].set_ylabel('y')
        
        for number_value in subset['number'].unique():
                number_subset = subset[subset['number'] == number_value]
                axs[row, col].plot(number_subset['x'], number_subset['y'], color='gray', linestyle='-', linewidth=0.5)
    # Add a common legend for all subplots
    fig.legend(handles=scatter.legend_elements()[0], labels=colors.keys(), loc='upper right')
    # Adjust layout to prevent clipping of the legend
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()