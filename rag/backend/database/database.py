import os

import psycopg2
from pgvector.psycopg2 import register_vector


class EmbeddingsTable:
    def __init__(self, database, host, user, password):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(
            database=self.database,
            host=self.host,
            user=self.user,
            password=self.password,
            port=5432,
        )
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
        register_vector(self.conn)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector(384)
            )
        """)
        self.conn.commit()

    def drop_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS embeddings")
        # Drop all tables
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = self.cursor.fetchall()
        for table in tables:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
        self.conn.commit()

    # Create a new database
    def create_database(self):
        self.conn = psycopg2.connect(
            dbname="template1",
            host=self.host,
            user=self.user,
            password=self.password,
            port=5432,
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f"CREATE DATABASE {self.database}")
        except psycopg2.errors.DuplicateDatabase:
            pass  # Database already exists
        finally:
            self.conn.autocommit = False
        self.conn.commit()

    def insert_embedding(self, text, embedding_data):
        self.cursor.execute(
            """
            INSERT INTO embeddings (content, embedding) VALUES (%s, %s)
        """,
            (text, embedding_data),
        )
        self.conn.commit()

    def search_similar(self, query_embedding, k=5):
        register_vector(self.conn)
        self.cursor.execute(
            """
            SELECT content FROM embeddings
            ORDER BY embedding <-> CAST(%s AS vector) LIMIT %s;
        """,
            (query_embedding, k),
        )
        return self.cursor.fetchall()

    def ingest_data(self, data, embedding_model):
        for i, chunk in enumerate(data):
            embedding = embedding_model.get_embedding(chunk)
            self.insert_embedding(chunk, embedding)
            print(f"Added chunk {i + 1}/{len(data)} to the database")

    def list_embeddings(self):
        self.cursor.execute("SELECT content FROM embeddings")
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


def get_db() -> EmbeddingsTable:
    database = os.getenv("DATABASE_NAME")
    host = os.getenv("DATABASE_HOST")
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    return EmbeddingsTable(database, host, user, password)
