import docx
import fitz

import os
import faiss
import numpy as np
from cohere import client

import os



from nltk.tokenize import sent_tokenize
import nltk


co = client.Client(os.getenv("API_KEY"))
def extract_pdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text = text + page.get_text()
    return text

def extract_docx(path):
    text = ""
    doc = docx.Document(path)
    for para in doc.paragraphs:
        text = text + para.text + "\n"
    return text

def process_question(question, base_name):
    from cohere import client
    import os
    co = client.Client(os.getenv("API_KEY"))
    

    response = co.embed(texts=[question], model="embed-english-v3.0", input_type="search_query")
    query_vector = np.array(response.embeddings[0], dtype='float32')

    index_path = f"media/vectors/{base_name}.index"
    if not os.path.exists(index_path):
        return "This document has not been indexed yet.", ""

    index = faiss.read_index(index_path)
    top_k = 3
    D, I = index.search(np.array([query_vector]), top_k)

    with open(f"media/texts/{base_name}.txt", "r", encoding="utf-8") as f:
        chunks = f.readlines()

    results = [chunks[i].strip() for i in I[0]]
    context = "\n\n".join(results)

    prompt = f"""
    You are an assistant helping extract answers from a resume. 
    All the data provided is from the user's own document.

    Context:
    {context}

    Question: {question}
    Answer:
    """
    response = co.chat(
        model="command-r-plus-08-2024",
        message=prompt,
        temperature=0.3
    )
    return response.text.strip(), context





def save_to_faiss_and_text(text, filename_base):
    # Step 1: Split text into chunks
    
    lines = text.split('\n')
    chunks = []
    chunk = ""

    for line in lines:
       if len(chunk) + len(line) < 500:
          chunk += " " + line.strip()
       else:

        chunks.append(chunk.strip())
        chunk = line.strip()
    if chunk:
      chunks.append(chunk.strip())

    # Step 2: Get embeddings from Cohere
    response = co.embed(
        texts=chunks,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    embeddings = np.array(response.embeddings, dtype='float32')

    # Step 3: Save FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs("media/vectors", exist_ok=True)
    os.makedirs("media/texts", exist_ok=True)

    faiss.write_index(index, f"media/vectors/{filename_base}.index")

    # Step 4: Save corresponding chunks
    with open(f"media/texts/{filename_base}.txt", "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n")

