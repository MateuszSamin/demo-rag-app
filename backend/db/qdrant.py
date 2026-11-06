from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
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

def store_embeddings(embeddings):
    points = []

    for item in embeddings:
        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=item["embedding"],
                payload={
                    "text": item["text"],
                    "filename": item["filename"],
                    "document_id": item["document_id"],
                    "chunk_index": item["chunk_index"],
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

def list_documents():
    documents = {}

    offset = None

    while True:
        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
            with_vectors=False,
            offset=offset,
        )

        for point in points:
            payload = point.payload

            document_id = payload["document_id"]

            if document_id not in documents:
                documents[document_id] = {
                    "document_id": document_id,
                    "filename": payload["filename"],
                    "chunks": 0,
                }

            documents[document_id]["chunks"] += 1

        if offset is None:
            break

    return list(documents.values())

def delete_document(document_id):
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(
                        value=document_id,
                    ),
                )
            ]
        )
    )