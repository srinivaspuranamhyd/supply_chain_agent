import os
import pandas as pd
from langchain.schema import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from config import CSV_PATH, CHROMA_PATH, EMBEDDING_MODEL

def load_and_embed_csv(csv_path, chroma_path, embedding_model):
    import requests
    # Check Ollama server availability before embedding
    ollama_url = "https://ollama-llama3-2-71690586093.asia-southeast1.run.app/api/tags"
    try:
        response = requests.get(ollama_url, timeout=5)
        if response.status_code != 200:
            raise RuntimeError(f"Ollama server is not responding at {ollama_url}")
    except Exception as e:
        import streamlit as st
        st.error(f"Ollama server is not running or unreachable at {ollama_url}. Please start Ollama and ensure the model '{embedding_model}' is available. Error: {e}")
        raise

    df = pd.read_csv(csv_path)
    docs = [
        Document(
            page_content=' '.join(row.astype(str)),
            metadata=row.to_dict()  # Ensure all fields, including order_id, are included in metadata
        )
        for _, row in df.iterrows()
    ]
    ids = [str(i) for i in range(len(docs))]
    embeddings = OllamaEmbeddings(model=embedding_model)
    vectordb = Chroma(
        collection_name='supply_chain',
        embedding_function=embeddings,
        persist_directory=chroma_path
    )
    print(f"Embedding {len(docs)} documents... This may take a while.")
    try:
        # Add documents to the vector database
        vectordb.add_documents(documents=docs, ids=ids, verbose=True)
    except Exception as e:
        import streamlit as st
        st.error(f"Failed to embed documents. Please ensure Ollama is running and the model '{embedding_model}' is loaded. Error: {e}")
        raise
    print(f"Loaded {len(docs)} documents into the vector database.")

    return vectordb

def initialize_vectordb():
    if not os.path.exists(CHROMA_PATH):
        return load_and_embed_csv(CSV_PATH, CHROMA_PATH, EMBEDDING_MODEL)
    else:
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        return Chroma(
            collection_name='supply_chain',
            embedding_function=embeddings,
            persist_directory=CHROMA_PATH
        )

def optimized_retriever(vectordb, query, metadata_filter=None, k=5, score_threshold=0.8):
    """Perform optimized retrieval with metadata filtering and score threshold."""
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "score_threshold": score_threshold}  # Include score_threshold
    )
    if metadata_filter:
        retriever = retriever.filter(metadata_filter)
    return retriever.invoke(query)
