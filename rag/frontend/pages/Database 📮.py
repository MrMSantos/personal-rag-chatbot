import pandas as pd
import streamlit as st
from utils import call_endpoint, create_sidebar

create_sidebar()

# Page title
st.set_page_config(page_title="Database", page_icon=":postbox:")

# Page title
st.title(":postbox: Database")

st.subheader("View database content", divider="blue")

# Create button to get all the embeddings
pages = st.button("View")

if pages:
    # List of all the embeddings
    response = call_endpoint("/")

    # response is a list. put it in a dataframe
    response = pd.DataFrame(response)

    st.write(response)

st.divider()

# Write "Get database content"
st.subheader("Upload a new file to the database", divider="blue")
# Option to upload a file
file = st.file_uploader("Upload a file", type=["txt", "csv"])

# Button to call the upload endpoint
upload = st.button("Upload")

if upload and file is None:
    st.warning("Please upload a file")

if upload and file is not None:
    # Upload the file
    filename = call_endpoint(
        "upload",
        method="POST",
        data={"file": file},
        params={"embedding_model_name": st.session_state.embedding_model_name},
    )

    st.write(filename)

    st.balloons()

st.divider()
