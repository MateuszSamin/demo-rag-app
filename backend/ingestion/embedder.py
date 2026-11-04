from uuid import uuid4

import ollama

MODEL = "nomic-embed-text"

def embed_text(chunks, document_id, filename):
    embeddings = []

    for chunk in chunks:
        response = ollama.embed(
            model = MODEL,
            input = chunk.text,
        )

        embeddings.append({
            "text": chunk.text,
            "embedding": response["embeddings"][0],
            "document_id": document_id,
            "filename": filename,
            "chunk_index": str(uuid4())
        })

    return embeddings