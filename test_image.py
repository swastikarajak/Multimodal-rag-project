from src.image_parser import extract_image
from src.image_describer import describe_image
from src.json_utils import save_document_json


def main():
    image_path = "data/uploads/sample.png"

    document = extract_image(image_path)

    image = document.pages[0].images[0]

    image.description = describe_image(
        image.image_base64,
        image.image_format
    )

    output_path = "data/processed/sample_image.json"

    save_document_json(
        document,
        output_path
    )

    print("Image processed successfully!")
    print(f"JSON saved to: {output_path}")


if __name__ == "__main__":
    main()