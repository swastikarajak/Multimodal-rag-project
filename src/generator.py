from .gemini_client import client


GENERATION_MODEL = "gemini-3.5-flash"


def generate_answer(
    question: str,
    context: str
) -> str:
    """
    Generate an answer using the user's question
    and the retrieved document context.
    """

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context,
say that the information is not available in the provided documents.

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt
    )

    return response.text