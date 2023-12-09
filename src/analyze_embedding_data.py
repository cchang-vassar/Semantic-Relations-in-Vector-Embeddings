from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import StandardScaler

from enum import Enum


class AnalysisType(Enum):
    TSNE = "tsne"
    PCA = "pca"


# TSNE it!
def arguments_embeddings_tsne(reshaped_arguments_embeddings: pd.DataFrame):
    numeric_columns = reshaped_arguments_embeddings.select_dtypes(include=[np.number]).columns
    reshaped_arguments_embeddings_data = reshaped_arguments_embeddings[numeric_columns].values
    tsne = TSNE(n_components=2, perplexity=len(reshaped_arguments_embeddings_data) // 2, random_state=42, init='random', learning_rate=200)
    arguments_tsne = tsne.fit_transform(reshaped_arguments_embeddings_data)
    arguments_tsne_plot_data = (
        pd.DataFrame(arguments_tsne, columns=['x','y'])
        .join(reshaped_arguments_embeddings[['number', 'type', 'stance']])
    )
    return arguments_tsne_plot_data


# PCA it!
def arguments_embeddings_pca(reshaped_arguments_embeddings: pd.DataFrame):
    numeric_columns = reshaped_arguments_embeddings.select_dtypes(include=[np.number]).columns
    reshaped_arguments_embeddings_data = reshaped_arguments_embeddings[numeric_columns].values
    scaler = StandardScaler()
    embedding_vectors_scaled = scaler.fit_transform(reshaped_arguments_embeddings_data)
    num_components = 2
    pca = PCA(n_components=num_components)
    arguments_pca = pca.fit_transform(embedding_vectors_scaled)
    arguments_pca_plot_data = (
        pd.DataFrame(arguments_pca, columns=['x','y'])
        .join(reshaped_arguments_embeddings[['number', 'type', 'stance']])
    )
    return arguments_pca_plot_data


# Write TSNE results to csv file
def tsne_write_to_file(
    debate_topic: DebateTopic,
    file_path: str,
    arguments_tsne_plot_data: pd.DataFrame
    ):
    arguments_tsne_plot_data.to_csv('../' + 'data_dump/' + 'tsne_dump/' + debate_topic.value + '/' +
                                    file_path + '_tsne.csv', index=False)


# Write PCA results to csv file'
def pca_write_to_file(
    debate_topic: DebateTopic,
    file_path: str,
    arguments_pca_plot_data: pd.DataFrame
    ):
    arguments_pca_plot_data.to_csv('../' + 'data_dump/' + 'pca_dump/' + debate_topic.value + '/' +
                                    file_path + '_pca.csv', index=False)
