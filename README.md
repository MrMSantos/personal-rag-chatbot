# Personal RAG Chatbot

Add documents to a vectorized database and ask it some questions in a streamlit app, using HuggingFace Models!

## Installation

### Requirements

- Python 3.11+
- Postgres
- pgvector
- Docker

### Configuration

Setup your Postgres parameters and HuggingFace API Key under .env file. Start by running:
```
cp .env.template .env
```
Fill `HUGGINGFACE_API_KEY` with your own key.
