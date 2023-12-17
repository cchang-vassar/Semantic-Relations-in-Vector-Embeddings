import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from plotnine import ggplot, geom_point, geom_text, aes, theme_void


ANALYSIS_ENUM = "run_analysis_batch.AnalysisType"


"""Debate level"""
# Plot embeddings for a single debate
def debate_plot(analysis_type: ANALYSIS_ENUM, arguments_plot_data: pd.DataFrame):
    from run_analysis_batch import AnalysisType
    stance_markers = {'PRO': '+', 'CON': '-'}
    plt.scatter(
        arguments_plot_data['x'],
        arguments_plot_data['y'],
        marker=arguments_plot_data['stance'].map(stance_markers),
        s=20)
    # connect pairs with lines
    for id in arguments_plot_data['id'].unique():
        subset = arguments_plot_data[arguments_plot_data['id'] == id]
        plt.plot(subset['x'], subset['y'], color='gray', linestyle='-', linewidth=0.5)
    plt.xlabel(f'{analysis_type.value}_x')
    plt.ylabel(f'{analysis_type.value}_y')
    plt.show()
    
    
"""Category level"""
# Plot embeddings for debates in a category
def category_plot(analysis_type: ANALYSIS_ENUM, category_plot_data: pd.DataFrame, facet: bool):
    from run_analysis_batch import AnalysisType
    stance_markers = {'PRO': '+', 'CON': '-'}
    unique_topics = category_plot_data['topic'].unique()
    
    if facet:
        num_cols = 5
        num_rows = len(unique_topics) // num_cols + (len(unique_topics) % num_cols > 0)
        fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(16, 2 * num_rows))
        
        for i, topic in enumerate(unique_topics):
            row = i // num_cols
            col = i % num_cols
            subset = category_plot_data[category_plot_data['topic'] == topic]
            scatter = axs[row, col].scatter(
                subset['x'],
                subset['y'],
                marker=subset['stance'].map(stance_markers),
                s=20)
            axs[row, col].set_title(f'Topic: \n{topic}', wrap=True)
            axs[row, col].set_xlabel(f'{analysis_type.value}_x')
            axs[row, col].set_ylabel(f'{analysis_type.value}_y')
            
            for id in subset['id'].unique():
                id_subset = subset[subset['id'] == id]
                axs[row, col].plot(
                    id_subset['x'],
                    id_subset['y'],
                    color='gray',
                    linestyle='-',
                    linewidth=0.5
                )
        # Add a common legend for all subplots
        fig.legend(handles=scatter.legend_elements()[0], labels=stance_markers.keys(), loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=len(stance_markers))
        # Adjust layout to prevent clipping of the legend
        plt.tight_layout(rect=[0, 0, 1, 0.96])
    else:
        category_plot_data['topic_color'] = category_plot_data['topic'].astype(str).agg('_'.join, axis=1)
        unique_topics = category_plot_data['topic_color'].unique()
        color_map = dict(zip(unique_topics, plt.cm.viridis(np.linspace(0, 1, len(unique_topics)))))
        scatter = plt.scatter(
            category_plot_data['x'],
            category_plot_data['y'],
            c=category_plot_data['topic'].map(color_map),
            marker=category_plot_data['stance'].map(stance_markers),
            s=20)
         # Add legend for topics
        plt.legend(handles=scatter.legend_elements()[0], labels=unique_topics, title='Topic', loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=len(unique_topics))
        # connect pairs with lines
        for id in category_plot_data['id'].unique():
            subset = category_plot_data[category_plot_data['id'] == id]
            plt.plot(subset['x'], subset['y'], color='gray', linestyle='-', linewidth=0.5)
    plt.show()
            
            
"""Global level"""
# Plot embeddings for debates in a category
def global_plot(analysis_type: ANALYSIS_ENUM, global_plot_data: pd.DataFrame, facet: bool):
    from run_analysis_batch import AnalysisType
    stance_markers = {'PRO': '+', 'CON': '-'}
    unique_topics = global_plot_data['topic'].unique()
    topic_color_map = dict(zip(unique_topics, plt.cm.viridis(np.linspace(0, 1, len(unique_topics)))))
    unique_categories = global_plot_data['category'].unique()
    category_color_map = dict(zip(unique_categories, plt.cm.viridis(np.linspace(0, 1, len(unique_categories)))))
    
    if facet:
        num_cols = 5
        num_rows = len(unique_categories) // num_cols + (len(unique_categories) % num_cols > 0)
        fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(16, 2 * num_rows))
        
        for i, category in enumerate(unique_categories):
            row = i // num_cols
            col = i % num_cols
            subset = global_plot_data[global_plot_data['category'] == category]
            scatter = axs[row, col].scatter(
                subset['x'],
                subset['y'],
                marker=subset['stance'].map(stance_markers),
                c=subset['topic'].map(topic_color_map),
                s=20)
            axs[row, col].set_title(f'Category: \n{category}', wrap=True)
            axs[row, col].set_xlabel(f'{analysis_type.value}_x')
            axs[row, col].set_ylabel(f'{analysis_type.value}_y')
            
            for id in subset['id'].unique():
                id_subset = subset[subset['id'] == id]
                axs[row, col].plot(
                    id_subset[f'{analysis_type.value}_x'],
                    id_subset[f'{analysis_type.value}_y'],
                    color='gray',
                    linestyle='-',
                    linewidth=0.5
                )
        # Add a common legend for all subplots
        fig.legend(handles=scatter.legend_elements()[0], labels=stance_markers.keys(), loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=len(stance_markers))
        # Adjust layout to prevent clipping of the legend
        plt.tight_layout(rect=[0, 0, 1, 0.96])
    else:
        scatter = plt.scatter(
            global_plot_data['x'],
            global_plot_data['y'],
            c=global_plot_data['topic'].map(topic_color_map),
            marker=global_plot_data['stance'].map(stance_markers),
            s=20)
         # Add legend for topics
        plt.legend(handles=scatter.legend_elements()[0], labels=stance_markers.keys(), loc='upper center')
        # connect pairs with lines
        for id in global_plot_data['id'].unique():
            subset = global_plot_data[global_plot_data['id'] == id]
            plt.plot(subset['x'], subset['y'], color='gray', linestyle='-', linewidth=0.5)
        # Add halo for category
        for category, color in category_color_map.items():
            category_subset = global_plot_data[global_plot_data['category'] == category]
            # Scatter plot with halo effect
            plt.scatter(
                category_subset['x'],
                category_subset['y'],
                c='none',  # Set the face color to 'none' for a halo effect
                edgecolors=color,  # Use the category color for the edge
                s=100,  # Adjust the size of the halo as needed
                marker='o',
                linewidths=1,
                alpha=0.3  # Adjust alpha as needed
            )
    plt.show()