import ollama
from db.qdrant import client, COLLECTION_NAME

MODEL = "nomic-embed-text"

def vector_search(query: str, limit: int = 5):

    response = ollama.embed(
        model=MODEL,
        input=query,
    )

    query_embedding = response["embeddings"][0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
    )

    chunks = []

    for point in results.points:
        chunks.append(
            {
                "text": point.payload["text"],
                "filename": point.payload["filename"],
                "document_id": point.payload["document_id"],
                "chunk_index": point.payload["chunk_index"],
            }
        )

    return chunks