import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def call_endpoint(endpoint, method="GET", params=None, data=None):
    """
    Makes a request to the specified endpoint with optional parameters or data.

    Args:
        endpoint (str): The endpoint path (e.g., 'users', 'items/123')
        method (str): The HTTP method ('GET' or 'POST'). Defaults to 'GET'.
        params (dict): Query parameters for GET requests
        data (dict): Body data for POST requests

    Returns:
        dict: JSON response from the server

    Raises:
        ValueError: If method is neither 'GET' nor 'POST'
        Exception: If the request fails
    """
    url = f"{os.getenv('BACKEND_URL', 'http://localhost:8000')}/{endpoint}"

    # Validate method
    if method.upper() not in ["GET", "POST"]:
        raise ValueError("Method must be either 'GET' or 'POST'")

    # Make the appropriate request
    if method.upper() == "GET":
        response = requests.get(url, params=params)
    else:
        response = requests.post(url, params=params, files=data)

    # Handle response
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error calling endpoint: {response.status_code} - {response.text}")


def create_sidebar():
    st.sidebar.subheader("Model Selection")
    if "embedding_model_name" not in st.session_state:
        st.session_state.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    if "generation_model_name" not in st.session_state:
        st.session_state.generation_model_name = "Qwen/Qwen3-1.7B"
    st.session_state.embedding_model_name = st.sidebar.selectbox(
        "Embedding Model",
        ["sentence-transformers/all-MiniLM-L6-v2", "Environment Variable"],
    )
    st.session_state.generation_model_name = st.sidebar.selectbox(
        "Generation Model",
        ["Qwen/Qwen3-1.7B", "HuggingFaceTB/SmolLM3-3B", "Environment Variable"],
    )
