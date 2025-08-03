import os
import pandas as pd
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from config import CSV_PATH, CHROMA_PATH, EMBEDDING_MODEL

def load_and_embed_csv(csv_path, chroma_path, embedding_model):
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
    
    # Add documents to the vector database
    vectordb.add_documents(documents=docs, ids=ids, verbose=True)
    
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
