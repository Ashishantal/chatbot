import cohere
import faiss
import numpy as np
import re
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("API_KEY")
co = cohere.Client(COHERE_API_KEY)

# Split long text into chunks
def chunk_text(text, max_words=150):
    words = text.split()
    chunks = [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]
    return chunks

# Embed chunks using Cohere
def embed_text_cohere(chunks):
    response = co.embed(
        texts=chunks,
        model="embed-english-v3.0",  # Or "embed-english-light-v3.0" for faster
        input_type="search_document"
    )
    embeddings = response.embeddings
    return list(zip(chunks, embeddings))

# Save into FAISS
import os

def save_to_faiss(embeddings, base_name):
    dim = len(embeddings[0][1])
    index = faiss.IndexFlatL2(dim)

    vectors = [np.array(e[1], dtype='float32') for e in embeddings]
    index.add(np.stack(vectors))

    # Create media folders if they don't exist
    os.makedirs("media/vectors", exist_ok=True)
    os.makedirs("media/texts", exist_ok=True)

    # Save vector index
    index_path = f"media/vectors/{base_name}.index"
    faiss.write_index(index, index_path)

    # Save text chunks
    texts = [e[0] for e in embeddings]
    text_path = f"media/texts/{base_name}.txt"
    with open(text_path, "w", encoding="utf-8") as f:
        for t in texts:
            f.write(t.replace("\n", " ") + "\n")

