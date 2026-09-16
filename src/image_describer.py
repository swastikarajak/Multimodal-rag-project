import base64
import time

from google.genai.errors import ServerError

from .gemini_client import client


def describe_image(
    image_base64: str,
    image_format: str,
    max_retries: int = 3
) -> str:
    """
    Sends an image to Gemini and returns a useful description.

    If Gemini temporarily returns a server error such as 503,
    the request is retried a few times.
    """

    image_bytes = base64.b64decode(image_base64)

    for attempt in range(max_retries):
        try:
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
                    Describe this image in detail for a document
                    retrieval system.

                    Focus on:
                    - What the image represents
                    - Important objects or visual information
                    - Charts, graphs, diagrams, or labels
                    - Important numbers or values
                    - Relationships shown in the image

                    Do not make assumptions about information
                    that is not visible.

                    Return only the description.
                    """
                ]
            )

            return response.text

        except ServerError as error:

            # If this was the final attempt, raise the error
            if attempt == max_retries - 1:
                raise error

            # Exponential backoff:
            # attempt 0 → 2 seconds
            # attempt 1 → 4 seconds
            wait_time = 2 ** (attempt + 1)

            print(
                f"Gemini server error. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)