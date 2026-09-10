from typing import List

from .gemini_client import client


EMBEDDING_MODEL = "gemini-embedding-001"


def create_embedding(text: str) -> List[float]:
    """
    Convert text into an embedding vector.
    """

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values
