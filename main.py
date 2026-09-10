from src.image_parser import extract_image
from src.json_utils import save_document_json


IMAGE_PATH = "data/uploads/sample.png"
OUTPUT_PATH = "data/processed/sample_image.json"


def main():

    print("Starting image ingestion...")

    document = extract_image(IMAGE_PATH)

    save_document_json(
        document,
        OUTPUT_PATH
    )

    print("Image processed successfully!")

    print(
        f"Total pages: {len(document.pages)}"
    )


if __name__ == "__main__":
    main()