from src.models import ChunkData
from src.vector_store import (
    add_chunks_to_vector_store,
    search_similar_chunks
)


def main():
    # Dummy chunks for testing
    chunks = [
        ChunkData(
            chunk_id="test_chunk_1",
            source_file="sample.pdf",
            file_type="pdf",
            page_number=1,
            content_type="text",
            content=(
                "Artificial Intelligence is the field of building "
                "machines that can perform tasks requiring human intelligence."
            )
        ),
        ChunkData(
            chunk_id="test_chunk_2",
            source_file="sample.pdf",
            file_type="pdf",
            page_number=2,
            content_type="text",
            content=(
                "Machine Learning is a subset of Artificial Intelligence "
                "that allows systems to learn patterns from data."
            )
        ),
        ChunkData(
            chunk_id="test_chunk_3",
            source_file="sample.pdf",
            file_type="pdf",
            page_number=3,
            content_type="text",
            content=(
                "Robotics combines mechanical systems, electronics, "
                "sensors and software to build intelligent machines."
            )
        )
    ]

    # Store chunks in ChromaDB
    add_chunks_to_vector_store(chunks)

    print("Chunks stored successfully!\n")

    # Search
    query = "What is Machine Learning?"

    results = search_similar_chunks(
        query,
        n_results=2
    )

    print("Query:")
    print(query)

    print("\nRetrieved chunks:")

    for i, document in enumerate(results["documents"][0]):
        print(f"\nResult {i + 1}:")
        print(document)

        print("Metadata:")
        print(results["metadatas"][0][i])

        print("Distance:")
        print(results["distances"][0][i])


if __name__ == "__main__":
    main()