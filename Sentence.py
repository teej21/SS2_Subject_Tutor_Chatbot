from sentence_transformers import SentenceTransformer
from hashlib import *

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(sentences):
    """
    generate embeddings for the sentences list
    """
    embeddings = model.encode(sentences)
    vectors = [{"id": md5(sentences[i].encode()).hexdigest(), "values": embedding.tolist()} for i, embedding in
               enumerate(embeddings)]
    return vectors


def generate_embedding(prompt):
    """
    generate embeddings from prompt to query
    """
    return model.encode(prompt).tolist()
