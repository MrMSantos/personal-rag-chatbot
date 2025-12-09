# Create a stramlit app that asks questions and returns answers

import os

import streamlit as st
from dotenv import load_dotenv
from utils import call_endpoint, create_sidebar

# Load environment variables from .env
load_dotenv()

# Create sidebar where I can select the model name I want
create_sidebar()

# Page title
st.set_page_config(page_title="Tennis Chatbot", page_icon=":tennis:")

st.title(":tennis: Tennis Chatbot")

# Get user question
user_question = st.chat_input("Ask me anything about tennis")

args = {
    "question": user_question,
}

if st.session_state.embedding_model_name == "Environment Variable":
    st.session_state.embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")

if st.session_state.generation_model_name == "Environment Variable":
    st.session_state.generation_model_name = os.getenv("GENERATION_MODEL_NAME")

args["embedding_model_name"] = st.session_state.embedding_model_name
args["generation_model_name"] = st.session_state.generation_model_name
print(args)

# Add a spinning wheel while waiting for the response
with st.spinner("Generating response..."):
    if user_question:
        st.chat_message("user").write(user_question)
        response = call_endpoint("ask", params=args)
        st.chat_message("assistant").write(response["response"])
