from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

client = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "documents"

def create_collection(vector_size: int):
    collections = client.get_collections().collections
    exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections
    )

    if exists:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )