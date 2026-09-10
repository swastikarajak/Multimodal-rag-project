import json


def save_document_json(document, output_path):

    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(
            document.model_dump(),
            file,
            indent=4,
            ensure_ascii=False
        )