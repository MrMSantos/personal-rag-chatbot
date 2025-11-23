import os

# Load environment variables from .env file
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from transformers import AutoModel, AutoTokenizer

load_dotenv()


class EmbeddingModel:
    def __init__(self, model_name):
        self.model = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs.last_hidden_state[:, 0, :].tolist()[0]


class GenerationModel:
    def __init__(self, model_name):
        self.model_name = model_name

    def generate_text(self, prompt):
        client = InferenceClient(
            api_key=os.getenv("HUGGINGFACE_API_KEY"),
        )

        completion = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )

        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


class VectorDB:
    def __init__(self, embedding_model):
        self.db = []
        self.embedding_model = embedding_model

    def add(self, chunk, embedding):
        self.db.append((chunk, embedding))

    def retrieve(self, query, top_n=3):
        query_embedding = self.embedding_model.get_embedding(query)
        # temporary list to store (chunk, similarity) pairs
        similarities = []
        for chunk, embedding in self.db:
            similarity = self.cosine_similarity(query_embedding, embedding)
            similarities.append((chunk, similarity))
        # sort by similarity in descending order, because higher similarity means more relevant chunks
        similarities.sort(key=lambda x: x[1], reverse=True)
        # finally, return the top N most relevant chunks
        return similarities[:top_n]

    def generate_prompt(self, retrieved_knowledge, input_query):
        prompt = f"Use the following pieces of information to help you answer \
            the question like if you were a pirate:\
            {' '.join([f' - {chunk}' for chunk, _ in retrieved_knowledge])} Question: {input_query}"
        return prompt

    def cosine_similarity(self, a, b):
        a = a.squeeze()
        b = b.squeeze()
        dot_product = sum([x * y for x, y in zip(a, b)])
        norm_a = sum([x**2 for x in a]) ** 0.5
        norm_b = sum([x**2 for x in b]) ** 0.5
        return dot_product / (norm_a * norm_b)

    def add_data(self, file_path):
        with open(file_path, "r", encoding="utf8") as file:
            data = file.readlines()
        for i, chunk in enumerate(data):
            embedding = self.embedding_model.get_embedding(chunk)
            self.add(chunk, embedding)
            print(f"Added chunk {i + 1}/{len(data)} to the database")
