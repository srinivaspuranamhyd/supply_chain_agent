import os
import pandas as pd
from langchain.schema import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from config import CSV_PATH, CHROMA_PATH, EMBEDDING_MODEL, OLLAMA_BASE_URL

def load_and_embed_csv(csv_path, chroma_path, embedding_model):
    """
    Loads a CSV file, converts each row to a Document with metadata,
    embeds the documents using Ollama, and stores them in a Chroma vector database.

    Args:
        csv_path (str): Path to the CSV file.
        chroma_path (str): Directory to persist Chroma DB.
        embedding_model (str): Name of the Ollama embedding model.

    Returns:
        Chroma: The initialized Chroma vector database.
    """
    import requests
    ollama_url = OLLAMA_BASE_URL  # Use from config

    # Check Ollama server availability before embedding
    try:
        response = requests.get(ollama_url + "/api/tags", timeout=5)
        if response.status_code != 200:
            raise RuntimeError(f"Ollama server is not responding at {ollama_url}")
    except Exception as e:
        import streamlit as st
        st.error(
            f"Ollama server is not running or unreachable at {ollama_url}. "
            f"Please start Ollama and ensure the model '{embedding_model}' is available. Error: {e}"
        )
        raise

    df = pd.read_csv(csv_path)
    docs = [
        Document(
            page_content=' '.join(row.astype(str)),
            metadata=row.to_dict()
        )
        for _, row in df.iterrows()
    ]
    ids = [str(i) for i in range(len(docs))]
    embeddings = OllamaEmbeddings(model=embedding_model, base_url=ollama_url)
    vectordb = Chroma(
        collection_name='supply_chain',
        embedding_function=embeddings,
        persist_directory=chroma_path
    )
    print(f"Embedding {len(docs)} documents... This may take a while.")
    try:
        vectordb.add_documents(documents=docs, ids=ids, verbose=True)
    except Exception as e:
        import streamlit as st
        st.error(
            f"Failed to embed documents. Please ensure Ollama is running and the model '{embedding_model}' is loaded. Error: {e}"
        )
        raise
    print(f"Loaded {len(docs)} documents into the vector database.")

    return vectordb

def initialize_vectordb():
    """
    Initializes or loads the Chroma vector database.

    Returns:
        Chroma: The initialized Chroma vector database.
    """
    ollama_url = OLLAMA_BASE_URL  # Use from config
    if not os.path.exists(CHROMA_PATH):
        return load_and_embed_csv(CSV_PATH, CHROMA_PATH, EMBEDDING_MODEL)
    else:
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=ollama_url)
        return Chroma(
            collection_name='supply_chain',
            embedding_function=embeddings,
            persist_directory=CHROMA_PATH
        )

def optimized_retriever(vectordb, query, metadata_filter=None, k=5, score_threshold=0.8):
    """
    Performs optimized retrieval from the vector database with optional metadata filtering and score threshold.

    Args:
        vectordb (Chroma): The Chroma vector database.
        query (str): The query string.
        metadata_filter (dict, optional): Metadata filter for retrieval.
        k (int, optional): Number of results to retrieve.
        score_threshold (float, optional): Minimum similarity score.

    Returns:
        list: Retrieved documents.
    """
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "score_threshold": score_threshold}
    )
    if metadata_filter:
        retriever = retriever.filter(metadata_filter)
    return retriever.invoke(query)
