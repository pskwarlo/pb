from langchain_community.embeddings import OllamaEmbeddings


def embedding_function():
    embeddings = OllamaEmbeddings(
        base_url="http://host.docker.internal:11434",
        model="nomic-embed-text",
        temperature=0,
    )
    return embeddings
