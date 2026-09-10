import base64
import pymupdf
import pdfplumber

from .models import DocumentData, PageData, TableData, ImageData


def extract_pdf(pdf_path: str) -> DocumentData:

    document = DocumentData(
        source_file=pdf_path,
        file_type="pdf"
    )

    # Open PDF using PyMuPDF
    pdf = pymupdf.open(pdf_path)

    # Open PDF using pdfplumber for table extraction
    plumber_pdf = pdfplumber.open(pdf_path)

    for page_index, page in enumerate(pdf):

        page_number = page_index + 1

        # -----------------------------
        # Extract normal text
        # -----------------------------
        text = page.get_text("text")

        page_data = PageData(
            page_number=page_number,
            text=text
        )

        # -----------------------------
        # Extract tables
        # -----------------------------
        plumber_page = plumber_pdf.pages[page_index]

        tables = plumber_page.extract_tables()

        for table in tables:

            markdown_table = convert_table_to_markdown(table)

            page_data.tables.append(
                TableData(
                    page_number=page_number,
                    content=markdown_table
                )
            )

        # -----------------------------
        # Extract images
        # -----------------------------
        images = page.get_images(full=True)

        for image in images:

            xref = image[0]

            image_data = pdf.extract_image(xref)

            image_bytes = image_data["image"]
            image_ext = image_data["ext"]

            image_base64 = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            page_data.images.append(
                ImageData(
                    page_number=page_number,
                    image_base64=image_base64,
                    image_format=image_ext
                )
            )

        document.pages.append(page_data)

    plumber_pdf.close()
    pdf.close()

    return document


def convert_table_to_markdown(table):

    if not table:
        return ""

    # Replace None values
    table = [
        [cell if cell is not None else "" for cell in row]
        for row in table
    ]

    header = table[0]

    markdown = "| " + " | ".join(header) + " |\n"

    markdown += "| " + " | ".join(
        ["---"] * len(header)
    ) + " |\n"

    for row in table[1:]:

        markdown += "| " + " | ".join(row) + " |\n"

    return markdown