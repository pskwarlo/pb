import argparse
import os
import shutil

from langchain.schema.document import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHROMA_PATH, CHUNK_OVERLAP, CHUNK_SIZE, DATA_PATH
from embedding_function import embedding_function


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset bazy danych.")
    args = parser.parse_args()
    if args.reset:
        print("Czyszenie bazy danych...")
        clear_database()

    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def load_documents():
    documents = DirectoryLoader(DATA_PATH, glob="./*.txt", loader_cls=TextLoader)
    print(documents)
    return documents.load()


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=False,
        strip_whitespace=False,
        separators=[
            "\n\n",
            "|",
        ],
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function())

    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Liczba dokumentów w bazie danych: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        print(chunk)
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Dodawanie dokumentów: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("Baza danych jest aktualna")


def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("zrodlo")
        page = chunk.metadata.get("strona")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()
