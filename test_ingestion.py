from src.ingestion import process_document


def main():
    file_path = "data/uploads/sample.pdf"
    
    document, chunks = process_document(
        file_path
    )

    print("\n================================")
    print("INGESTION COMPLETE")
    print("================================")

    print(f"File: {document.source_file}")
    print(f"File type: {document.file_type}")
    print(f"Pages: {len(document.pages)}")
    print(f"Chunks: {len(chunks)}")

    print("\nCreated chunks:")

    for chunk in chunks:
        print(
            f"\nID: {chunk.chunk_id}"
        )
        print(
            f"Page: {chunk.page_number}"
        )
        print(
            f"Type: {chunk.content_type}"
        )
        print(
            f"Content: {chunk.content[:150]}..."
        )


if __name__ == "__main__":
    main()