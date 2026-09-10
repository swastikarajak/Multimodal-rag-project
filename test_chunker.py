from src.models import DocumentData, PageData
from src.chunker import chunk_document, count_tokens


def main():

    # Sample document
    document = DocumentData(
        source_file="sample.pdf",
        file_type="pdf",
        pages=[
            PageData(
                page_number=1,
                text="""
                Artificial Intelligence is transforming many industries.
                Companies are using AI to automate repetitive tasks.
                Machine learning allows systems to learn patterns from data.
                Natural language processing helps computers understand human language.
                Computer vision allows machines to understand images and videos.
                Generative AI can create text, images, audio, and code.
                Retrieval Augmented Generation combines language models with external information.
                This allows AI systems to provide answers based on specific documents.
                RAG systems are commonly used for document question answering.
                They first retrieve relevant information from a knowledge base.
                The retrieved information is then provided to a language model.
                The model uses this information to generate the final answer.
                """,
            )
        ]
    )

    document.pages[0].text = document.pages[0].text * 20

    # Create chunks
    chunks = chunk_document(document)

    print(f"Total chunks: {len(chunks)}")
    print()

    # Display every chunk
    for chunk in chunks:

        print("=" * 60)

        print(f"Chunk ID: {chunk.chunk_id}")
        print(f"Page: {chunk.page_number}")
        print(f"Type: {chunk.content_type}")

        print(
            f"Approx tokens: "
            f"{count_tokens(chunk.content)}"
        )

        print("\nContent:")
        print(chunk.content)

        print()


if __name__ == "__main__":
    main()