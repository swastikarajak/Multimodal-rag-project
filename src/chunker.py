import re
from pathlib import Path
from typing import List

import tiktoken

from .models import DocumentData, ChunkData


# Tokenizer used for local token estimation
tokenizer = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """
    Count the approximate number of tokens in a text.
    """
    return len(tokenizer.encode(text))


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into simple sentences.
    """
    text = text.strip()

    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def create_text_chunks(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> List[str]:
    """
    Create sentence-aware chunks.

    Target:
    - around 500 tokens per chunk
    - around 50 tokens overlap
    """

    sentences = split_into_sentences(text)

    if not sentences:
        return []

    chunks = []

    current_sentences = []
    current_tokens = 0

    for sentence in sentences:

        sentence_tokens = count_tokens(sentence)

       
        if (
            current_sentences
            and current_tokens + sentence_tokens > chunk_size
        ):
            chunk_text = " ".join(current_sentences)
            chunks.append(chunk_text)

            # Keep the last few sentences for overlap.
            overlap_sentences = []
            overlap_tokens = 0

            for previous_sentence in reversed(current_sentences):

                previous_tokens = count_tokens(previous_sentence)

                if overlap_tokens + previous_tokens <= overlap:
                    overlap_sentences.insert(
                        0,
                        previous_sentence
                    )
                    overlap_tokens += previous_tokens
                else:
                    break

            current_sentences = overlap_sentences
            current_tokens = overlap_tokens

        current_sentences.append(sentence)
        current_tokens += sentence_tokens

    # Add the final chunk
    if current_sentences:
        chunks.append(
            " ".join(current_sentences)
        )

    return chunks


def chunk_document(document: DocumentData) -> List[ChunkData]:
    chunks = []

    chunk_number = 1

    # Get document name without extension
    source_path = Path(document.source_file)

    source_name = (
    f"{source_path.stem}_{source_path.suffix.replace('.', '')}"
     )

    for page in document.pages:

        # ---------------------------------------------
        # TEXT CHUNKS
        # ---------------------------------------------

        text_chunks = create_text_chunks(
            page.text,
            chunk_size=500,
            overlap=50
        )

        for text_chunk in text_chunks:

            chunks.append(
                ChunkData(
                    chunk_id=f"{source_name}_chunk_{chunk_number}",
                    source_file=document.source_file,
                    file_type=document.file_type,
                    page_number=page.page_number,
                    content_type="text",
                    content=text_chunk
                )
            )

            chunk_number += 1


        # ---------------------------------------------
        # TABLE CHUNKS
        # ---------------------------------------------

        for table in page.tables:

            chunks.append(
                ChunkData(
                    chunk_id=f"{source_name}_chunk_{chunk_number}",
                    source_file=document.source_file,
                    file_type=document.file_type,
                    page_number=table.page_number,
                    content_type="table",
                    content=table.content
                )
            )

            chunk_number += 1


        # ---------------------------------------------
        # IMAGE CHUNKS
        # ---------------------------------------------

        for image in page.images:

            if image.description:

                chunks.append(
                    ChunkData(
                        chunk_id=f"{source_name}_chunk_{chunk_number}",
                        source_file=document.source_file,
                        file_type=document.file_type,
                        page_number=image.page_number,
                        content_type="image",
                        content=image.description
                    )
                )

                chunk_number += 1

    return chunks