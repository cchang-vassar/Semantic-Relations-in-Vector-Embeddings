from openai import OpenAI
import os
import API_KEY
os.environ["OPENAI_API_KEY"] = API_KEY.api_key()
client = OpenAI()
client.models.list()

import pandas as pd
from sklearn.manifold import TSNE
import numpy as np
from ast import literal_eval
import matplotlib.pyplot as plt
import extract_arguments
from extract_arguments import DebateTopic
from plotnine import ggplot, geom_point, geom_text, aes, theme_void


def get_arguments_embeddings(arguments: {}):
    pro_arguments = arguments['pro']
    con_arguments = arguments["con"]
    arguments_embeddings = {"pro_arguments_embeddings": [], "con_arguments_embeddings": []}
    # Loop through all pro arguments and create embeddings
    for argument in pro_arguments:
        argument_embedding = client.embeddings.create(input=argument, model="text-embedding-ada-002")
        arguments_embeddings["pro_arguments_embeddings"].append(argument_embedding.data[0].embedding)
    # Loop through all con arguments and create embeddings
    for argument in con_arguments:
        argument_embedding = client.embeddings.create(input=argument, model="text-embedding-ada-002")
        arguments_embeddings["con_arguments_embeddings"].append(argument_embedding.data[0].embedding)
    return arguments_embeddings


# Convert the embeddings to lists
def embeddings_df(arguments_embedding: {}):
    reshaped_arguments_embeddings = pd.DataFrame()
    for i, pro_embedding in enumerate(arguments_embedding["pro_arguments_embeddings"]):
        reshaped_embedding = pd.DataFrame(np.array(pro_embedding).reshape(1, -1))
        reshaped_arguments_embeddings = pd.concat([reshaped_arguments_embeddings, reshaped_embedding], axis=0)
        reshaped_arguments_embeddings = reshaped_arguments_embeddings.reset_index(drop=True)
        reshaped_arguments_embeddings.loc[reshaped_arguments_embeddings.index[-1], 'stance'] = 'PRO'
    for j, con_embedding in enumerate(arguments_embedding["con_arguments_embeddings"]):
        reshaped_embedding = pd.DataFrame(np.array(con_embedding).reshape(1, -1))
        reshaped_arguments_embeddings = pd.concat([reshaped_arguments_embeddings, reshaped_embedding], axis=0)
        reshaped_arguments_embeddings = reshaped_arguments_embeddings.reset_index(drop=True)
        reshaped_arguments_embeddings.loc[reshaped_arguments_embeddings.index[-1], 'stance'] = 'CON'
    return reshaped_arguments_embeddings.dropna()


# Write extracted embeddings to csv file
def embeddings_write_to_file(debate_topic: DebateTopic, file_path: str, reshaped_arguments_embeddings: pd.DataFrame):
    reshaped_arguments_embeddings.to_csv('../' + 'data_dump/' + 'embeddings_dump/' +
                                         debate_topic.value + '/' + file_path + '_embeddings.csv',
                                         index=False)


# TSNE it!
def arguments_embeddings_tsne(reshaped_arguments_embeddings: pd.DataFrame):
    reshaped_arguments_embeddings_data = reshaped_arguments_embeddings.iloc[:, :-1].values
    tsne = TSNE(n_components=2, perplexity=5, random_state=42, init='random', learning_rate=200)
    arguments_tsne = tsne.fit_transform(reshaped_arguments_embeddings_data)
    arguments_tsne_plot_data = pd.DataFrame(arguments_tsne, columns=['x','y']).join(reshaped_arguments_embeddings['stance'])
    return arguments_tsne_plot_data


# Write TSNE results to csv file
def tsne_write_to_file(
    debate_topic: DebateTopic,
    file_path: str,
    arguments_tsne_plot_data: pd.DataFrame
    ):
    arguments_tsne_plot_data.to_csv('../' + 'data_dump/' + 'tsne_dump/' + debate_topic.value + '/' +
                                    file_path + '_tsne.csv', index=False)


# Plot it!
def arguments_embeddings_tsne_plot(arguments_tsne_plot_data: pd.DataFrame):
    colors = {'PRO': 'red', 'CON': 'blue'}
    plt.scatter(
        arguments_tsne_plot_data['x'],
        arguments_tsne_plot_data['y'],
        c=arguments_tsne_plot_data['stance'].map(colors),
        s=20)
    plt.show()


# Batch process debates to get tsne data
def debates_embeddings_data_batch(debates_files: []):
    debates_tsne_set = pd.DataFrame()
    for debate_file in debates_files:
        debate_file_topic = debate_file["debate_topic"]
        debate_file_path = debate_file["file_path"]
        arguments = extract_arguments.extract_arguments(debate_file_topic.value, debate_file_path)
        if arguments:
            arguments_embeddings = get_arguments_embeddings(arguments)
            arguments_df = embeddings_df(arguments_embeddings)
            arguments_tsne = arguments_embeddings_tsne(arguments_df)
            arguments_tsne['file_path'] = debate_file_path
            tsne_write_to_file(debate_file_topic, debate_file_path, arguments_tsne)
            debates_tsne_set = pd.concat([debates_tsne_set, arguments_tsne], axis=0)
    return debates_tsne_set
        
        
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
        axs[row, col].scatter(subset['x'], subset['y'], c=subset['stance'].map(colors), s=20)
        axs[row, col].set_title(f'File Path: {file_path}')
        axs[row, col].set_xlabel('x')
        axs[row, col].set_ylabel('y')

    plt.tight_layout()
    plt.show()