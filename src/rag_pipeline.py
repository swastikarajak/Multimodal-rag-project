from .vector_store import search_similar_chunks
from .generator import generate_answer


def answer_question(
    question: str,
    n_results: int = 5
):
    """
    Complete RAG pipeline:

    1. Search relevant chunks from ChromaDB
    2. Build context from retrieved chunks
    3. Generate an answer using Gemini
    4. Return answer with source information
    """

    # Step 1: Retrieve relevant chunks
    results = search_similar_chunks(
        query=question,
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Step 2: Build context
    context_parts = []

    for i, document in enumerate(documents):
        metadata = metadatas[i]

        context_parts.append(
            f"""
Source: {metadata['source_file']}
Page: {metadata['page_number']}
Content Type: {metadata['content_type']}

Content:
{document}
"""
        )

    context = "\n".join(context_parts)

    # Step 3: Generate answer
    answer = generate_answer(
        question=question,
        context=context
    )

    # Step 4: Return answer + sources
    return {
        "answer": answer,
        "sources": metadatas
    }