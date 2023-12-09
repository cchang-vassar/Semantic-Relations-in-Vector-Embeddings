from openai import OpenAI
import os
import API_KEY
os.environ["OPENAI_API_KEY"] = API_KEY.api_key()
client = OpenAI()
client.models.list()

import pandas as pd
import numpy as np
from ast import literal_eval


from ctypes import Union
from enum import Enum
from typing import Optional


# Convert arguments to embeddings
def _get_arguments_embeddings(arguments: {}) -> {}:
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
    # key: "pro_arguments_embeddings", "con_arguments_embeddings"
    # value: list of dictionaries where each is {'point_embedding':, 'counter_embedding':}
    return arguments_embeddings


# Convert the embeddings to lists
def embeddings_df(arguments_embedding: {}, debate_topic: Optional[argument.Category], debate_title: Optional[str]):
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


"""Batch processing"""
# Batch process debates in a category
def category_embeddings_data_batch(debate_file_topic: argument.Category, category_debates_arguments: [], analysis_type: AnalysisType) -> pd.DataFrame:
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
        



# Write extracted embeddings to csv file
def _embeddings_write_to_file(debate_topic: argument.Category, file_path: str, reshaped_arguments_embeddings: pd.DataFrame):
    reshaped_arguments_embeddings.to_csv('../' + 'data_dump/' + 'embeddings_dump/' +
                                         debate_topic.value + '/' + file_path + '_embeddings.csv',
                                         index=False)

