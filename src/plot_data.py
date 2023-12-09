import matplotlib.pyplot as plt
from plotnine import ggplot, geom_point, geom_text, aes, theme_void


# Plot it!
def arguments_embeddings_plot(arguments_plot_data: pd.DataFrame):
    colors = {'PRO': 'red', 'CON': 'blue'}
    plt.scatter(
        arguments_plot_data['x'],
        arguments_plot_data['y'],
        c=arguments_plot_data['stance'].map(colors),
        s=20)
    # connect pairs with lines
    for number_value in arguments_plot_data['number'].unique():
        subset = arguments_plot_data[arguments_plot_data['number'] == number_value]
        plt.plot(subset['x'], subset['y'], color='gray', linestyle='-', linewidth=0.5)

    plt.show()

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