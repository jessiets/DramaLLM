import streamlit as st
from tmdb_utils import *
from openai_utils import *
import random
import time


st.title('Netflix K-Drama & C-Drama Recommender')
st.write('Let the bot know the genre(s) you are interested in and get top drama recommendations available on Netflix!')


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's find a drama you like on Netflix 👇"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your drama request here!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     message_placeholder = st.empty()
    #     full_response = ""
    #     assistant_response = random.choice(
    #         [
    #             "Hello there! How can I assist you today?",
    #             "Hi, human! Is there anything I can help you with?",
    #             "Do you need help?",
    #         ]
    #     )
    #     # Simulate stream of response with milliseconds delay
    #     for chunk in assistant_response.split():
    #         full_response += chunk + " "
    #         time.sleep(0.05)
    #         # Add a blinking cursor to simulate typing
    #         message_placeholder.markdown(full_response + "▌")
    #     message_placeholder.markdown(full_response)
    # # Add assistant response to chat history
    # st.session_state.messages.append({"role": "assistant", "content": full_response})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            intent = interpret_user_message(prompt)
            genre_map = {
                "Romance": 10749,
                "Drama": 18,
                "Comedy": 35,
                "Mystery": 9648,
                "Action & Adventure": 10759,
            }
            genre_id = genre_map.get(intent["genre"], 18)
            region = "KR" if intent["region"] == "KR" else "CN"
            dramas = get_top_netflix_dramas(genre_id, region='US')
            reply = summarize_dramas(dramas)
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})