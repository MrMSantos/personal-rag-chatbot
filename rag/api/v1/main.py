import logging

import chardet
from fastapi import Depends, FastAPI, HTTPException, UploadFile

from rag.api.v1.schema import ListDBSchema, ResponseSchema
from rag.backend.database.database import EmbeddingsTable, get_db
from rag.backend.models.models import EmbeddingModel, GenerationModel

app = FastAPI()

# Configure the logging settings
logging.basicConfig(level=logging.INFO)


@app.get("/", response_model=ListDBSchema)
async def root(
    db: EmbeddingsTable = Depends(get_db),
):
    try:
        db.connect()
        content = db.list_embeddings()
        logging.info("Content: %s", content)
        response = ListDBSchema(pages=content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return response


@app.post("/upload", response_model=ListDBSchema)
async def upload(
    file: UploadFile,
    embedding_model_name: str,
    db: EmbeddingsTable = Depends(get_db),
):
    logging.info("Received file: %s", file.filename)
    # Read the file content
    file_content = await file.read()
    file_content = file_content.replace(b"\x00", b"")

    logging.info("File content: %s", file_content)
    # Convert the file content to a string
    detection_result = chardet.detect(file_content)
    detected_encoding = detection_result["encoding"]
    file_content = file_content.decode(detected_encoding)
    # Break the file content into chunks
    file_content = file_content.split("\n")
    # Remove empty lines
    file_content = [line.strip() for line in file_content if line.strip()]
    # Connect to the database
    try:
        db.connect()
        db.create_table()
        # Add the file content to the database
        db.ingest_data(file_content, EmbeddingModel(embedding_model_name))
        logging.info("File content as string: %s", file_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    response = ListDBSchema(pages=file_content)

    return response


@app.get("/ask", response_model=ResponseSchema)
async def ask(
    question: str,
    embedding_model_name: str,
    generation_model_name: str,
    db: EmbeddingsTable = Depends(get_db),
):
    logging.info("Received question: %s", question)

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        db.connect()
        logging.info("Connected to database")

        embed_model = EmbeddingModel(embedding_model_name)
        user_question_embedding = embed_model.get_embedding(question)

        # Retrieve relevant chunks
        retrieved_knowledge = db.search_similar(user_question_embedding)
        logging.info("Retrieved chunks: %s", retrieved_knowledge)

        prompt = f"You are a helpful assistant. Here is the context to use to reply to the user question\
            : {retrieved_knowledge}. User question: {question}"

        # Generate response
        generation_model = GenerationModel(generation_model_name)
        answer = generation_model.generate_text(prompt)
        answer = ResponseSchema(response=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return answer
