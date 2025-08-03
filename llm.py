from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from config import OLLAMA_MODEL
from database import optimized_retriever
import streamlit as st

def get_ollama_llm():
    return OllamaLLM(
        model=OLLAMA_MODEL,
        base_url="http://localhost:11434",
        temperature=1,
        streaming=True
    )

def process_user_input(vectordb, user_input, chat_history):
    # Use optimized_retriever for document retrieval
    retrieved_docs = optimized_retriever(vectordb, query=user_input, k=10)

    print(f"Retrieved {len(retrieved_docs)} documents for query: {retrieved_docs}")

    # Extract only the page_content field for context
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    
    llm = get_ollama_llm()
    template = """
        You are a helpful assistant that answers questions about our supply chain. 
        Use the provided context and metadata fields (e.g., order_id, order_date, delivery_date, Customer_Country, Customer_City) to answer the user's question.

        Here are some relevant details:
        {context}
        Your task is to answer the question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    qa_chain = prompt | llm
    
    # Stream response
    response_placeholder = st.empty()   
    result = ""
    for partial_result in qa_chain.stream({"context": context, "question": user_input, "chat_history": chat_history}):
        result += partial_result
        response_placeholder.markdown(f"<p style='color:green;'><b>Bot:</b> {result}</p>", unsafe_allow_html=True)
    
    return result
