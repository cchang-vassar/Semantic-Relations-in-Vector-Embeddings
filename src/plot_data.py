
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
