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
        
        /* Hide the deploy button */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Alternative method to hide deploy button */
        .stDeployButton {
            display: none !important;
        }
        
        /* Hide the hamburger menu that contains deploy option */
        .stApp > header {
            background-color: transparent;
        }
        .stApp > header > div {
            display: none;
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
    col1, col2 = st.columns([1, 5])  # Adjust column widths as needed
    with col1:
        st.image("assets/images/history_icon.png", width=50)  # Replace with your desired image path
    with col2:
        st.subheader("User Conversations")

    # Display chat history
    if not chat_history:
        st.write("No conversation history yet.")
        return
    
    for q, a in reversed(chat_history):  # Reverse the order
        st.markdown(f"<h4 style='color:blue;'>User Input:</h4> <p style='color:blue;'>{q}</p><h4 style='color:green;'>Bot Response:</h4><p style='color:green;'>{a}</p><hr style='border: 2px solid #ccc; margin: 20px 0;'/>", unsafe_allow_html=True)  # Header for user input
    