import base64
from pathlib import Path

from .models import DocumentData, PageData, ImageData


def extract_image(image_path: str) -> DocumentData:

    # Create the main document object
    document = DocumentData(
        source_file=image_path,
        file_type="image"
    )

    # Get image extension
    image_format = Path(image_path).suffix.lower().replace(".", "")

    # Read image as binary data
    with open(image_path, "rb") as image_file:

        image_bytes = image_file.read()

    # Convert binary image data to Base64
    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    # Create page object
    # A standalone image is treated as one logical page
    page_data = PageData(
        page_number=1,
        text=""
    )

    # Add image information
    page_data.images.append(
        ImageData(
            page_number=1,
            image_base64=image_base64,
            image_format=image_format
        )
    )

    # Add page to document
    document.pages.append(page_data)

    return document