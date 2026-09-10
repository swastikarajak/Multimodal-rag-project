import base64

from google import genai

from .gemini_client import client


def describe_image(image_base64: str, image_format: str) -> str:
    """
    Sends an image to Gemini and returns a useful description.
    """

    image_bytes = base64.b64decode(image_base64)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            {
                "inline_data": {
                    "mime_type": f"image/{image_format}",
                    "data": image_bytes,
                }
            },
            """
            Describe this image in detail for a document retrieval system.

            Focus on:
            - What the image represents
            - Important objects or visual information
            - Charts, graphs, diagrams, or labels
            - Important numbers or values
            - Relationships shown in the image

            Do not make assumptions about information that is not visible.
            Return only the description.
            """
        ]
    )

    return response.text