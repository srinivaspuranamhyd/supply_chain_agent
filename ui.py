import streamlit as st

def setup_page():
    st.set_page_config(page_title="Supply Chain Sage", layout="wide", initial_sidebar_state="expanded")
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url("https://images.unsplash.com/photo-1542831371-3f2b8f7f4f3c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80") no-repeat center center fixed;
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Use st.image() to display the local image file
    st.image("assets/images/supply_chain_bot_logo.png", width=380)
    st.title("Supply Chain Sage")
    st.write("Your intelligent assistant for all supply chain insights!")

def display_chat_history(chat_history):
    # Create columns for subheader and image
    col1, col2 = st.columns([1, 3])  # Adjust column widths as needed
    with col1:
        st.image("assets/images/history_icon.png", width=50)  # Replace with your desired image path
    with col2:
        st.subheader("History")

    # Display chat history
    if not chat_history:
        st.write("No conversation history yet.")
        return
    
    # Create columns for spacing
    _, col, _ = st.columns([4, 0, 0])  # Add spacing columns on the left and right
    with col:
        for q, a in reversed(chat_history):  # Reverse the order
            st.markdown("<h4 style='color:blue;'>User Input:</h4>", unsafe_allow_html=True)  # Header for user input
            st.markdown(f"<p style='color:blue;'>{q}</p>", unsafe_allow_html=True)  # User input in blue
            st.markdown("<h4 style='color:green;'>Bot Response:</h4>", unsafe_allow_html=True)  # Header for bot response
            st.markdown(f"<p style='color:green;'>{a}</p>", unsafe_allow_html=True)
