from pathlib import Path

from .pdf_parser import extract_pdf
from .docx_parser import extract_docx
from .image_parser import extract_image
from .image_describer import describe_image
from .chunker import chunk_document
from .vector_store import add_chunks_to_vector_store
from .json_utils import save_document_json


def process_document(file_path: str):
    """
    Complete document ingestion pipeline.

    Supported formats:
    - PDF
    - DOCX
    - PNG
    - JPG / JPEG

    Steps:
    1. Detect file type
    2. Extract document content
    3. Describe images using Gemini
    4. Create chunks
    5. Store chunks in ChromaDB
    6. Save processed document as JSON
    """

    file_path = Path(file_path)

    # --------------------------------------------------
    # STEP 1: Detect file type
    # --------------------------------------------------

    extension = file_path.suffix.lower()

    print(f"Processing: {file_path.name}")

    # --------------------------------------------------
    # STEP 2: Extract document
    # --------------------------------------------------

    if extension == ".pdf":

        print("Detected PDF")

        document = extract_pdf(
            str(file_path)
        )

    elif extension == ".docx":

        print("Detected DOCX")

        document = extract_docx(
            str(file_path)
        )

    elif extension in [".png", ".jpg", ".jpeg"]:

        print("Detected Image")

        document = extract_image(
            str(file_path)
        )

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    print("Content extracted successfully.")

    # --------------------------------------------------
    # STEP 3: Describe images
    # --------------------------------------------------

    image_count = 0

    for page in document.pages:

        for image in page.images:

            if not image.description:

                print(
                    f"Describing image on page "
                    f"{image.page_number}..."
                )

                image.description = describe_image(
                    image.image_base64,
                    image.image_format
                )

                image_count += 1

    print(
        f"Images processed: {image_count}"
    )

    # --------------------------------------------------
    # STEP 4: Create chunks
    # --------------------------------------------------

    chunks = chunk_document(
        document
    )

    print(
        f"Chunks created: {len(chunks)}"
    )

    # --------------------------------------------------
    # STEP 5: Store chunks in ChromaDB
    # --------------------------------------------------

    if chunks:

        add_chunks_to_vector_store(
            chunks
        )

        print(
            "Chunks stored in ChromaDB successfully."
        )

    else:

        print(
            "No chunks were created."
        )

    # --------------------------------------------------
    # STEP 6: Save processed JSON
    # --------------------------------------------------

    output_directory = Path(
        "data/processed"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )


    output_path = (
        output_directory
        / f"{file_path.stem}_{extension.replace('.', '')}.json"
    )
    

    save_document_json(
        document,
        str(output_path)
    )

    print(
        f"Processed JSON saved to: {output_path}"
    )

    return document, chunks