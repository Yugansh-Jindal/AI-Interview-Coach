import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="interview_data",
    embedding_function=embedding_function
)


def store_chunks(chunks, document_name, user_id):
    """
    Store document chunks in ChromaDB.
    Existing chunks for the same document are replaced.
    """

    if not chunks:
        return

    # Remove previous chunks for this document
    try:
        existing = collection.get(
        where={
            "$and": [
                {"source": document_name},
                {"user_id": str(user_id)}
        ]
    }
)

        if existing["ids"]:
            collection.delete(
                ids=existing["ids"]
            )

    except Exception as e:
         raise e

    ids = [
        f"user_{user_id}_{document_name}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "user_id": str(user_id),
            "source": document_name,
            "chunk_index": index
        }
    for index in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )


def get_document_chunks(document_name, user_id):

    results = collection.get(
        where={
            "$and": [
             {"source": document_name},
             {"user_id": str(user_id)}
        ]
    }
)

    return results.get("documents", [])


def clear_vector_store(user_id):

    try:

        results = collection.get(
            where={
                "user_id": str(user_id)
            }
        )

        ids = results.get("ids", [])

        if ids:
            collection.delete(ids=ids)

    except Exception as e:
        raise e