# Personal RAG Chatbot

Add documents to a vectorized database and ask it some questions in a streamlit app, using HuggingFace Models!

## Installation

### Requirements

- Python 3.11+
- Postgres
- pgvector

### Configuration

Setup your Postgres parameters and HuggingFace API Key under .env file. Start by running:
```
cp .env.template .env
```
Fill `HUGGINGFACE_API_KEY` with your own key and all database related parameters.

### Setup

To run the application build run docker compose by running:
```
docker compose build
docker compose up
```

## Usage
### Ask Chatbot
<img width="1886" height="853" alt="image" src="https://github.com/user-attachments/assets/94ba11a9-2b74-499f-a2ef-bb4c1aca7bf5" />

### Load and List Database
<img width="1882" height="797" alt="image" src="https://github.com/user-attachments/assets/1ad897be-6f47-4f05-a8b6-fe24814296d8" />
