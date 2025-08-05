__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from database import initialize_vectordb
from llm import process_user_input
from ui import setup_page, display_chat_history

# --- MAIN APP ---
def main():
    setup_page()
    vectordb = initialize_vectordb()

    # Create columns for better layout
    col1, col2, col3 = st.columns([3, 2, 3])  # Narrow column for input, wider column for chat history

    with col1:
        user_input = st.text_input("Type your question:", key="input")  # Input box in the first column
        if st.button("Send") and user_input:
            with st.spinner("Thinking..."):
                result = process_user_input(vectordb, user_input, st.session_state.get("chat_history", []))
                if "chat_history" not in st.session_state:
                    st.session_state["chat_history"] = []
                st.session_state["chat_history"].append((user_input, result))

    with col2:
        st.empty()  # Spacer to add vertical space
        st.empty()  # Spacer to add vertical space

    with col3:
        display_chat_history(st.session_state.get("chat_history", []))

if __name__ == "__main__":
    main()