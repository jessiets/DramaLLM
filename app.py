import streamlit as st
from chromaDB_store import ChromaDB
from openai_utils import *
from tmdb_queries import get_poster_image, get_drama_title
import random


# Setup database
with st.spinner("Populating database... (this will take about 9-10 minutes)"):
    if 'db' not in st.session_state:
        st.session_state.db = ChromaDB('collection')


st.title('Netflix K-Drama & C-Drama Recommender')
st.write('Let the bot know the genre(s) you are interested in and get top drama recommendations available on Netflix!')


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's find a drama you like on Netflix 👇"}]


# Accept user input
if prompt := st.text_input("Type your drama request here!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        # process results
        reply = analyze_results(prompt, st.session_state.db)
        print(f'\n----------------------------\nreply: {reply}\n-------------------------------\n')


        # output results
        no_result = 0
        st.write(f"Your request is: {reply[0]['user_input']}\n")
        st.write(f"Based on your request, I've searched for dramas that match the keywords: {reply[0]['keywords']}\n\n")
        st.write(f"Here are some dramas that I think you will be interested in!")
        for i in range(0, len(reply)):
            if reply[i]['is_match'].lower() == 'no':
                no_result += 1
                continue

            col1,col2 = st.columns(2, border=True)
            # get poster images
            poster_path = get_poster_image(reply[i]['show_id'])
            
            if len(poster_path) > 1:
                col1.image(poster_path[0])
                col1.image(poster_path[random.randint(1, len(poster_path)-1)])
            elif len(poster_path) > 0:
                col1.image(poster_path[0])
            else:
                col1.write("No posters for this drama.")
            col2.markdown(f"Title: {get_drama_title(reply[i]['show_id'])}\n")
            col2.markdown(reply[i]['synopsis'])

        if no_result >= len(reply):
            st.write("Sorry! I don't know any drama that you will like at the moment.")
        
