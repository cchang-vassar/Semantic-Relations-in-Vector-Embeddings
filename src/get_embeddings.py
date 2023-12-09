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

from extract_arguments import Category


"""Debate level"""
# Convert arguments to embeddings
def _debate_get_embeddings(arguments: {}) -> {}:
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
def _debate_get_embeddings_df(topic: str, arguments_embeddings: {}) -> pd.DataFrame:
    arguments_embeddings_df = pd.DataFrame()
    # loop through all argument pairs in the # PRO section
    for i, pro_embedding in enumerate(arguments_embeddings["pro_arguments_embeddings"]):
        point_embedding = pd.DataFrame(np.array(pro_embedding['point_embedding']).reshape(1, -1))
        point_embedding['id'] = chr(i)
        point_embedding['type'] = 'point'
        point_embedding['stance'] = 'PRO'
        arguments_embeddings_df = pd.concat([arguments_embeddings_df, point_embedding], axis=0)
        arguments_embeddings_df = arguments_embeddings_df.reset_index(drop=True)
        
        counter_embedding = pd.DataFrame(np.array(pro_embedding['counter_embedding']).reshape(1, -1))
        counter_embedding['id'] = chr(i)
        counter_embedding['type'] = 'counter'
        counter_embedding['stance'] = 'CON'
        arguments_embeddings_df = pd.concat([arguments_embeddings_df, counter_embedding], axis=0)
        arguments_embeddings_df = arguments_embeddings_df.reset_index(drop=True)
    
    offset = len(arguments_embeddings["pro_arguments_embeddings"])
    # loop through all argument pairs in the # COUNTER section
    for j, con_embedding in enumerate(arguments_embeddings["con_arguments_embeddings"]):
        point_embedding = pd.DataFrame(np.array(con_embedding['point_embedding']).reshape(1, -1))
        point_embedding['id'] = chr(j + offset)
        point_embedding['type'] = 'point'
        point_embedding['stance'] = 'CON'
        arguments_embeddings_df = pd.concat([arguments_embeddings_df, point_embedding], axis=0)
        arguments_embeddings_df = arguments_embeddings_df.reset_index(drop=True)
        
        counter_embedding = pd.DataFrame(np.array(con_embedding['counter_embedding']).reshape(1, -1))
        counter_embedding['id'] = chr(j + offset)
        counter_embedding['type'] = 'counter'
        counter_embedding['stance'] = 'PRO'
        arguments_embeddings_df = pd.concat([arguments_embeddings_df, counter_embedding], axis=0)
        arguments_embeddings_df = arguments_embeddings_df.reset_index(drop=True)
    arguments_embeddings_df['topic'] = topic
    return arguments_embeddings_df.dropna()


# Write extracted embeddings to csv file
def _embeddings_write_to_file(debate_topic: argument.Category, file_path: str, reshaped_arguments_embeddings: pd.DataFrame):
    reshaped_arguments_embeddings.to_csv('../' + 'data_dump/' + 'embeddings_dump/' +
                                         debate_topic.value + '/' + file_path + '_embeddings.csv',
                                         index=False)



"""Category level"""
# Batch process debates in a category
def category_get_embeddings_df(category: Category, category_arguments: {}) -> pd.DataFrame:
    category_embeddings_df = pd.DataFrame()
    for topic, arguments in category_arguments[category.value]:
        arguments_embeddings = _debate_get_embeddings(arguments)
        arguments_df = _debate_get_embeddings_df(topic, arguments_embeddings)
        category_embeddings_df = pd.concat([category_embeddings_df, arguments_df], axis=0)
    category_embeddings_df['category'] = category.value
    return category_embeddings_df


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
        


