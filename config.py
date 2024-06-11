from langchain_community.embeddings import OllamaEmbeddings

CHROMA_PATH = "database/"
DATA_PATH = "sources/"

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
EMBED_NAME = "llama3"


def embedding_function():
    embeddings = OllamaEmbeddings(
        base_url="http://host.docker.internal:11434",
        model="nomic-embed-text",
        temperature=0,
    )
    return embeddings


PROMPT = """
Jesteś pomocnym asystentem - nie dodawaj nic od siebie, nie dodawaj żadnych opinii. 
Odpowiadaj na pytania TYLKO na podstawie podanego kontekstu - nie używaj swojej własnej wiedzy - jeżeli w kontekście nie ma odpowiedzi na pytanie, poiwedz o tym. 
Odpowiadaj krótko i precyzyjnie w języku Polskim - nie oceniaj, nie modyfikuj - odpowiadaj tylko na podstawie kontekstu.
"""
