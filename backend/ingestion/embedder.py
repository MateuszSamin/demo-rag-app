import ollama

MODEL = "nomic-embed-text"

def embed_text(chunks):
    embeddings = []

    for chunk in chunks:
        response = ollama.embed(
            model = MODEL,
            input = chunk.text,
        )

        embeddings.append({
            "text": chunk.text,
            "embedding": response["embeddings"][0]
        })

    return embeddings