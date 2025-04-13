import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from chromaDB_store import ChromaDB
from openai_utils import *


# Setup database
if 'db' not in st.session_state:
    st.session_state.db = ChromaDB()


st.title('Netflix K-Drama & C-Drama Recommender')
st.write('Let the bot know the genre(s) you are interested in and get top drama recommendations available on Netflix!')


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's find a drama you like on Netflix 👇"}]


# Accept user input
if prompt := st.chat_input("Type your drama request here!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        print(f'\nat spinner\n')
        with st.spinner("Thinking..."):
            intent = interpret_user_message(prompt, st.session_state.db)
           
            # reply = summarize_dramas(dramas)
            # st.markdown(reply)
            st.markdown(intent)
            st.session_state.messages.append({"role": "assistant", "content": intent})
