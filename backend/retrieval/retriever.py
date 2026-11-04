import ollama
from db.qdrant import client, COLLECTION_NAME

MODEL = "nomic-embed-text"

def retrieve(query: str, limit: int = 5):

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

    return [
        point.payload
        for point in results.points
    ]