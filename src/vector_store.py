import chromadb

from .models import ChunkData
from .embedding import create_embedding


CHROMA_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "document_chunks"


# Persistent ChromaDB client
client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)


# Create the collection if it does not exist
collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def add_chunks_to_vector_store(
    chunks: list[ChunkData]
):
    """
    Create embeddings for chunks
    and store them in ChromaDB.
    """

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:

        embedding = create_embedding(
            chunk.content
        )

        ids.append(chunk.chunk_id)

        documents.append(
            chunk.content
        )

        embeddings.append(
            embedding
        )

        metadatas.append(
            {
                "source_file": chunk.source_file,
                "file_type": chunk.file_type,
                "page_number": chunk.page_number,
                "content_type": chunk.content_type,
            }
        )

    if chunks:
        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
  )
        

def search_similar_chunks(
    query: str,
    n_results: int = 5
):
    """
    Find the most relevant chunks for a query.
    """

    query_embedding = create_embedding(
        query
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results